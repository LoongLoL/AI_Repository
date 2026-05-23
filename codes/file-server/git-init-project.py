#!/usr/bin/env python3
"""
Git project initializer — creates a local working repo and links it to the
central Git server (Docker-based).

Usage:
    python3 git-init-project.py /path/to/new/project [description]

This script:
  1. Runs `git init` in the project directory (if needed)
  2. Creates a bare repo at /root/.openclaw/workspace/projects/pyprojects/repos/
  3. Sets `git remote origin` to the Docker Git server
  4. Makes an initial commit and pushes
"""

import os
import subprocess
import sys
from pathlib import Path

REPOS_DIR = Path("/root/.openclaw/workspace/projects/pyprojects/repos")
GIT_HOST = "192.168.31.246"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    print(f"  → {' '.join(cmd)}")
    return subprocess.run(cmd, check=False, **kwargs)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    description = sys.argv[2] if len(sys.argv) > 2 else project_path.name
    repo_name = project_path.name

    # 1. Init local repo
    if not (project_path / ".git").is_dir():
        print(f"📁 Initializing: {project_path}")
        run(["git", "init", "-b", "master"], cwd=str(project_path))
    else:
        print(f"📁 Already a git repo: {project_path}")

    # Ensure there's something to commit
    gitignore = project_path / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(
            "__pycache__/\n*.py[cod]\n.venv/\n.pytest_cache/\n"
            "*.egg-info/\ndist/\nbuild/\n.env\n"
        )

    # 2. Create bare repo
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    bare_path = REPOS_DIR / f"{repo_name}.git"
    if not bare_path.is_dir():
        print(f"📦 Creating bare repo: {bare_path}")
        run(["git", "init", "--bare", str(bare_path)])
        (bare_path / "description").write_text(description)
        # git-daemon-export-ok for git:// protocol
        (bare_path / "git-daemon-export-ok").touch()
        print("   ✅ git-daemon-export-ok created")
    else:
        print(f"📦 Bare repo exists: {bare_path}")

    # 3. Set up remote (prefer git:// for simplicity)
    remote_url = f"git://{GIT_HOST}/{repo_name}.git"
    print(f"🔗 Remote origin → {remote_url}")
    result = run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(project_path), capture_output=True, text=True,
    )
    if result.returncode != 0:
        run(["git", "remote", "add", "origin", remote_url], cwd=str(project_path))
    else:
        run(["git", "remote", "set-url", "origin", remote_url], cwd=str(project_path))

    # 4. Commit and push
    print("📝 Staging files...")
    run(["git", "add", "-A"], cwd=str(project_path))

    status = run(
        ["git", "status", "--porcelain"],
        cwd=str(project_path), capture_output=True, text=True,
    )
    if status.stdout.strip():
        run(
            ["git", "commit", "-m", f"Initial commit: {description}"],
            cwd=str(project_path),
        )
        print("🚀 Pushing to central server...")
        run(
            ["git", "push", "-u", "origin", "master"],
            cwd=str(project_path),
        )
    else:
        print("  (nothing to commit)")

    print(f"\n✅ Done!")
    print(f"   git clone {remote_url}")
    print(f"   Web: http://{GIT_HOST}:7890/git")
    print(f"   HTTP clone: http://{GIT_HOST}:3000/{repo_name}.git")


if __name__ == "__main__":
    main()
