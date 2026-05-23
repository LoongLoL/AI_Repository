# OpenClaw File Server

A lightweight, modern file server with directory listing, online text
editor, and file viewer — rebuilt to modern Python web project standards.

## Features

- 📁 **Directory listing** with pagination, emoji icons, and human-readable file sizes
- ✏️ **Online editor** for text files (Markdown, HTML, CSS, JS, JSON, XML, TXT)
- 👁 **File viewer** for browser-displayable formats including images
- 🔒 **Path-traversal protection** — only serves files within the configured directory
- 🎨 **Clean, responsive UI** — works on desktop and mobile

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with defaults (port 7890, serves /root/.openclaw/workspace/projects/downloads)
python main.py

# Or customize via environment variables
FILESERVER_PORT=8080 FILESERVER_DIR=/var/www/files python main.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FILESERVER_DIR` | `/root/.openclaw/workspace/projects/downloads` | Directory to serve |
| `FILESERVER_PORT` | `7890` | HTTP port |
| `FILESERVER_HOST` | `0.0.0.0` | Bind address |
| `FILESERVER_PAGE_SIZE` | `15` | Files per page |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## Project Structure

```
file-server/
├── app/
│   ├── __init__.py      # Flask app factory & routes
│   ├── config.py         # Configuration (env vars)
│   ├── utils.py          # Helper functions
│   └── templates/        # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       └── editor.html
├── static/
│   ├── css/style.css
│   └── js/editor.js
├── tests/                # pytest test suite
├── main.py               # Entry point
├── pyproject.toml
└── requirements.txt
```

## License

MIT
