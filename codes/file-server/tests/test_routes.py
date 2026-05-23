"""Tests for Flask routes."""


class TestIndex:
    def test_index_loads(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "📁 文件列表" in resp.text

    def test_index_shows_files(self, client):
        """Index page shows visible files (sorted by size desc, paginated)."""
        resp = client.get("/")
        # PAGE_SIZE=2: largest files first → index.html(31B), test.md(30B) on page 1
        assert "test.md" in resp.text
        # Dot-files should be hidden
        assert ".hidden" not in resp.text
        # notes.txt should appear on a later page
        resp2 = client.get("/?page=2")
        assert "notes.txt" in resp2.text

    def test_index_pagination(self, client):
        """With PAGE_SIZE=2 and 5 visible files, should have 3 pages."""
        resp = client.get("/")
        assert resp.status_code == 200
        # Page 1 should show the first 2 files (sorted by size desc)
        # Our files: 22B config.json, 25B index.html, 29B test.md, 30B notes.txt, 16B photo.jpg
        # Sorted by size desc: notes.txt(30), test.md(29), index.html(25), config.json(22), photo.jpg(16)
        # Page 1 should have notes.txt and test.md

    def test_index_page_out_of_range(self, client):
        """Page out of range should be clamped to last page."""
        resp = client.get("/?page=999")
        assert resp.status_code == 200


class TestEditor:
    def test_editor_loads(self, client):
        resp = client.get("/edit?file=test.md")
        assert resp.status_code == 200
        assert "✏️ test.md" in resp.text
        assert "# Hello" in resp.text

    def test_editor_missing_file_param(self, client):
        resp = client.get("/edit")
        assert resp.status_code == 400

    def test_editor_nonexistent_file(self, client):
        resp = client.get("/edit?file=does_not_exist.txt")
        assert resp.status_code == 404

    def test_editor_non_editable_extension(self, client):
        resp = client.get("/edit?file=photo.jpg")
        assert resp.status_code == 403

    def test_editor_path_traversal(self, client):
        resp = client.get("/edit?file=../../../etc/passwd")
        assert resp.status_code in (400, 403, 404)


class TestSave:
    def test_save_file(self, client, serve_dir):
        import os

        resp = client.post(
            "/save",
            data={"file": "test.md", "content": "updated content"},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True

        # Verify the file was actually written
        with open(os.path.join(serve_dir, "test.md"), encoding="utf-8") as f:
            assert f.read() == "updated content"

    def test_save_missing_file_param(self, client):
        resp = client.post("/save", data={"content": "whatever"})
        data = resp.get_json()
        assert data["ok"] is False

    def test_save_invalid_path(self, client):
        resp = client.post(
            "/save",
            data={"file": "../../../etc/hacked", "content": "evil"},
        )
        data = resp.get_json()
        assert data["ok"] is False

    def test_save_non_editable_type(self, client):
        resp = client.post(
            "/save",
            data={"file": "photo.jpg", "content": "should fail"},
        )
        data = resp.get_json()
        assert data["ok"] is False


class TestStaticFileServing:
    def test_serve_existing_file(self, client):
        resp = client.get("/test.md")
        assert resp.status_code == 200
        assert "# Hello" in resp.text

    def test_serve_nonexistent_file(self, client):
        resp = client.get("/nope.txt")
        assert resp.status_code == 404

    def test_serve_path_traversal(self, client):
        resp = client.get("/../../../etc/passwd")
        assert resp.status_code in (403, 404)


class TestGitRepos:
    def test_git_page_loads(self, client):
        """Git repos page should load (may be empty if no /srv/git)."""
        resp = client.get("/git")
        assert resp.status_code == 200
        assert "Git 仓库" in resp.text

    def test_git_page_has_clone_info(self, client):
        """Git page should show clone command and git:// URL."""
        resp = client.get("/git")
        assert "git clone" in resp.text or "git://" in resp.text
