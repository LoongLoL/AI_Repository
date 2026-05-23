"""File server application configuration."""

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    """Application configuration loaded from environment variables."""

    serve_dir: str = field(
        default_factory=lambda: os.getenv(
            "FILESERVER_DIR", "/data/documents"
        )
    )
    port: int = field(
        default_factory=lambda: int(os.getenv("FILESERVER_PORT", "7890"))
    )
    host: str = field(
        default_factory=lambda: os.getenv("FILESERVER_HOST", "0.0.0.0")
    )
    page_size: int = field(
        default_factory=lambda: int(os.getenv("FILESERVER_PAGE_SIZE", "15"))
    )
    # File extensions that can be edited in the online editor
    editable_extensions: frozenset[str] = frozenset({
        ".md", ".txt", ".html", ".htm", ".css", ".js", ".json", ".xml",
    })
    # File extensions that browsers can display natively (view button shown)
    viewable_extensions: frozenset[str] = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "viewable_extensions",
            self.editable_extensions
            | frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}),
        )


config = Config()
