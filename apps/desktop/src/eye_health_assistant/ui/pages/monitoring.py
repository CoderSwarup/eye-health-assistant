"""Monitoring page — live timer display and controls."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.domain.enums import TimerPhase
from eye_health_assistant.domain.models.timer_session import TimerSession
from eye_health_assistant.timer.controller import TimerController


class MonitoringPage(QWidget):
    """Live monitoring page with timer display and controls."""

    navigate_to_settings = Signal()

    def __init__(
        self,
        timer_controller: TimerController,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._timer = timer_controller
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Build the monitoring page layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        # Page header
        header = QLabel("Live Monitoring")
        header.setObjectName("pageTitle")
        layout.addWidget(header)

        # Timer display card
        timer_card = self._create_timer_card()
        layout.addWidget(timer_card)

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
