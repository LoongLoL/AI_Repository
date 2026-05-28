# Django 文件管理器

一个简洁的服务器文件浏览/编辑/下载工具，无需登录即可访问。

## 功能

- 📁 三级目录结构：主目录 → 子目录 → 文件列表
- 📄 文件列表分页（默认每页 20 条）
- 👁 **预览**：图片、PDF、视频、音频、HTML 等 Chrome 可直接打开的格式
- ✏️ **编辑**：txt、md、json、py、js、css 等纯文本格式，支持在线保存
- ⬇️ **下载**：所有文件均可下载
- 🔓 无权限验证，直接访问即可

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置文件根目录

**方式一：环境变量（推荐）**
```bash
export FILES_ROOT=/your/files/path
```

**方式二：修改 settings.py**
```python
# filemanager/settings.py
FILES_ROOT = '/your/files/path'
```

### 3. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

然后访问 `http://服务器IP:8000`

## 每页文件数量

在 `filemanager/settings.py` 中修改：
```python
FILES_PER_PAGE = 20  # 改成你想要的数量
```

## 生产部署（gunicorn + nginx）

```bash
pip install gunicorn
gunicorn filemanager.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

Nginx 配置示例：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/filemanager/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # 大文件下载超时设置
        proxy_read_timeout 300;
        proxy_send_timeout 300;
    }
}
```

## 目录结构

```
filemanager/
├── manage.py
├── requirements.txt
├── filemanager/          # 项目配置
│   ├── settings.py       # ← 修改 FILES_ROOT 和 FILES_PER_PAGE
│   ├── urls.py
│   └── wsgi.py
└── files/                # 核心应用
    ├── views.py           # 视图逻辑
    ├── urls.py            # 路由
    └── templates/files/
        ├── base.html      # 基础布局
        ├── index.html     # 主目录
        ├── browse.html    # 子目录
        ├── edit.html      # 编辑器
        ├── error.html     # 错误页
        └── _file_table.html  # 文件表格组件
```

## 支持的文件类型

### 可预览（浏览器直接打开）
图片：jpg, jpeg, png, gif, webp, svg, bmp
视频：mp4, webm, ogg
音频：mp3, wav, flac
文档：pdf, html

### 可编辑（在线编辑器）
txt, md, csv, json, xml, yaml, ini, cfg, conf, log,
py, js, css, html, sh, sql, .env

### 可下载
所有文件
