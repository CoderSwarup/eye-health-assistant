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

    # Timer defaults
    focus_duration: int = 1200  # 20 minutes in seconds
    break_duration: int = 20  # 20 seconds
    long_break_duration: int = 300  # 5 minutes in seconds

    # Notifications
    notifications_enabled: bool = True
    min_notification_interval: int = 300  # 5 minutes in seconds

    # Smart mode (camera)
    camera_enabled: bool = False
    camera_device_index: int = 0
    camera_preview_enabled: bool = True
    smart_mode_default: bool = False
    sampling_fps: int = 10  # frames per second to process
    min_observation_seconds: int = 30
    sustained_low_blink_seconds: int = 120  # 2 minutes before reminder
    score_algorithm_version: str = "1.0"

    # Blink detection thresholds
    blink_rate_threshold: float = 15.0  # blinks per minute
    rolling_window_minutes: int = 3
    ear_close_threshold: float = 0.22
    ear_open_threshold: float = 0.28
    ear_closed_threshold: float = 0.20

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
