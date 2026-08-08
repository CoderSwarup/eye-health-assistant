"""Unit tests for exceptions."""

import pytest

from eye_health_assistant.core.exceptions import (
    CameraError,
    CameraNotAvailableError,
    CameraPermissionDeniedError,
    ContentNotFoundError,
    DatabaseConnectionError,
    DatabaseCorruptedError,
    EyeHealthError,
)


def test_eye_health_error_is_exception():
    """EyeHealthError should inherit from Exception."""
    assert issubclass(EyeHealthError, Exception)


def test_camera_error_hierarchy():
    """Camera errors should inherit from EyeHealthError."""
    assert issubclass(CameraError, EyeHealthError)
    assert issubclass(CameraPermissionDeniedError, CameraError)
    assert issubclass(CameraNotAvailableError, CameraError)


def test_database_error_hierarchy():
    """Database errors should inherit from EyeHealthError."""
    from eye_health_assistant.core.exceptions import DatabaseError

    assert issubclass(DatabaseError, EyeHealthError)
    assert issubclass(DatabaseConnectionError, DatabaseError)
    assert issubclass(DatabaseCorruptedError, DatabaseError)


def test_content_not_found_error():
    """ContentNotFoundError should be raisable."""
    with pytest.raises(ContentNotFoundError):
        raise ContentNotFoundError("not found")
