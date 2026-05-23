"""Tests for utility functions."""

import os

from app.utils import file_emoji, human_size, safe_path


class TestHumanSize:
    def test_bytes(self):
        assert human_size(0) == "0 B"
        assert human_size(512) == "512 B"
        assert human_size(1023) == "1023 B"

    def test_kilobytes(self):
        assert human_size(1024) == "1.0 KB"
        assert human_size(1536) == "1.5 KB"
        assert human_size(1048575) == "1024.0 KB"

    def test_megabytes(self):
        assert human_size(1048576) == "1.0 MB"
        assert human_size(2097152) == "2.0 MB"


class TestFileEmoji:
    def test_markdown(self):
        assert file_emoji("readme.md") == "📄"

    def test_image(self):
        assert file_emoji("photo.jpg") == "🖼"
        assert file_emoji("icon.png") == "🖼"

    def test_html(self):
        assert file_emoji("index.html") == "🌐"

    def test_cookbook_keyword(self):
        assert file_emoji("菜谱.md") == "🍳"

    def test_notes_keyword(self):
        assert file_emoji("学习笔记.md") == "📝"

    def test_unknown(self):
        assert file_emoji("random.bin") == "📄"


class TestSafePath:
    def test_normal_file(self, serve_dir):
        result = safe_path(serve_dir, "test.md")
        assert result == os.path.join(serve_dir, "test.md")

    def test_directory_traversal(self, serve_dir):
        result = safe_path(serve_dir, "../../etc/passwd")
        assert result is None

    def test_absolute_path_escape(self, serve_dir):
        result = safe_path(serve_dir, "/etc/passwd")
        assert result is None
