"""Custom exceptions for Eye Health Assistant."""

from __future__ import annotations


class EyeHealthError(Exception):
    """Base exception for all application errors."""


class CameraError(EyeHealthError):
    """Camera-related errors."""


class CameraPermissionDeniedError(CameraError):
    """Camera permission was denied by the user or system."""


class CameraNotAvailableError(CameraError):
    """No camera is available on the system."""


class CameraReadError(CameraError):
    """Failed to read a frame from the camera."""


class DatabaseError(EyeHealthError):
    """Database-related errors."""


class DatabaseConnectionError(DatabaseError):
    """Failed to connect to the database."""


class DatabaseCorruptedError(DatabaseError):
    """Database appears to be corrupted."""


class NotificationError(EyeHealthError):
    """Notification-related errors."""


class ContentError(EyeHealthError):
    """Content loading errors."""


class ContentNotFoundError(ContentError):
    """Requested content was not found."""


class SettingsError(EyeHealthError):
    """Settings-related errors."""


class PlatformError(EyeHealthError):
    """Platform-specific operation errors."""
