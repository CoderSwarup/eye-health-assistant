"""Application configuration."""

from __future__ import annotations

import json
import platform
from dataclasses import dataclass, field
from pathlib import Path


def get_app_data_dir() -> Path:
    """Get the platform-appropriate application data directory."""
    system = platform.system()
    if system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    elif system == "Windows":
        base = Path.home() / "AppData" / "Local"
    else:
        base = Path.home() / ".local" / "share"

    app_dir = base / "EyeHealthAssistant"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


@dataclass
class Config:
    """Application configuration.

    Precedence: Defaults < Config file < User settings.
    """

    app_data_dir: Path = field(default_factory=get_app_data_dir)
    database_path: Path | None = None
    log_level: str = "INFO"
    theme: str = "system"
    language: str = "en"

    def __post_init__(self) -> None:
        if self.database_path is None:
            self.database_path = self.app_data_dir / "database" / "app.sqlite"
            self.database_path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_file(cls, path: Path) -> Config:
        """Load configuration from a JSON file."""
        if not path.exists():
            return cls()
        with open(path) as f:
            data = json.load(f)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def save(self, path: Path) -> None:
        """Save configuration to a JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(
                {
                    k: str(v) if isinstance(v, Path) else v
                    for k, v in self.__dict__.items()
                },
                f,
                indent=2,
            )
