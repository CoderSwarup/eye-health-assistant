"""Camera preview widget — displays live feed with detection overlays."""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from eye_health_assistant.infrastructure.computer_vision.landmark_detector import (
    FaceLandmarks,
)


def _draw_overlays(
    frame: np.ndarray,
    face: FaceLandmarks | None = None,
) -> np.ndarray:
    """Draw face bounding box and eye landmarks on the frame.

    Returns a copy of the frame with overlays drawn.
    """
    import cv2

    overlay = frame.copy()

    if face is not None and face.face_detected:
        # Draw face bounding box using actual bbox (stable, no jitter)
        if face.face_bbox is not None:
            fx, fy, fw, fh = face.face_bbox
            cv2.rectangle(overlay, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
            cv2.putText(
                overlay,
                "Face Detected",
                (fx, fy - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
            )

        # Draw eye landmarks
        for eye in [face.left_eye, face.right_eye]:
            points = np.array(
                [
                    eye.top.astype(int),
                    eye.bottom.astype(int),
                    eye.left.astype(int),
                    eye.right.astype(int),
                ],
                dtype=np.int32,
            )
            # Draw eye contour
            cv2.polylines(overlay, [points], True, (0, 255, 0), 1)
            # Draw center dot
            center = ((eye.left + eye.right) / 2).astype(int)
            cv2.circle(overlay, tuple(center), 3, (0, 255, 0), -1)
    else:
        # No face detected — show message
        cv2.putText(
            overlay,
            "No face detected",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 165, 255),  # Orange
            1,
        )

    return overlay


class CameraPreview(QFrame):
    """Live camera preview with face detection overlays.

    Displays the camera feed with drawn bounding boxes and eye landmarks
    so users can see how the scanning is working.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setMinimumHeight(240)
        self.setMaximumHeight(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel()
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setMinimumHeight(240)
        self._label.setText("Camera preview will appear here")
        self._label.setObjectName("subtitle")
        layout.addWidget(self._label)

        self._face: FaceLandmarks | None = None

    @Slot(np.ndarray)
    def update_frame(self, frame: np.ndarray) -> None:
        """Receive a camera frame and display it with overlays."""
        overlay = _draw_overlays(frame, self._face)

        # Convert BGR to RGB
        rgb = overlay[:, :, ::-1].copy()
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        q_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # Scale to fit label while maintaining aspect ratio
        scaled = pixmap.scaled(
            self._label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._label.setPixmap(scaled)

    def set_face(self, face: FaceLandmarks | None) -> None:
        """Update the current face landmarks for overlay drawing."""
        self._face = face

    def clear(self) -> None:
        """Clear the preview."""
        self._label.clear()
        self._label.setText("Camera preview will appear here")
        self._face = None
