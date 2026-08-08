"""Unit tests for application constants."""

from eye_health_assistant.core.constants import (
    APP_NAME,
    DEFAULT_BREAK_DURATION,
    DEFAULT_FOCUS_DURATION,
    VERSION,
)


def test_app_name():
    """App name should be set."""
    assert APP_NAME == "Eye Health Assistant"


def test_version_format():
    """Version should follow semver."""
    parts = VERSION.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)


def test_default_focus_duration():
    """Default focus duration should be 20 minutes in seconds."""
    assert DEFAULT_FOCUS_DURATION == 20 * 60


def test_default_break_duration():
    """Default break duration should be 20 seconds."""
    assert DEFAULT_BREAK_DURATION == 20
