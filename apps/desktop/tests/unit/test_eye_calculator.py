"""Tests for eye aspect ratio calculation."""

from __future__ import annotations

import numpy as np

from eye_health_assistant.blink.calculator import compute_openness, eye_aspect_ratio
from eye_health_assistant.infrastructure.computer_vision.landmark_detector import (
    EyeLandmarks,
    FaceLandmarks,
    _empty_eye,
)


def _make_eye(
    top: float = 0.0,
    bottom: float = 10.0,
    left: float = 0.0,
    right: float = 10.0,
    upper: float = 2.0,
    lower: float = 8.0,
) -> EyeLandmarks:
    """Create an EyeLandmarks with given coordinates."""
    return EyeLandmarks(
        top=np.array([5.0, top]),
        bottom=np.array([5.0, bottom]),
        left=np.array([left, 5.0]),
        right=np.array([right, 5.0]),
        upper=np.array([3.0, upper]),
        lower=np.array([7.0, lower]),
    )


class TestEyeAspectRatio:
    """Test EAR calculation."""

    def test_open_eye(self) -> None:
        """An open eye should have a higher EAR."""
        eye = _make_eye(top=0.0, bottom=10.0, upper=2.0, lower=8.0)
        ear = eye_aspect_ratio(eye)
        assert ear > 0.0

    def test_closed_eye(self) -> None:
        """A closed eye should have a lower EAR."""
        eye = _make_eye(top=4.5, bottom=5.5, upper=4.8, lower=5.2)
        ear_closed = eye_aspect_ratio(eye)

        eye_open = _make_eye(top=0.0, bottom=10.0, upper=2.0, lower=8.0)
        ear_open = eye_aspect_ratio(eye_open)

        assert ear_closed < ear_open

    def test_zero_width_eye(self) -> None:
        """An eye with zero width should return 0."""
        eye = _make_eye(left=5.0, right=5.0)
        ear = eye_aspect_ratio(eye)
        assert ear == 0.0

    def test_symmetric_eye(self) -> None:
        """A symmetric eye should have consistent EAR."""
        eye = _make_eye(top=0.0, bottom=10.0, left=0.0, right=10.0,
                        upper=2.5, lower=7.5)
        ear = eye_aspect_ratio(eye)
        assert 0.0 < ear < 2.0


class TestComputeOpenness:
    """Test average openness calculation."""

    def test_no_face(self) -> None:
        """No face should return None."""
        face = FaceLandmarks(
            left_eye=_empty_eye(),
            right_eye=_empty_eye(),
            face_detected=False,
        )
        result = compute_openness(face)
        assert result is None

    def test_face_detected(self) -> None:
        """Detected face should return a float value."""
        left = _make_eye(top=0.0, bottom=10.0, upper=2.0, lower=8.0)
        right = _make_eye(top=0.0, bottom=10.0, upper=2.0, lower=8.0)
        face = FaceLandmarks(
            left_eye=left,
            right_eye=right,
            face_detected=True,
        )
        result = compute_openness(face)
        assert result is not None
        assert isinstance(result, float)
        assert result > 0.0

    def test_average_of_eyes(self) -> None:
        """Should return the average of left and right EAR."""
        left = _make_eye(top=0.0, bottom=10.0, upper=2.0, lower=8.0)
        right = _make_eye(top=0.0, bottom=10.0, upper=2.0, lower=8.0)
        face = FaceLandmarks(
            left_eye=left,
            right_eye=right,
            face_detected=True,
        )
        result = compute_openness(face)
        expected_left = eye_aspect_ratio(left)
        expected_right = eye_aspect_ratio(right)
        assert result is not None
        assert abs(result - (expected_left + expected_right) / 2.0) < 1e-6
