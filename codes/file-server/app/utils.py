"""Utility functions for the file server."""

import os
from typing import Optional


def file_emoji(filename: str) -> str:
    """Pick an emoji icon for a filename based on extension or content hints."""
    ext = os.path.splitext(filename)[1].lower()
    lower = filename.lower()

    if "菜谱" in lower:
        return "\U0001F373"  # 🍳
    if "学习" in lower or "笔记" in lower:
        return "\U0001F4DD"  # 📝

    emoji_map = {
        ".md": "\U0001F4C4",    # 📄
        ".pptx": "\U0001F4CA",  # 📊
        ".ppt": "\U0001F4CA",   # 📊
        ".html": "\U0001F310",  # 🌐
        ".pdf": "\U0001F4D5",   # 📕
    }
    if ext in emoji_map:
        return emoji_map[ext]

    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
    if ext in image_exts:
        return "\U0001F5BC"  # 🖼

    return "\U0001F4C4"  # 📄


def human_size(size: int) -> str:
    """Return a human-readable size string (B / KB / MB)."""
    if size < 1024:
        return f"{size} B"
    if size < 1048576:
        return f"{size / 1024:.1f} KB"
    return f"{size / 1048576:.1f} MB"


def safe_path(serve_dir: str, filename: str) -> Optional[str]:
    """Resolve *filename* against *serve_dir* with path-traversal protection.

    Returns the absolute path if safe, or None if the path escapes the serve
    directory.
    """
    target = os.path.normpath(os.path.join(serve_dir, filename))
    allowed_prefix = os.path.normpath(serve_dir)
    # startswith with prefix + sep handles the case where target == prefix
    if target == allowed_prefix or target.startswith(allowed_prefix + os.sep):
        return target
    return None
