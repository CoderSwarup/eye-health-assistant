"""Camera infrastructure — webcam access and management."""

from eye_health_assistant.core.exceptions import (
    CameraNotAvailableError,
    CameraReadError,
)
from eye_health_assistant.infrastructure.camera.adapter import (
    CameraAdapter,
    OpenCVCamera,
)

__all__ = [
    "CameraAdapter",
    "CameraNotAvailableError",
    "CameraReadError",
    "OpenCVCamera",
]
