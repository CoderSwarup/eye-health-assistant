"""OpenCV camera adapter — abstraction over webcam access."""

from __future__ import annotations

import logging
from typing import Any, Protocol, cast

import numpy as np

logger = logging.getLogger(__name__)


class CameraError(Exception):
    """Camera operation failed."""


class CameraPermissionDeniedError(CameraError):
    """Camera permission was denied by the user or OS."""


class CameraNotAvailableError(CameraError):
    """No camera is available on this system."""


class CameraReadError(CameraError):
    """Failed to read a frame from the camera."""


class CameraAdapter(Protocol):
    """Protocol for camera backends."""

    def open(self, device_index: int = 0) -> None:
        """Open the camera."""
        ...

    def read(self) -> np.ndarray:
        """Read a frame. Raises CameraReadError on failure."""
        ...

    def is_opened(self) -> bool:
        """Whether the camera is currently open."""
        ...

    def close(self) -> None:
        """Release the camera."""
        ...

    def enumerate_devices(self) -> list[int]:
        """Return available camera device indices."""
        ...


class OpenCVCamera:
    """OpenCV-based camera adapter.

    Wraps cv2.VideoCapture with proper error handling and resource
    management. Never allows a camera failure to crash the application.
    """

    def __init__(self) -> None:
        self._cap: Any = None
        self._opened = False

    def open(self, device_index: int = 0) -> None:
        """Open the camera at the given device index."""
        try:
            import cv2
        except ImportError as err:
            raise CameraNotAvailableError(
                "OpenCV is not installed. Install with: pip install opencv-python"
            ) from err

        if self._opened:
            self.close()

        self._cap = cv2.VideoCapture(device_index)
        if not self._cap.isOpened():
            self._cap = None
            raise CameraNotAvailableError(
                f"Could not open camera at index {device_index}. "
                "Check that a camera is connected and not in use."
            )

        self._opened = True
        logger.info("Camera opened at index %d", device_index)

    def read(self) -> np.ndarray:
        """Read a frame from the camera.

        Returns the frame as a BGR numpy array.
        Raises CameraReadError if the frame cannot be read.
        """
        if not self._opened or self._cap is None:
            raise CameraReadError("Camera is not open")

        ret, frame = self._cap.read()
        if not ret or frame is None:
            raise CameraReadError("Failed to read frame from camera")

        return cast(np.ndarray, frame)

    def is_opened(self) -> bool:
        """Whether the camera is currently open."""
        return self._opened

    def close(self) -> None:
        """Release the camera resources."""
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                logger.exception("Error releasing camera")
            self._cap = None
        self._opened = False
        logger.info("Camera closed")

    def enumerate_devices(self) -> list[int]:
        """Probe for available camera device indices.

        Returns a list of indices that responded. This may not be exhaustive
        on all platforms.
        """
        try:
            import cv2
        except ImportError:
            return []

        available: list[int] = []
        for idx in range(5):
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                available.append(idx)
                cap.release()
        return available
