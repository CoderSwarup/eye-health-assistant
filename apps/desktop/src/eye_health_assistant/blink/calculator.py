"""Eye openness calculator — geometric eye aspect ratio (EAR)."""

from __future__ import annotations

import numpy as np

from eye_health_assistant.infrastructure.computer_vision.landmark_detector import (
    EyeLandmarks,
    FaceLandmarks,
)


def eye_aspect_ratio(eye: EyeLandmarks) -> float:
    """Calculate the Eye Aspect Ratio (EAR) for a single eye.

    EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)

    Where p1..p6 are the 6 eye landmarks ordered as:
    p1=left, p2=upper, p3=top, p4=right, p5=lower, p6=bottom

    A higher EAR means the eye is more open.
    Typical values: ~0.2-0.3 (closed) to ~0.3-0.4 (open).

    Args:
        eye: EyeLandmarks with the 6 key points.

    Returns:
        The eye aspect ratio as a float.
    """
    # Vertical distances
    v1 = np.linalg.norm(eye.top - eye.bottom)
    v2 = np.linalg.norm(eye.upper - eye.lower)

    # Horizontal distance
    h = np.linalg.norm(eye.left - eye.right)

    # Avoid division by zero
    if h < 1e-6:
        return 0.0

    return float((v1 + v2) / (2.0 * h))


def compute_openness(face: FaceLandmarks) -> float | None:
    """Compute average eye openness for a detected face.

    Returns the average EAR of both eyes, or None if no face is detected.

    Args:
        face: FaceLandmarks from the landmark detector.

    Returns:
        Average EAR float, or None if no face.
    """
    if not face.face_detected:
        return None

    left_ear = eye_aspect_ratio(face.left_eye)
    right_ear = eye_aspect_ratio(face.right_eye)

    return (left_ear + right_ear) / 2.0
