"""Monitoring service — orchestrates smart camera monitoring."""

from __future__ import annotations

import logging
import time
from typing import Any

import numpy as np
from PySide6.QtCore import QObject, Signal

from eye_health_assistant.blink.detector import BlinkDetector
from eye_health_assistant.blink.metrics import MetricsAggregator
from eye_health_assistant.core.config import Config
from eye_health_assistant.infrastructure.camera.adapter import (
    CameraAdapter,
    OpenCVCamera,
)
from eye_health_assistant.monitoring.worker import MonitoringWorker
from eye_health_assistant.notifications.service import NotificationService

logger = logging.getLogger(__name__)


class MonitoringService(QObject):
    """High-level service for smart camera monitoring.

    Manages the lifecycle of the monitoring worker and coordinates
    between camera, CV, blink detection, metrics, and notifications.

    Signals:
        monitoring_started: ()
        monitoring_stopped: ()
        face_state_changed: (detected: bool)
        blink_rate_updated: (rate: float|None, total_blinks: int)
        eye_openness_updated: (openness: float|None)
        frame_available: (frame: np.ndarray) — processed frame with overlays
        error_occurred: (message: str)
    """

    monitoring_started = Signal()
    monitoring_stopped = Signal()
    face_state_changed = Signal(bool)
    blink_rate_updated = Signal(object, int)
    eye_openness_updated = Signal(object)
    frame_available = Signal(np.ndarray)
    face_landmarks_available = Signal(object)  # FaceLandmarks | None
    error_occurred = Signal(str)

    def __init__(
        self,
        config: Config,
        notification_service: NotificationService,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._notifications = notification_service
        self._worker: MonitoringWorker | None = None
        self._camera: CameraAdapter | None = None
        self._landmark_detector: Any = None
        self._blink_detector: BlinkDetector | None = None
        self._metrics: MetricsAggregator | None = None

        # Reminder state
        self._last_reminder_time: float | None = None
        self._low_blink_start: float | None = None

    @property
    def is_active(self) -> bool:
        return self._worker is not None and self._worker.is_running

    def start(
        self,
        device_index: int | None = None,
        sampling_fps: int | None = None,
    ) -> None:
        """Start smart monitoring.

        Args:
            device_index: Camera device index (defaults to config).
            sampling_fps: Frames per second to process (defaults to config).
        """
        if self.is_active:
            logger.warning("Monitoring already active")
            return

        idx = (
            device_index
            if device_index is not None
            else self._config.camera_device_index
        )
        fps = (
            sampling_fps
            if sampling_fps is not None
            else self._config.sampling_fps
        )

        # Create components
        self._camera = OpenCVCamera()

        # Use OpenCV detector (MediaPipe not available on Python 3.14)
        from eye_health_assistant.infrastructure.computer_vision import (
            opencv_detector as _cv_module,
        )
        self._landmark_detector = _cv_module.OpenCVFaceDetector()
        logger.info("Using OpenCV face detector")

        self._blink_detector = BlinkDetector(
            close_threshold=self._config.ear_close_threshold,
            open_threshold=self._config.ear_open_threshold,
            closed_threshold=self._config.ear_closed_threshold,
        )
        self._metrics = MetricsAggregator(
            window_seconds=self._config.rolling_window_minutes * 60.0,
            min_observation_seconds=float(self._config.min_observation_seconds),
        )

        # Create and configure worker
        self._worker = MonitoringWorker(
            camera=self._camera,
            detector=self._landmark_detector,
            blink_detector=self._blink_detector,
            metrics=self._metrics,
            device_index=idx,
            sampling_fps=fps,
        )

        # Connect signals
        self._worker.face_state_changed.connect(self.face_state_changed.emit)
        self._worker.blink_rate_updated.connect(self._on_blink_rate_updated)
        self._worker.eye_openness_updated.connect(self.eye_openness_updated.emit)
        self._worker.frame_available.connect(self.frame_available.emit)
        self._worker.face_landmarks_available.connect(self.face_landmarks_available.emit)
        self._worker.monitoring_error.connect(self.error_occurred.emit)
        self._worker.worker_stopped.connect(self._on_worker_stopped)

        # Start
        self._low_blink_start = None
        self._last_reminder_time = None
        self._worker.start()
        self.monitoring_started.emit()
        logger.info("Smart monitoring started (device=%d, fps=%d)", idx, fps)

    def stop(self) -> None:
        """Stop smart monitoring."""
        if self._worker is not None:
            self._worker.stop()
            self._worker.wait(3000)  # Wait up to 3 seconds
            if self._worker.isRunning():
                self._worker.terminate()
            self._worker = None

        self._camera = None
        self._landmark_detector = None
        self._blink_detector = None
        self._metrics = None
        self._low_blink_start = None

        logger.info("Smart monitoring stopped")

    def _on_blink_rate_updated(self, rate: float | None, total_blinks: int) -> None:
        """Handle blink rate update — check reminder policy."""
        self.blink_rate_updated.emit(rate, total_blinks)
        self._check_reminder_policy(rate)

    def _check_reminder_policy(self, rate: float | None) -> None:
        """Evaluate whether to send a low-blink reminder."""
        if not self._config.notifications_enabled:
            return

        now = time.monotonic()

        if rate is None:
            # Not enough data yet
            self._low_blink_start = None
            return

        if rate >= self._config.blink_rate_threshold:
            # Blink rate is healthy
            self._low_blink_start = None
            return

        # Rate is below threshold — track sustained duration
        if self._low_blink_start is None:
            self._low_blink_start = now
            return

        sustained_seconds = now - self._low_blink_start
        if sustained_seconds < self._config.sustained_low_blink_seconds:
            return

        # Check cooldown
        if self._last_reminder_time is not None:
            cooldown = self._config.min_notification_interval
            if (now - self._last_reminder_time) < cooldown:
                return

        # Send reminder
        self._notifications.notify_blink_reminder()
        self._last_reminder_time = now
        self._low_blink_start = now  # Reset for next reminder
        logger.info(
            "Low-blink reminder sent (rate=%.1f/min, sustained=%ds)",
            rate,
            sustained_seconds,
        )

    def _on_worker_stopped(self) -> None:
        """Handle worker stopped signal."""
        self.monitoring_stopped.emit()

    def get_available_cameras(self) -> list[int]:
        """Enumerate available camera devices."""
        cam = OpenCVCamera()
        return cam.enumerate_devices()
