"""OpenCV fallback landmark detector — when MediaPipe is unavailable.

Uses YuNet for face detection and simple image analysis for blink detection.
YuNet's 5-point landmarks are unreliable on some platforms, so we use
the face bounding box + grayscale eye region analysis instead.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np

from eye_health_assistant.infrastructure.computer_vision.landmark_detector import (
    EyeLandmarks,
    FaceLandmarks,
)

logger = logging.getLogger(__name__)

_MODEL_DIR = Path(__file__).parent / "models"
_YUNET_MODEL = _MODEL_DIR / "face_detection_yunet.onnx"


def _empty_eye() -> EyeLandmarks:
    """Return empty EyeLandmarks with zero coordinates."""
    zero = np.zeros(2)
    return EyeLandmarks(
        top=zero, bottom=zero, left=zero, right=zero, upper=zero, lower=zero
    )


def _estimate_eye_landmarks(
    fx: float, fy: float, fw: float, fh: float,
    is_left_eye: bool,
) -> EyeLandmarks:
    """Estimate eye landmarks from face bounding box geometry.

    Uses face proportions determined from YuNet face detection data:
    - Eyes are at ~30-35% from top of face bbox
    - Left eye center at ~50% from left, right eye at ~85%
    - Face bbox includes ears/hair on left side
    """
    # Eye vertical position (32% from top)
    eye_y = fy + fh * 0.32

    # Eye horizontal position
    eye_x = fx + fw * 0.50 if is_left_eye else fx + fw * 0.85

    # Eye dimensions — based on face size
    eye_w = fw * 0.18
    eye_h = fh * 0.06

    half_w = eye_w / 2
    half_h = eye_h / 2

    return EyeLandmarks(
        left=np.array([eye_x - half_w, eye_y]),
        right=np.array([eye_x + half_w, eye_y]),
        top=np.array([eye_x, eye_y - half_h]),
        bottom=np.array([eye_x, eye_y + half_h]),
        upper=np.array([eye_x, eye_y - half_h * 1.4]),
        lower=np.array([eye_x, eye_y + half_h * 1.4]),
    )


def _analyze_eye_openness(
    frame: np.ndarray, eye_center: tuple[int, int], eye_size: int
) -> float:
    """Analyze eye openness using brightness comparison.

    Compares the center of the estimated eye region to the surrounding area.
    Returns 0.0 (closed) to 1.0 (open).

    Note: This is a rough estimate. For reliable blink detection, consider
    using MediaPipe Face Mesh (available on Python <3.14) which provides
    precise 468 face landmarks.
    """
    h, w = frame.shape[:2]
    cx, cy = eye_center

    # Extract eye region
    half = int(eye_size * 1.5)
    x1 = max(0, cx - half)
    y1 = max(0, cy - half)
    x2 = min(w, cx + half)
    y2 = min(h, cy + half)

    if x2 - x1 < 10 or y2 - y1 < 10:
        return 0.5

    roi = frame[y1:y2, x1:x2]
    if len(roi.shape) == 3:
        gray = np.mean(roi, axis=2).astype(np.float32)
    else:
        gray = roi.astype(np.float32)

    roi_h, _roi_w = gray.shape

    # Split into top (eyebrow/forehead), middle (eye), bottom (cheek)
    h1 = roi_h // 3
    h2 = 2 * roi_h // 3
    top = gray[:h1, :]
    mid = gray[h1:h2, :]
    bot = gray[h2:, :]

    # Reference: average of top and bottom (skin areas)
    ref = (float(np.mean(top)) + float(np.mean(bot))) / 2.0
    eye_val = float(np.mean(mid))

    if ref < 5:
        return 0.5

    # Darkness: how much darker is the eye area vs skin
    darkness = (ref - eye_val) / ref

    # Also check for the darkest row in the middle section
    # (should correspond to the pupil/eyelash line when open)
    row_mins = np.min(mid, axis=1)
    darkest_row = float(np.min(row_mins))
    darkest_darkness = (ref - darkest_row) / ref

    # Combine: overall darkness + darkest point
    score = 0.5 * darkness + 0.5 * darkest_darkness

    # Normalize: typical range is 0.0 to 0.2
    return max(0.0, min(1.0, score / 0.2))


class OpenCVFaceDetector:
    """Fallback face detector using OpenCV's YuNet DNN model.

    Uses YuNet for face detection and simple image analysis for eye openness.
    Provides face bounding box detection and estimated eye landmarks.
    """

    def __init__(self) -> None:
        self._cv2: Any = None
        self._detector: Any = None
        self._input_size: tuple[int, int] = (320, 320)
        self._initialized = False
        self._warmup_frames = 0

    def initialize(self) -> None:
        """Load YuNet face detection model."""
        if not _YUNET_MODEL.exists():
            raise FileNotFoundError(
                f"YuNet model not found at {_YUNET_MODEL}. "
                "Download from https://github.com/opencv/opencv_zoo"
            )

        try:
            import cv2

            self._cv2 = cv2
            self._detector = cv2.FaceDetectorYN_create(  # type: ignore[attr-defined]
                str(_YUNET_MODEL),
                "",
                self._input_size,
                0.2,  # Score threshold
                0.4,  # NMS threshold
                5000,  # top_k
            )

            self._initialized = True
            self._warmup_frames = 0
            logger.info("OpenCV YuNet detector initialized")

        except Exception as e:
            logger.error("Failed to initialize OpenCV detector: %s", e)
            raise

    def detect(self, frame: np.ndarray) -> FaceLandmarks:
        """Detect face and estimate eye landmarks.

        Uses YuNet for face bounding box only, then estimates eye positions
        using standard face proportions.
        """
        if not self._initialized or self._detector is None or self._cv2 is None:
            raise RuntimeError("Detector not initialized. Call initialize() first.")

        h, w = frame.shape[:2]
        self._detector.setInputSize((w, h))
        retval, faces = self._detector.detect(frame)

        # Camera warmup: skip first few frames for stability
        self._warmup_frames += 1

        if not retval or faces is None or len(faces) == 0:
            return FaceLandmarks(
                left_eye=_empty_eye(),
                right_eye=_empty_eye(),
                face_detected=False,
            )

        # Use the face with highest score
        # YuNet output: [x, y, w, h, score, ...landmarks]
        # Score is at index4 but may be >1 on some platforms
        best_face = max(faces, key=lambda f: f[4])
        fx, fy, fw, fh = best_face[:4]

        # Sanity check: face bbox should be within frame
        if fw < 20 or fh < 20 or fx < -fw or fy < -fh or fx > w or fy > h:
            return FaceLandmarks(
                left_eye=_empty_eye(),
                right_eye=_empty_eye(),
                face_detected=False,
            )

        # Estimate eye landmarks from face geometry
        left_eye = _estimate_eye_landmarks(fx, fy, fw, fh, is_left_eye=True)
        right_eye = _estimate_eye_landmarks(fx, fy, fw, fh, is_left_eye=False)

        logger.debug(
            "Face detected at (%.0f, %.0f, %.0f, %.0f)",
            fx, fy, fw, fh,
        )

        return FaceLandmarks(
            left_eye=left_eye,
            right_eye=right_eye,
            face_detected=True,
            face_bbox=(int(fx), int(fy), int(fw), int(fh)),
        )

    def analyze_eye_openness(
        self, frame: np.ndarray, face: FaceLandmarks
    ) -> float | None:
        """Analyze actual eye openness from the camera frame.

        Uses grayscale image analysis of the eye region to determine
        if eyes are open or closed. Returns value 0.0-1.0 or None.
        """
        if not face.face_detected:
            return None

        left_center = (
            int((face.left_eye.left[0] + face.left_eye.right[0]) / 2),
            int((face.left_eye.top[1] + face.left_eye.bottom[1]) / 2),
        )
        right_center = (
            int((face.right_eye.left[0] + face.right_eye.right[0]) / 2),
            int((face.right_eye.top[1] + face.right_eye.bottom[1]) / 2),
        )

        # Eye region size
        left_width = np.linalg.norm(
            face.left_eye.right - face.left_eye.left
        )
        eye_size = max(12, int(left_width / 2))

        left_openness = _analyze_eye_openness(frame, left_center, eye_size)
        right_openness = _analyze_eye_openness(frame, right_center, eye_size)

        return (left_openness + right_openness) / 2.0

    def shutdown(self) -> None:
        """Release resources."""
        self._cv2 = None
        self._detector = None
        self._initialized = False
        logger.info("OpenCV YuNet detector shut down")
