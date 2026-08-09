"""Camera infrastructure — webcam access and management."""

from eye_health_assistant.infrastructure.camera.adapter import (
    CameraAdapter,
    CameraNotAvailableError,
    CameraPermissionDeniedError,
    CameraReadError,
    OpenCVCamera,
)

__all__ = [
    "CameraAdapter",
    "CameraNotAvailableError",
    "CameraPermissionDeniedError",
    "CameraReadError",
    "OpenCVCamera",
]
