"""Test fixtures for the file server."""
import os
import tempfile

import pytest

from app import create_app


@pytest.fixture
def serve_dir():
    """Create a temporary directory with sample files for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some test files
        (tmpdir_path := tmpdir)

        # A markdown file
        with open(os.path.join(tmpdir_path, "test.md"), "w", encoding="utf-8") as f:
            f.write("# Hello\n\nThis is a test file.\n")

        # A text file
        with open(os.path.join(tmpdir_path, "notes.txt"), "w", encoding="utf-8") as f:
            f.write("line one\nline two\nline three\n")

        # An HTML file
        with open(os.path.join(tmpdir_path, "index.html"), "w", encoding="utf-8") as f:
            f.write("<html><body>test</body></html>\n")

        # A JSON file
        with open(os.path.join(tmpdir_path, "config.json"), "w", encoding="utf-8") as f:
            f.write('{"key": "value"}\n')

        # A non-editable file (image placeholder)
        with open(os.path.join(tmpdir_path, "photo.jpg"), "w", encoding="utf-8") as f:
            f.write("fake image data")

        # A dot-file (should be hidden from listing)
        with open(os.path.join(tmpdir_path, ".hidden"), "w", encoding="utf-8") as f:
            f.write("secret")

        yield tmpdir_path


@pytest.fixture
def app(serve_dir):
    """Create a Flask test app configured to use the temp directory."""
    app = create_app()
    app.config["SERVE_DIR"] = serve_dir
    app.config["PAGE_SIZE"] = 2  # small for pagination testing
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()
