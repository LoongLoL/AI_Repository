import os
import mimetypes
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator
from django.http import (
    HttpResponse, Http404, JsonResponse, FileResponse, StreamingHttpResponse
)
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.utils.encoding import smart_str


# ── 工具函数 ────────────────────────────────────────────────

def get_files_root() -> Path:
    return Path(settings.FILES_ROOT)


def safe_resolve(base: Path, *parts: str) -> Path:
    """将用户提供的路径拼接并确保不会逃逸出 base 目录（防路径穿越）。"""
    target = (base / Path(*parts)).resolve()
    if not str(target).startswith(str(base.resolve())):
        raise Http404("非法路径")
    return target


def file_info(path: Path, base: Path) -> dict:
    """返回文件/目录的基本信息字典。"""
    stat = path.stat()
    ext = path.suffix.lower()
    is_dir = path.is_dir()
    rel = path.relative_to(base)

    mtime_dt = datetime.fromtimestamp(stat.st_mtime)
    return {
        'name': path.name,
        'rel_path': str(rel).replace('\\', '/'),
        'is_dir': is_dir,
        'size': stat.st_size if not is_dir else None,
        'size_human': human_size(stat.st_size) if not is_dir else '—',
        'mtime': mtime_dt.strftime('%Y-%m-%d %H:%M'),
        'ext': ext,
        'can_preview': ext in settings.PREVIEWABLE_TYPES,
        'can_edit': ext in settings.EDITABLE_TYPES,
    }


def human_size(size: int) -> str:
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def list_directory(path: Path, base: Path) -> tuple[list, list]:
    """返回 (dirs, files) 两个列表，均为 file_info 字典。"""
    dirs, files = [], []
    try:
        entries = list(path.iterdir())
    except PermissionError:
        return [], []

    dirs = sorted([e for e in entries if e.is_dir() and not e.name.startswith('.')], key=lambda p: p.name.lower())
    files = sorted([e for e in entries if e.is_file() and not e.name.startswith('.')], key=lambda p: p.stat().st_mtime, reverse=True)

    dirs = [file_info(d, base) for d in dirs]
    files = [file_info(f, base) for f in files]

    return dirs, files


# ── 视图 ────────────────────────────────────────────────────

def index(request):
    """主目录：列出所有子目录。"""
    base = get_files_root()
    if not base.exists():
        return render(request, 'files/error.html', {
            'message': f'文件根目录不存在：{base}',
            'tip': '请在 settings.py 中设置正确的 FILES_ROOT，或设置环境变量 FILES_ROOT。'
        })

    dirs, files = list_directory(base, base)

    return render(request, 'files/index.html', {
        'dirs': dirs,
        'files': files,
        'current_path': '',
        'breadcrumbs': [],
    })


def browse(request, rel_path=''):
    """子目录/文件列表页，支持分页。"""
    base = get_files_root()
    target = safe_resolve(base, rel_path) if rel_path else base

    if not target.exists():
        raise Http404("路径不存在")

    # 如果是文件，直接跳转预览
    if target.is_file():
        return redirect('preview', rel_path=rel_path)

    dirs, files = list_directory(target, base)

    # 分页（只对文件分页，子目录全部展示）
    per_page = settings.FILES_PER_PAGE
    paginator = Paginator(files, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 面包屑导航
    breadcrumbs = build_breadcrumbs(rel_path)

    return render(request, 'files/browse.html', {
        'dirs': dirs,
        'page_obj': page_obj,
        'current_path': rel_path,
        'breadcrumbs': breadcrumbs,
        'total_files': len(files),
    })


def preview(request, rel_path):
    """文件预览（在浏览器内直接打开）。"""
    base = get_files_root()
    target = safe_resolve(base, rel_path)

    if not target.exists() or not target.is_file():
        raise Http404("文件不存在")

    ext = target.suffix.lower()
    if ext not in settings.PREVIEWABLE_TYPES:
        raise Http404("该文件类型不支持预览")

    mime = settings.PREVIEWABLE_TYPES[ext]
    # 文本类 MIME 必须指定 charset，否则中文乱码
    if mime.startswith('text/'):
        mime = f'{mime}; charset=utf-8'
    try:
        file_obj = open(target, 'rb')
        response = FileResponse(file_obj, content_type=mime)
        response['Content-Disposition'] = f'inline; filename="{smart_str(target.name)}"'
        return response
    except IOError as e:
        raise Http404(f"无法打开文件：{str(e)}")


def edit(request, rel_path):
    """文本文件编辑页。"""
    base = get_files_root()
    target = safe_resolve(base, rel_path)

    if not target.exists() or not target.is_file():
        raise Http404("文件不存在")

    ext = target.suffix.lower()
    if ext not in settings.EDITABLE_TYPES:
        raise Http404("该文件类型不支持编辑")

    breadcrumbs = build_breadcrumbs(rel_path)
    parent_path = str(Path(rel_path).parent).replace('\\', '/')
    if parent_path == '.':
        parent_path = ''

    if request.method == 'POST':
        content = request.POST.get('content', '')
        try:
            target.write_text(content, encoding='utf-8')
            return JsonResponse({'ok': True, 'message': '保存成功'})
        except Exception as e:
            return JsonResponse({'ok': False, 'message': str(e)}, status=500)

    # GET：读取文件内容
    try:
        content = target.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            content = target.read_text(encoding='gbk')
        except Exception:
            content = target.read_bytes().decode('utf-8', errors='replace')

    return render(request, 'files/edit.html', {
        'content': content,
        'rel_path': rel_path,
        'filename': target.name,
        'breadcrumbs': breadcrumbs,
        'parent_path': parent_path,
        'file_size': human_size(target.stat().st_size),
        'ext': ext,
    })


def download(request, rel_path):
    """文件下载（强制下载，不在浏览器打开）。"""
    base = get_files_root()
    target = safe_resolve(base, rel_path)

    if not target.exists() or not target.is_file():
        raise Http404("文件不存在")

    try:
        file_obj = open(target, 'rb')
        response = FileResponse(file_obj, as_attachment=True)
        response['Content-Disposition'] = (
            f'attachment; filename="{smart_str(target.name)}"'
        )
        response['Content-Length'] = target.stat().st_size
        return response
    except IOError as e:
        raise Http404(f"无法读取文件：{str(e)}")


# ── 辅助函数 ────────────────────────────────────────────────

def build_breadcrumbs(rel_path: str) -> list[dict]:
    """生成面包屑导航数据。"""
    if not rel_path:
        return []
    parts = Path(rel_path).parts
    crumbs = []
    for i, part in enumerate(parts):
        path = '/'.join(parts[:i + 1])
        crumbs.append({'name': part, 'path': path})
    return crumbs
