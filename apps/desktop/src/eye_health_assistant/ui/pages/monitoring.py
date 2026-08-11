"""Monitoring page — live timer display, Smart Mode, and controls."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.domain.enums import TimerPhase
from eye_health_assistant.domain.models.timer_session import TimerSession
from eye_health_assistant.timer.controller import TimerController
from eye_health_assistant.ui.widgets.camera_preview import CameraPreview


class SmartModePanel(QFrame):
    """Smart Mode camera monitoring panel."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._is_active = False
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        title = QLabel("Smart Mode (Camera)")
        title.setObjectName("section-title")
        header.addWidget(title)
        header.addStretch()

        self._status_badge = QLabel("OFF")
        self._status_badge.setObjectName("caption")
        header.addWidget(self._status_badge)

        layout.addLayout(header)

        # Info row
        info = QLabel(
            "Track your blink rate and eye wellness using your webcam. "
            "Camera data is processed locally and never stored."
        )
        info.setObjectName("subtitle")
        info.setWordWrap(True)
        layout.addWidget(info)

        # Camera preview
        self._preview = CameraPreview()
        layout.addWidget(self._preview)

        # Metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(16)

        # Face detection
        face_layout = QVBoxLayout()
        face_layout.setSpacing(4)
        face_label = QLabel("Face Detection")
        face_label.setObjectName("caption")
        face_layout.addWidget(face_label)
        self._face_status = QLabel("--")
        self._face_status.setObjectName("stat-number")
        face_layout.addWidget(self._face_status)
        metrics_grid.addLayout(face_layout, 0, 0)

        # Blink rate
        blink_layout = QVBoxLayout()
        blink_layout.setSpacing(4)
        blink_label = QLabel("Blink Rate")
        blink_label.setObjectName("caption")
        blink_layout.addWidget(blink_label)
        self._blink_rate = QLabel("--")
        self._blink_rate.setObjectName("stat-number")
        blink_layout.addWidget(self._blink_rate)
        metrics_grid.addLayout(blink_layout, 0, 1)

        # Eye openness
        eye_layout = QVBoxLayout()
        eye_layout.setSpacing(4)
        eye_label = QLabel("Eye Openness")
        eye_label.setObjectName("caption")
        eye_layout.addWidget(eye_label)
        self._eye_openness = QLabel("--")
        self._eye_openness.setObjectName("stat-number")
        eye_layout.addWidget(self._eye_openness)
        metrics_grid.addLayout(eye_layout, 0, 2)

        # Total blinks
        total_layout = QVBoxLayout()
        total_layout.setSpacing(4)
        total_label = QLabel("Total Blinks")
        total_label.setObjectName("caption")
        total_layout.addWidget(total_label)
        self._total_blinks = QLabel("0")
        self._total_blinks.setObjectName("stat-number")
        total_layout.addWidget(self._total_blinks)
        metrics_grid.addLayout(total_layout, 1, 0)

        layout.addLayout(metrics_grid)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        self._start_btn = QPushButton("Start Smart Mode")
        self._start_btn.clicked.connect(self._toggle_monitoring)
        controls_layout.addWidget(self._start_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

    def _connect_signals(self) -> None:
        """Connect to monitoring service signals."""
        if self.deps.monitoring_service is None:
            return

        service = self.deps.monitoring_service
        service.monitoring_started.connect(self._on_started)
        service.monitoring_stopped.connect(self._on_stopped)
        service.face_state_changed.connect(self._on_face_changed)
        service.blink_rate_updated.connect(self._on_blink_rate)
        service.eye_openness_updated.connect(self._on_eye_openness)
        service.frame_available.connect(self._preview.update_frame)
        service.face_landmarks_available.connect(self._preview.set_face)
        service.error_occurred.connect(self._on_error)

    @Slot()
    def _toggle_monitoring(self) -> None:
        if self.deps.monitoring_service is None:
            return

        if self._is_active:
            self.deps.monitoring_service.stop()
        else:
            self.deps.monitoring_service.start()

    @Slot()
    def _on_started(self) -> None:
        self._is_active = True
        self._status_badge.setText("ACTIVE")
        self._status_badge.setStyleSheet("color: #4CAF50;")
        self._start_btn.setText("Stop Smart Mode")
        self._face_status.setText("Scanning...")
        self._blink_rate.setText("...")
        self._eye_openness.setText("...")
        self._total_blinks.setText("0")

    @Slot()
    def _on_stopped(self) -> None:
        self._is_active = False
        self._status_badge.setText("OFF")
        self._status_badge.setStyleSheet("")
        self._start_btn.setText("Start Smart Mode")
        self._face_status.setText("--")
        self._blink_rate.setText("--")
        self._eye_openness.setText("--")
        self._total_blinks.setText("0")
        self._preview.clear()

    @Slot(bool)
    def _on_face_changed(self, detected: bool) -> None:
        if detected:
            self._face_status.setText("Detected")
            self._face_status.setStyleSheet("color: #4CAF50;")
        else:
            self._face_status.setText("Not Found")
            self._face_status.setStyleSheet("color: #FF9800;")

    @Slot(object, int)
    def _on_blink_rate(self, rate: float | None, total: int) -> None:
        if rate is not None:
            self._blink_rate.setText(f"{rate:.1f}/min")
        else:
            self._blink_rate.setText("Measuring...")
        self._total_blinks.setText(str(total))

    @Slot(object)
    def _on_eye_openness(self, openness: float | None) -> None:
        if openness is not None:
            self._eye_openness.setText(f"{openness:.2f}")
        else:
            self._eye_openness.setText("N/A")

    @Slot(str)
    def _on_error(self, _message: str) -> None:
        self._status_badge.setText("ERROR")
        self._status_badge.setStyleSheet("color: #F44336;")
        self._start_btn.setText("Start Smart Mode")
        self._face_status.setText("Error")


class MonitoringPage(QWidget):
    """Live monitoring page with timer and Smart Mode."""

    navigate_to_settings = Signal()

    def __init__(
        self,
        deps: Dependencies,
        timer_controller: TimerController,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.deps = deps
        self._timer = timer_controller
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        # Page header
        header = QLabel("Live Monitoring")
        header.setObjectName("pageTitle")
        layout.addWidget(header)

        # Timer section
        timer_card = self._create_timer_card()
        layout.addWidget(timer_card)

        # Smart Mode section
        self._smart_panel = SmartModePanel(deps=self.deps)
        layout.addWidget(self._smart_panel)

        # Status card
        status_card = self._create_status_card()
        layout.addWidget(status_card)

        # Control buttons
        controls = self._create_controls()
        layout.addWidget(controls)

        layout.addStretch()

    def _create_timer_card(self) -> QFrame:
        """Create the main timer display card."""
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.Shape.NoFrame)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(12)

        # Phase label
        self._phase_label = QLabel("Ready")
        self._phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._phase_label.setObjectName("timerPhase")
        card_layout.addWidget(self._phase_label)

        # Time display
        self._time_label = QLabel("00:00")
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._time_label.setObjectName("timerDisplay")
        card_layout.addWidget(self._time_label)

        # Progress bar placeholder
        self._progress_label = QLabel("—")
        self._progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self._progress_label)

        return card

    def _create_status_card(self) -> QFrame:
        """Create status info card."""
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.Shape.NoFrame)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(24, 16, 24, 16)
        card_layout.setSpacing(24)

        # Session count
        self._session_label = QLabel("Sessions: 0")
        self._session_label.setObjectName("metricLabel")
        card_layout.addWidget(self._session_label)

        # Current duration
        self._duration_label = QLabel("Focus: 20 min")
        self._duration_label.setObjectName("metricLabel")
        card_layout.addWidget(self._duration_label)

        # Status
        self._status_label = QLabel("Idle")
        self._status_label.setObjectName("metricLabel")
        card_layout.addWidget(self._status_label)

        return card

    def _create_controls(self) -> QFrame:
        """Create timer control buttons."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.NoFrame)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self._start_btn = QPushButton("Start")
        self._start_btn.setObjectName("primaryButton")
        self._start_btn.clicked.connect(self._on_start)
        layout.addWidget(self._start_btn)

        self._pause_btn = QPushButton("Pause")
        self._pause_btn.setObjectName("secondaryButton")
        self._pause_btn.setEnabled(False)
        self._pause_btn.clicked.connect(self._on_pause)
        layout.addWidget(self._pause_btn)

        self._stop_btn = QPushButton("Stop")
        self._stop_btn.setObjectName("dangerButton")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._on_stop)
        layout.addWidget(self._stop_btn)

        return frame

    def _connect_signals(self) -> None:
        """Connect timer controller signals."""
        self._timer.session_started.connect(self._on_session_started)
        self._timer.session_updated.connect(self._on_session_updated)
        self._timer.session_paused.connect(self._on_session_paused)
        self._timer.session_resumed.connect(self._on_session_resumed)
        self._timer.session_ended.connect(self._on_session_ended)

    def _on_start(self) -> None:
        """Handle Start button click."""
        if self._timer.is_paused:
            self._timer.resume()
        else:
            self._timer.start(
                focus_duration=self._get_focus_duration(),
                break_duration=self._get_break_duration(),
            )

    def _on_pause(self) -> None:
        """Handle Pause button click."""
        self._timer.pause()

    def _on_stop(self) -> None:
        """Handle Stop button click."""
        self._timer.stop()

    def _on_session_started(self) -> None:
        """Update UI when session starts."""
        self._start_btn.setEnabled(False)
        self._pause_btn.setEnabled(True)
        self._stop_btn.setEnabled(True)
        self._update_display()

    def _on_session_updated(self, _session: TimerSession) -> None:
        """Update UI on timer tick."""
        self._update_display()

    def _on_session_paused(self) -> None:
        """Update UI when paused."""
        self._start_btn.setText("Resume")
        self._start_btn.setEnabled(True)
        self._pause_btn.setEnabled(False)
        self._status_label.setText("Paused")

    def _on_session_resumed(self) -> None:
        """Update UI when resumed."""
        self._start_btn.setEnabled(False)
        self._pause_btn.setEnabled(True)
        self._status_label.setText("Running")

    def _on_session_ended(self, _session: TimerSession) -> None:
        """Update UI when session ends."""
        self._reset_display()

    def _update_display(self) -> None:
        """Update timer display from current session."""
        session = self._timer.session
        if session is None:
            return

        # Phase
        if session.phase == TimerPhase.FOCUS:
            self._phase_label.setText("Focus Time")
            remaining = session.focus_remaining
        else:
            self._phase_label.setText("Break Time")
            remaining = session.break_remaining

        # Format time
        minutes = max(0, int(remaining)) // 60
        seconds = max(0, int(remaining)) % 60
        self._time_label.setText(f"{minutes:02d}:{seconds:02d}")

        # Progress
        progress = session.progress
        self._progress_label.setText(f"{progress:.0f}%")

        # Status info
        self._session_label.setText(
            f"Sessions: {session.completed_focus_sessions}"
        )
        self._duration_label.setText(
            f"Focus: {session.focus_duration // 60} min"
        )
        self._status_label.setText("Running" if session.is_active else "Idle")

    def _reset_display(self) -> None:
        """Reset display to idle state."""
        self._phase_label.setText("Ready")
        self._time_label.setText("00:00")
        self._progress_label.setText("—")
        self._session_label.setText("Sessions: 0")
        self._duration_label.setText("Focus: 20 min")
        self._status_label.setText("Idle")
        self._start_btn.setText("Start")
        self._start_btn.setEnabled(True)
        self._pause_btn.setEnabled(False)
        self._stop_btn.setEnabled(False)

    def _get_focus_duration(self) -> int:
        """Get focus duration from config."""
        session = self._timer._engine._session
        return session.focus_duration if session else 1200

    def _get_break_duration(self) -> int:
        """Get break duration from config."""
        session = self._timer._engine._session
        return session.break_duration if session else 20
