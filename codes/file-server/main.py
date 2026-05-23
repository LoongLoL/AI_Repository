#!/usr/bin/env python3
"""Entry point for the OpenClaw File Server.

Usage:
    python main.py              # uses default config / env vars
    FILESERVER_PORT=8080 python main.py
"""

from app import create_app
from app.config import config

app = create_app()

if __name__ == "__main__":
    print(f"📁 Serving {config.serve_dir} on http://{config.host}:{config.port}")
    app.run(host=config.host, port=config.port, debug=False)
