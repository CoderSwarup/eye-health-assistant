"""Monitoring worker — background thread for camera processing."""

from __future__ import annotations

import logging
import random
import time
from typing import Any

import numpy as np
from PySide6.QtCore import QObject, QThread, Signal

from eye_health_assistant.blink.detector import BlinkDetector
from eye_health_assistant.blink.metrics import MetricsAggregator
from eye_health_assistant.infrastructure.camera.adapter import (
    CameraAdapter,
    CameraReadError,
)

logger = logging.getLogger(__name__)

# Number of frames to skip after camera open for auto-exposure/warmup
_CAMERA_WARMUP_FRAMES = 15

# Research-based blink rate during screen use (blinks per minute)
_SCREEN_BLINK_RATE = 6.0


class MonitoringWorker(QThread):
    """Background worker for smart camera monitoring.

    Runs the camera → face detection → estimated blink rate pipeline
    in a separate thread. Uses time-based blink estimation because
    image-based detection requires precise eye landmarks (MediaPipe)
    which is not available on Python 3.14.

    Signals:
        face_state_changed: (face_detected: bool)
        blink_rate_updated: (rate: float | None, total_blinks: int)
        eye_openness_updated: (openness: float | None)
        frame_available: (frame: np.ndarray) — processed frame with overlays
        face_landmarks_available: (FaceLandmarks | None)
        monitoring_error: (message: str)
        worker_stopped: ()
    """

    face_state_changed = Signal(bool)
    blink_rate_updated = Signal(object, int)  # float|None, int
    eye_openness_updated = Signal(object)  # float|None
    frame_available = Signal(np.ndarray)
    face_landmarks_available = Signal(object)  # FaceLandmarks | None
    monitoring_error = Signal(str)
    worker_stopped = Signal()

    def __init__(
        self,
        camera: CameraAdapter,
        detector: Any,
        blink_detector: BlinkDetector,
        metrics: MetricsAggregator,
        device_index: int = 0,
        sampling_fps: int = 10,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._camera = camera
        self._landmark_detector = detector
        self._blink_detector = blink_detector
        self._metrics = metrics
        self._device_index = device_index
        self._sampling_interval = 1.0 / max(1, sampling_fps)
        self._running = False

        # Tracking state
        self._last_face_detected: bool | None = None
        self._valid_observation_seconds = 0.0
        self._last_sample_time: float | None = None
        self._blinks_since_sample = 0

        # Time-based blink estimation
        self._next_blink_time: float | None = None
        self._session_start: float | None = None
        self._last_face_time: float | None = None

    @property
    def is_running(self) -> bool:
        return self._running

    def _schedule_next_blink(self) -> None:
        """Schedule the next estimated blink using exponential distribution."""
        # Exponential inter-blink intervals (realistic blink timing)
        mean_interval = 60.0 / _SCREEN_BLINK_RATE  # seconds between blinks
        interval = random.expovariate(1.0 / mean_interval)
        self._next_blink_time = time.monotonic() + interval

    def run(self) -> None:
        """Main worker loop — runs in a separate thread."""
        self._running = True
        self._blink_detector.reset()
        self._metrics.start_session()
        self._last_sample_time = None
        self._valid_observation_seconds = 0.0
        self._blinks_since_sample = 0
        self._session_start = time.monotonic()
        self._schedule_next_blink()

        try:
            self._camera.open(self._device_index)
            logger.info("Camera opened successfully at index %d", self._device_index)
        except Exception as e:
            logger.error("Failed to open camera: %s", e)
            self.monitoring_error.emit(f"Could not open camera: {e}")
            self._running = False
            self.worker_stopped.emit()
            return

        # Camera warmup: read and discard frames for auto-exposure
        logger.info("Warming up camera (%d frames)...", _CAMERA_WARMUP_FRAMES)
        for _ in range(_CAMERA_WARMUP_FRAMES):
            try:
                self._camera.read()
            except Exception:
                break
        logger.info("Camera warmup complete")

        try:
            self._landmark_detector.initialize()
            logger.info("Landmark detector initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize landmark detector: %s", e)
            self.monitoring_error.emit(f"Could not initialize face detection: {e}")
            self._camera.close()
            self._running = False
            self.worker_stopped.emit()
            return

        logger.info("Monitoring worker started")

        try:
            while self._running:
                loop_start = time.monotonic()

                try:
                    self._process_frame()
                except CameraReadError:
                    self.monitoring_error.emit("Camera disconnected")
                    break
                except Exception as e:
                    logger.exception("Error processing frame: %s", e)
                    # Continue processing — don't crash on one bad frame

                # Maintain target sampling rate
                elapsed = time.monotonic() - loop_start
                sleep_time = self._sampling_interval - elapsed
                if sleep_time > 0:
                    self.msleep(int(sleep_time * 1000))

        finally:
            self._cleanup()

    def _process_frame(self) -> None:
        """Process a single camera frame."""
        frame = self._camera.read()
        face = self._landmark_detector.detect(frame)

        # Update face state (emit on first frame too)
        if (
            self._last_face_detected is None
            or face.face_detected != self._last_face_detected
        ):
            self._last_face_detected = face.face_detected
            self.face_state_changed.emit(face.face_detected)

        # Emit face landmarks for overlay drawing
        self.face_landmarks_available.emit(face if face.face_detected else None)

        # Eye openness: not available without MediaPipe landmarks
        self.eye_openness_updated.emit(None)

        # Time-based blink estimation
        now = time.monotonic()
        if face.face_detected:
            self._last_face_time = now

        # Count blinks if face was seen recently (2 second grace period)
        # This prevents counter from stopping when face detection briefly drops
        face_recent = (
            self._last_face_time is not None
            and (now - self._last_face_time) < 2.0
        )
        blink_due = (
            face_recent
            and self._next_blink_time is not None
            and now >= self._next_blink_time
        )
        if blink_due:
            self._blinks_since_sample += 1
            self._schedule_next_blink()
            logger.debug("Estimated blink (total: %d)", self._blinks_since_sample)

        # Track observation time and emit metrics periodically
        if self._last_sample_time is not None:
            dt = now - self._last_sample_time
            if face.face_detected:
                self._valid_observation_seconds += dt
            # Add sample with accumulated blinks since last sample
            self._metrics.add_sample(
                blink_count=self._blinks_since_sample,
                valid_observation_seconds=dt if face.face_detected else 0.0,
            )
            self._blinks_since_sample = 0
        self._last_sample_time = now

        # Emit updated metrics
        metrics = self._metrics.get_metrics()
        self.blink_rate_updated.emit(
            metrics.estimated_blink_rate,
            metrics.total_blinks,
        )

        # Emit frame with detection overlays for camera preview
        self.frame_available.emit(frame)

    def _cleanup(self) -> None:
        """Release all resources."""
        logger.info("Monitoring worker cleaning up")
        self._camera.close()
        self._landmark_detector.shutdown()
        self._running = False
        self.worker_stopped.emit()
        logger.info("Monitoring worker stopped")

    def stop(self) -> None:
        """Request the worker to stop."""
        self._running = False
