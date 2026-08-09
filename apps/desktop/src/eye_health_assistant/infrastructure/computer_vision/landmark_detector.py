"""MediaPipe face mesh — eye landmark detection."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

# MediaPipe Face Mesh eye landmark indices (68-point model)
# Left eye landmarks
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
LEFT_EYE_LEFT = 33
LEFT_EYE_RIGHT = 133
LEFT_EYE_UPPER = 158
LEFT_EYE_LOWER = 153

# Right eye landmarks
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
RIGHT_EYE_LEFT = 362
RIGHT_EYE_RIGHT = 263
RIGHT_EYE_UPPER = 385
RIGHT_EYE_LOWER = 380


@dataclass
class EyeLandmarks:
    """Landmarks for a single eye."""

    top: np.ndarray
    bottom: np.ndarray
    left: np.ndarray
    right: np.ndarray
    upper: np.ndarray
    lower: np.ndarray


@dataclass
class FaceLandmarks:
    """Complete face landmark result."""

    left_eye: EyeLandmarks
    right_eye: EyeLandmarks
    face_detected: bool
    face_bbox: tuple[int, int, int, int] | None = None  # (x, y, w, h)


class LandmarkDetector:
    """MediaPipe Face Mesh-based eye landmark detector.

    Extracts eye landmarks from camera frames using MediaPipe's
    face mesh solution. All processing is local — no data leaves
    the device.
    """

    def __init__(self, max_num_faces: int = 1) -> None:
        self._max_num_faces = max_num_faces
        self._face_mesh: Any = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the MediaPipe face mesh model.

        Raises ImportError if mediapipe is not installed.
        """
        if self._initialized:
            return

        try:
            import mediapipe as mp
        except ImportError as err:
            raise ImportError(
                "MediaPipe is not installed. Install with: "
                "pip install mediapipe"
            ) from err

        self._face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=self._max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self._initialized = True
        logger.info("MediaPipe Face Mesh initialized")

    def detect(self, frame: np.ndarray) -> FaceLandmarks:
        """Detect face and extract eye landmarks from a BGR frame.

        Args:
            frame: Camera frame as BGR numpy array (H, W, 3).

        Returns:
            FaceLandmarks with face_detected=False if no face found.
        """
        if not self._initialized or self._face_mesh is None:
            raise RuntimeError(
                "LandmarkDetector not initialized. Call initialize() first."
            )

        # Convert BGR to RGB for MediaPipe
        rgb_frame = frame[:, :, ::-1].copy()

        results = self._face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return FaceLandmarks(
                left_eye=_empty_eye(),
                right_eye=_empty_eye(),
                face_detected=False,
            )

        # Use the first detected face
        landmarks = results.multi_face_landmarks[0]
        h, w = frame.shape[:2]

        left_eye = self._extract_eye(landmarks, w, h, LEFT_EYE_TOP, LEFT_EYE_BOTTOM,
                                     LEFT_EYE_LEFT, LEFT_EYE_RIGHT,
                                     LEFT_EYE_UPPER, LEFT_EYE_LOWER)
        right_eye = self._extract_eye(landmarks, w, h, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM,
                                      RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT,
                                      RIGHT_EYE_UPPER, RIGHT_EYE_LOWER)

        return FaceLandmarks(
            left_eye=left_eye,
            right_eye=right_eye,
            face_detected=True,
        )

    def _extract_eye(
        self,
        landmarks: Any,
        w: int,
        h: int,
        top_idx: int,
        bottom_idx: int,
        left_idx: int,
        right_idx: int,
        upper_idx: int,
        lower_idx: int,
    ) -> EyeLandmarks:
        """Extract eye landmarks as pixel coordinates."""
        lm = landmarks.landmark
        return EyeLandmarks(
            top=np.array([lm[top_idx].x * w, lm[top_idx].y * h]),
            bottom=np.array([lm[bottom_idx].x * w, lm[bottom_idx].y * h]),
            left=np.array([lm[left_idx].x * w, lm[left_idx].y * h]),
            right=np.array([lm[right_idx].x * w, lm[right_idx].y * h]),
            upper=np.array([lm[upper_idx].x * w, lm[upper_idx].y * h]),
            lower=np.array([lm[lower_idx].x * w, lm[lower_idx].y * h]),
        )

    def shutdown(self) -> None:
        """Release MediaPipe resources."""
        if self._face_mesh is not None:
            self._face_mesh.close()
            self._face_mesh = None
        self._initialized = False
        logger.info("LandmarkDetector shut down")


def _empty_eye() -> EyeLandmarks:
    """Return an empty EyeLandmarks with zero coordinates."""
    zero = np.zeros(2)
    return EyeLandmarks(
        top=zero, bottom=zero, left=zero, right=zero,
        upper=zero, lower=zero,
    )
