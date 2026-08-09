"""Application configuration with validation."""

from __future__ import annotations

import json
import logging
import platform
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


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


# Valid ranges for configuration values
_VALID_RANGES: dict[str, tuple[float, float]] = {
    "focus_duration": (60, 7200),  # 1 min to 2 hours
    "break_duration": (5, 600),  # 5 sec to 10 min
    "long_break_duration": (60, 1800),  # 1 min to 30 min
    "min_notification_interval": (30, 3600),  # 30 sec to 1 hour
    "sampling_fps": (1, 30),
    "min_observation_seconds": (5, 300),
    "sustained_low_blink_seconds": (10, 600),
    "blink_rate_threshold": (5.0, 30.0),
    "rolling_window_minutes": (1, 10),
    "ear_close_threshold": (0.1, 0.5),
    "ear_open_threshold": (0.1, 0.5),
    "ear_closed_threshold": (0.05, 0.3),
}

_VALID_THEMES = {"light", "dark", "system"}


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

    # Quiet hours
    quiet_hours_start: str = "22:00"
    quiet_hours_end: str = "07:00"

    # Sound
    notification_sound_enabled: bool = True

    # Startup behavior
    start_minimized: bool = False
    start_on_login: bool = False
    start_monitoring_auto: bool = False

    # Onboarding
    onboarding_completed: bool = False

    def __post_init__(self) -> None:
        if self.database_path is None:
            self.database_path = self.app_data_dir / "database" / "app.sqlite"
            self.database_path.parent.mkdir(parents=True, exist_ok=True)

    def validate(self) -> list[str]:
        """Validate configuration values. Returns list of error messages."""
        errors: list[str] = []

        if self.theme not in _VALID_THEMES:
            valid = sorted(_VALID_THEMES)
            errors.append(
                f"Invalid theme: {self.theme!r} (must be one of {valid})"
            )

        for field_name, (min_val, max_val) in _VALID_RANGES.items():
            value = getattr(self, field_name, None)
            if value is not None:
                try:
                    num_val = float(value)
                    if num_val < min_val or num_val > max_val:
                        errors.append(
                            f"{field_name}: {num_val} out of range"
                            f" [{min_val}, {max_val}]"
                        )
                except (TypeError, ValueError):
                    errors.append(f"{field_name}: invalid numeric value {value!r}")

        if not isinstance(self.notifications_enabled, bool):
            errors.append("notifications_enabled must be a boolean")
        if not isinstance(self.camera_enabled, bool):
            errors.append("camera_enabled must be a boolean")
        if not isinstance(self.camera_preview_enabled, bool):
            errors.append("camera_preview_enabled must be a boolean")

        return errors

    def apply_defaults_for_invalid(self) -> list[str]:
        """Apply safe defaults for invalid values. Returns list of fixes applied."""
        fixes: list[str] = []

        if self.theme not in _VALID_THEMES:
            fixes.append(f"theme: {self.theme!r} -> 'system'")
            self.theme = "system"

        for field_name, (min_val, max_val) in _VALID_RANGES.items():
            value = getattr(self, field_name, None)
            if value is not None:
                try:
                    num_val = float(value)
                    if num_val < min_val:
                        fixes.append(f"{field_name}: {num_val} -> {min_val}")
                        setattr(self, field_name, type(value)(min_val))
                    elif num_val > max_val:
                        fixes.append(f"{field_name}: {num_val} -> {max_val}")
                        setattr(self, field_name, type(value)(max_val))
                except (TypeError, ValueError):
                    default = Config().__dict__.get(field_name)
                    fixes.append(f"{field_name}: {value!r} -> {default!r}")
                    setattr(self, field_name, default)

        return fixes

    @classmethod
    def from_file(cls, path: Path) -> Config:
        """Load configuration from a JSON file with validation."""
        if not path.exists():
            logger.info("No config file found at %s, using defaults", path)
            return cls()

        try:
            with open(path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.warning("Invalid config file at %s: %s. Using defaults.", path, e)
            return cls()
        except OSError as e:
            logger.warning(
                "Cannot read config file at %s: %s. Using defaults.", path, e
            )
            return cls()

        # Filter to known fields only
        valid_fields = cls.__dataclass_fields__
        filtered = {k: v for k, v in data.items() if k in valid_fields}

        # Convert path strings back to Path objects
        if "database_path" in filtered and isinstance(filtered["database_path"], str):
            filtered["database_path"] = Path(filtered["database_path"])
        if "app_data_dir" in filtered and isinstance(filtered["app_data_dir"], str):
            filtered["app_data_dir"] = Path(filtered["app_data_dir"])

        try:
            config = cls(**filtered)
        except (TypeError, ValueError) as e:
            logger.warning("Invalid config values: %s. Using defaults.", e)
            return cls()

        # Validate and fix invalid values
        fixes = config.apply_defaults_for_invalid()
        if fixes:
            logger.info("Applied %d config fixes: %s", len(fixes), "; ".join(fixes))

        return config

    def save(self, path: Path) -> None:
        """Save configuration to a JSON file atomically."""
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(".tmp")
        try:
            with open(tmp_path, "w") as f:
                json.dump(
                    {
                        k: str(v) if isinstance(v, Path) else v
                        for k, v in self.__dict__.items()
                    },
                    f,
                    indent=2,
                )
            tmp_path.replace(path)
            logger.debug("Config saved to %s", path)
        except OSError as e:
            logger.error("Failed to save config to %s: %s", path, e)
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            raise
