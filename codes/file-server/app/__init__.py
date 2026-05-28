"""Flask application factory and routes."""

import os
import socket
import subprocess
import urllib.parse
from datetime import datetime

from flask import Flask, current_app, jsonify, render_template, request

from .config import config
from .utils import file_emoji, human_size, safe_path


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        static_folder="../static",
        template_folder="templates",
    )
    # Flask config keys are uppercase by convention; map from the dataclass.
    app.config.update({
        "SERVE_DIR": config.serve_dir,
        "PORT": config.port,
        "HOST": config.host,
        "PAGE_SIZE": config.page_size,
        "EDITABLE_EXTENSIONS": config.editable_extensions,
        "VIEWABLE_EXTENSIONS": config.viewable_extensions,
    })

    # Register routes
    app.add_url_rule("/", "index", _serve_directory_listing)
    app.add_url_rule("/edit", "edit", _serve_editor)
    app.add_url_rule("/save", "save", _handle_save, methods=["POST"])
    app.add_url_rule("/git", "git", _serve_git_repos)
    # Static file serving — catch-all for files in the serve directory
    app.add_url_rule("/<path:filename>", "serve_file", _serve_static_file)

    return app


def _serve_directory_listing() -> str:
    """Render the paginated file-list page with subdirectory support."""
    cfg = current_app.config
    base_dir = cfg["SERVE_DIR"]

    # Subdirectory browsing: ?subdir=main
    subdir = request.args.get("subdir", "").strip("/")
    serve_dir = os.path.normpath(os.path.join(base_dir, subdir)) if subdir else base_dir

    # Security: ensure we stay inside base_dir
    base_prefix = os.path.normpath(base_dir)
    if not (serve_dir == base_prefix or serve_dir.startswith(base_prefix + os.sep)):
        return "Forbidden", 403

    try:
        dirs, files = _collect_dir_entries(serve_dir)
    except OSError as exc:
        return f"<h1>500 — {exc}</h1>", 500

    # Build directory items (folders)
    dir_items = [_build_dir_item(d, subdir) for d in dirs]
    # Build file items
    file_items = [
        _build_file_item(name, size, mtime, subdir)
        for name, size, mtime in files
    ]
    items = dir_items + file_items

    page = max(1, request.args.get("page", 1, type=int))
    page_size = cfg["PAGE_SIZE"]
    total = len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = min(page, total_pages)

    start = (page - 1) * page_size
    end = min(start + page_size, total)
    shown = items[start:end]

    hostname = os.uname().nodename

    # Breadcrumb parts for display
    breadcrumbs = []
    if subdir:
        parts = subdir.split("/")
        path_so_far = ""
        for i, p in enumerate(parts):
            path_so_far = "/".join(parts[:i + 1])
            breadcrumbs.append({"name": p, "path": path_so_far, "last": i == len(parts) - 1})

    count_label = f"{len(dirs)} 个目录 · {len(files)} 个文件" if dirs else f"{len(files)} 个文件"

    return render_template(
        "index.html",
        title=f"📁 {subdir or '文档库'} — AI Repository",
        count=count_label,
        host=f"ai_repo — {hostname}",
        items=shown,
        page=page,
        total_pages=total_pages,
        subdir=subdir,
        breadcrumbs=breadcrumbs,
        enumerate=enumerate,
    )


def _serve_editor() -> str:
    """Serve the online text editor page for a file."""
    cfg = current_app.config
    base_dir = cfg["SERVE_DIR"]

    filename = request.args.get("file", "")
    if not filename:
        return "Missing file parameter", 400

    # Support subdir for editor too
    subdir = request.args.get("subdir", "")
    if subdir:
        filename = os.path.join(subdir, filename)

    fullpath = safe_path(base_dir, filename)
    if not fullpath or not os.path.isfile(fullpath):
        return "File not found", 404

    ext = os.path.splitext(filename)[1].lower()
    if ext not in cfg["EDITABLE_EXTENSIONS"]:
        return "This file type is not editable", 403

    try:
        with open(fullpath, encoding="utf-8") as fh:
            content = fh.read()
    except (OSError, ValueError) as exc:
        return f"<h1>500 — {exc}</h1>", 500

    line_count = content.count("\n") + 1

    return render_template(
        "editor.html",
        title=f"✏️ {filename} — 在线编辑",
        filename=filename,
        content=content,
        lines=line_count,
        file_encoded=urllib.parse.quote(filename),
    )


def _handle_save():
    """Handle POST /save — write edited content to disk."""
    cfg = current_app.config
    serve_dir = cfg["SERVE_DIR"]

    filename = request.form.get("file", "")
    content = request.form.get("content", "")

    if not filename:
        return jsonify({"ok": False, "error": "Missing file parameter"})

    fullpath = safe_path(serve_dir, filename)
    if not fullpath:
        return jsonify({"ok": False, "error": "Invalid file path"})

    ext = os.path.splitext(filename)[1].lower()
    if ext not in cfg["EDITABLE_EXTENSIONS"]:
        return jsonify({"ok": False, "error": "Cannot edit this file type"})

    try:
        with open(fullpath, "w", encoding="utf-8") as fh:
            fh.write(content)
    except (OSError, ValueError) as exc:
        return jsonify({"ok": False, "error": str(exc)})

    return jsonify({"ok": True})


