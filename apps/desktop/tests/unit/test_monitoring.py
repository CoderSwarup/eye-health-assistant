"""Tests for monitoring service and worker (mocked)."""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import numpy as np

from eye_health_assistant.blink.detector import BlinkDetector
from eye_health_assistant.blink.metrics import MetricsAggregator
from eye_health_assistant.core.config import Config
from eye_health_assistant.infrastructure.computer_vision.landmark_detector import (
    EyeLandmarks,
    FaceLandmarks,
    _empty_eye,
)
from eye_health_assistant.monitoring.service import MonitoringService
from eye_health_assistant.monitoring.worker import MonitoringWorker
from eye_health_assistant.notifications.service import NotificationService


def _make_face(openness: float = 0.35) -> FaceLandmarks:
    """Create face landmarks where EAR scales linearly with openness."""
    eye = EyeLandmarks(
        top=np.array([5.0, -openness * 5.0]),
        bottom=np.array([5.0, openness * 5.0]),
        left=np.array([0.0, 5.0]),
        right=np.array([10.0, 5.0]),
        upper=np.array([5.0, -openness * 3.0]),
        lower=np.array([5.0, openness * 3.0]),
    )
    return FaceLandmarks(left_eye=eye, right_eye=eye, face_detected=True)


def _no_face() -> FaceLandmarks:
    return FaceLandmarks(
        left_eye=_empty_eye(), right_eye=_empty_eye(), face_detected=False
    )


class MockCameraImpl:
    def __init__(self) -> None:
        self._opened = False

    def open(self, _device_index: int = 0) -> None:
        self._opened = True

    def read(self) -> np.ndarray:
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def is_opened(self) -> bool:
        return self._opened

    def close(self) -> None:
        self._opened = False

    def enumerate_devices(self) -> list[int]:
        return [0]


class MockDetectorImpl:
    def __init__(self) -> None:
        self._initialized = False

    def initialize(self) -> None:
        self._initialized = True

    def detect(self, _frame: np.ndarray) -> FaceLandmarks:
        return _no_face()

    def shutdown(self) -> None:
        self._initialized = False


class MockDetectorWithFace:
    def __init__(self) -> None:
        self._initialized = False

    def initialize(self) -> None:
        self._initialized = True

    def detect(self, _frame: np.ndarray) -> FaceLandmarks:
        return _make_face(0.35)

    def shutdown(self) -> None:
        self._initialized = False


class TestMonitoringWorker:
    """Test worker logic by calling _process_frame directly."""

    def test_process_frame_no_face(self) -> None:
        """Processing a frame with no face should update face state."""
        worker = MonitoringWorker(
            camera=MockCameraImpl(),  # type: ignore[arg-type]
            detector=MockDetectorImpl(),  # type: ignore[arg-type]
            blink_detector=BlinkDetector(),
            metrics=MetricsAggregator(),
        )

        face_states: list[bool] = []
        worker.face_state_changed.connect(lambda s: face_states.append(s))

        worker._running = True
        worker._process_frame()

        assert False in face_states

    def test_process_frame_with_face(self) -> None:
        """Processing a frame with face should emit face detected."""
        worker = MonitoringWorker(
            camera=MockCameraImpl(),  # type: ignore[arg-type]
            detector=MockDetectorWithFace(),  # type: ignore[arg-type]
            blink_detector=BlinkDetector(),
            metrics=MetricsAggregator(window_seconds=5.0, min_observation_seconds=0.1),
        )

        face_states: list[bool] = []
        worker.face_state_changed.connect(lambda s: face_states.append(s))

        worker._running = True
        worker._process_frame()

        assert True in face_states

    def test_process_frame_blink_detection(self) -> None:
        """Time-based estimation should produce blinks when face is detected."""
        worker = MonitoringWorker(
            camera=MockCameraImpl(),  # type: ignore[arg-type]
            detector=MockDetectorWithFace(),  # type: ignore[arg-type]
            blink_detector=BlinkDetector(),
            metrics=MetricsAggregator(window_seconds=5.0, min_observation_seconds=0.1),
        )

        worker._running = True
        worker._last_sample_time = time.monotonic() - 0.1
        # Set next_blink_time to now so next frame triggers a blink
        worker._next_blink_time = time.monotonic() - 0.01

        worker._process_frame()

        metrics = worker._metrics.get_metrics()
        assert metrics.total_blinks > 0

    def test_worker_stop_sets_flag(self) -> None:
        """stop() should set _running to False."""
        worker = MonitoringWorker(
            camera=MockCameraImpl(),  # type: ignore[arg-type]
            detector=MockDetectorImpl(),  # type: ignore[arg-type]
            blink_detector=BlinkDetector(),
            metrics=MetricsAggregator(),
        )
        worker._running = True
        worker.stop()
        assert not worker._running


class TestMonitoringService:
    """Test the monitoring service orchestration."""

    def setup_method(self) -> None:
        self.config = Config()
        self.config.notifications_enabled = True
        self.config.blink_rate_threshold = 15.0
        self.config.sustained_low_blink_seconds = 1
        self.config.min_notification_interval = 1
        self.notifications = NotificationService(self.config)

    def test_not_active_initially(self) -> None:
        service = MonitoringService(
            config=self.config,
            notification_service=self.notifications,
        )
        assert not service.is_active

    @patch("eye_health_assistant.infrastructure.camera.adapter.OpenCVCamera")
    def test_start_stop(self, _mock_cam: MagicMock) -> None:
        """Test starting and stopping the monitoring service."""
        # Mock the camera
        _mock_cam.return_value.open.return_value = None
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        _mock_cam.return_value.read.return_value = frame

        service = MonitoringService(
            config=self.config,
            notification_service=self.notifications,
        )
        service.start()
        time.sleep(0.1)
        assert service.is_active
        service.stop()
        assert not service.is_active

    @patch("eye_health_assistant.monitoring.service.OpenCVCamera")
    def test_get_available_cameras(self, mock_cam: MagicMock) -> None:
        mock_cam.return_value.enumerate_devices.return_value = [0, 1]
        service = MonitoringService(
            config=self.config,
            notification_service=self.notifications,
        )
        cameras = service.get_available_cameras()
        assert cameras == [0, 1]

    def test_reminder_policy_no_data(self) -> None:
        """No reminder if no blink rate data."""
        service = MonitoringService(
            config=self.config,
            notification_service=self.notifications,
        )
        service._last_reminder_time = None
        service._check_reminder_policy(None)
        assert service._last_reminder_time is None

    def test_reminder_policy_healthy_rate(self) -> None:
        """No reminder if blink rate is healthy."""
        service = MonitoringService(
            config=self.config,
            notification_service=self.notifications,
        )
        service._check_reminder_policy(20.0)
        assert service._last_reminder_time is None

    def test_reminder_policy_sustained_low(self) -> None:
        """Reminder sent after sustained low blink rate."""
        self.config.sustained_low_blink_seconds = 0
        self.config.min_notification_interval = 0
        service = MonitoringService(
            config=self.config,
            notification_service=self.notifications,
        )
        service._low_blink_start = 0.0  # Simulate sustained low rate
        service._last_reminder_time = None

        with patch.object(service._notifications, "notify_blink_reminder") as mock:
            service._check_reminder_policy(10.0)
            mock.assert_called_once()