def _serve_static_file(filename: str):
    """Serve a static file from the serve directory, supporting subdirs."""
    from flask import send_from_directory

    cfg = current_app.config
    base_dir = cfg["SERVE_DIR"]

    subdir = request.args.get("subdir", "")
    serve_dir = os.path.normpath(os.path.join(base_dir, subdir)) if subdir else base_dir

    # Path traversal check
    abs_path = os.path.normpath(os.path.join(serve_dir, filename))
    allowed_prefix = os.path.normpath(serve_dir)
    if not (
        abs_path == allowed_prefix or abs_path.startswith(allowed_prefix + os.sep)
    ):
        return "Forbidden", 403

    if not os.path.isfile(abs_path):
        return "File not found", 404

    return send_from_directory(serve_dir, filename)


# ── git repo browser ──

# Git repo directory (configurable for Docker)
GIT_REPO_DIR = os.environ.get("FILESERVER_GIT_DIR", "/srv/git")
# Public host IP for clone URLs (set via env in Docker)
PUBLIC_HOST = os.environ.get("FILESERVER_HOST_IP", "")


def _get_local_ip() -> str:
    """Return the machine's public IP (env or detected)."""
    if PUBLIC_HOST:
        return PUBLIC_HOST
    try:
        # Use socket to get the IP that connects to an external address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("192.168.31.1", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        # Fallback: parse ip addr output
        try:
            result = subprocess.run(
                ["ip", "-4", "addr", "show", "scope", "global"],
                capture_output=True, text=True,
            )
            for line in result.stdout.split("\n"):
                if "inet " in line and "127." not in line:
                    return line.strip().split()[1].split("/")[0]
        except OSError:
            pass
        return "127.0.0.1"


def _scan_git_repos() -> list[dict]:
    """Scan GIT_REPO_DIR for bare repositories and return metadata."""
    repos: list[dict] = []
    if not os.path.isdir(GIT_REPO_DIR):
        return repos
    try:
        names = sorted(os.listdir(GIT_REPO_DIR))
    except OSError:
        return repos

    local_ip = _get_local_ip()

    for name in names:
        if not name.endswith(".git"):
            continue
        full = os.path.join(GIT_REPO_DIR, name)
        if not os.path.isdir(full):
            continue

        repo_name = name[:-4]  # strip .git
        desc = ""
        desc_path = os.path.join(full, "description")
        if os.path.isfile(desc_path):
            try:
                with open(desc_path, encoding="utf-8") as f:
                    desc = f.read().strip()
            except OSError:
                pass

        # Get last commit info
        last_commit = ""
        try:
            result = subprocess.run(
                ["git", "--git-dir", full, "log", "-1",
                 "--format=%h %s (%ar)"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0:
                last_commit = result.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass

        repos.append({
            "name": repo_name,
            "description": desc or "No description",
            "git_url": f"git://{local_ip}/{name}",
            "http_url": f"http://{local_ip}:3000/{name}",
            "ssh_url": f"git@{local_ip}:/srv/git/{name}",
            "last_commit": last_commit or "—",
        })

    return repos


def _serve_git_repos() -> str:
    """Render the Git repository discovery page."""
    repos = _scan_git_repos()
    local_ip = _get_local_ip()
    return render_template(
        "git.html",
        title="📦 Git 仓库",
        repos=repos,
        host_ip=local_ip,
        total=len(repos),
    )


# ── helpers ──


def _collect_dir_entries(
    serve_dir: str,
) -> tuple[list[str], list[tuple[str, int, float]]]:
    """Scan *serve_dir* and return ``(directories, files)`` sorted.
    Directories sorted alphabetically, files sorted by mtime descending (newest first).
    Dot-files and dot-directories are skipped."""
    dirs: list[str] = []
    files: list[tuple[str, int, float]] = []
    try:
        names = os.listdir(serve_dir)
    except OSError:
        return dirs, files

    for name in names:
        if name.startswith("."):
            continue
        full = os.path.join(serve_dir, name)
        try:
            stat = os.stat(full)
        except OSError:
            continue
        if os.path.isdir(full):
            dirs.append(name)
        else:
            files.append((name, stat.st_size, stat.st_mtime))

    dirs.sort()
    files.sort(key=lambda e: e[2], reverse=True)
    return dirs, files


def _build_dir_item(dirname: str, parent_subdir: str) -> dict:
    """Build a directory entry for template rendering."""
    path = f"{parent_subdir}/{dirname}" if parent_subdir else dirname
    return {
        "name": dirname,
        "emoji": "📂",
        "size": "—",
        "date": "",
        "encoded": urllib.parse.quote(dirname),
        "show_view": False,
        "show_edit": False,
        "is_dir": True,
        "subdir_path": path,
    }


def _build_file_item(
    name: str, size: int, mtime: float, subdir: str = ""
) -> dict:
    """Build a dictionary with file info for template rendering."""
    emoji = file_emoji(name)
    date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    size_str = human_size(size)
    encoded = urllib.parse.quote(name)
    ext = os.path.splitext(name)[1].lower()

    cfg = current_app.config

    show_view = ext in cfg["VIEWABLE_EXTENSIONS"]
    show_edit = ext in cfg["EDITABLE_EXTENSIONS"]

    return {
        "name": name,
        "emoji": emoji,
        "size": size_str,
        "date": date_str,
        "encoded": encoded,
        "show_view": show_view,
        "show_edit": show_edit,
        "is_dir": False,
        "subdir_path": "",
    }
