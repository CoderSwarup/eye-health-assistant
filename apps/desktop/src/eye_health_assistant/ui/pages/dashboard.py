"""Dashboard page - the primary screen of the application."""

from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies


class MetricCard(QFrame):
    """A card displaying a single metric with label and value."""

    def __init__(
        self, title: str, value: str, subtitle: str = "", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("metric-card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._title_label = QLabel(title)
        self._title_label.setObjectName("caption")
        layout.addWidget(self._title_label)

        self._value_label = QLabel(value)
        self._value_label.setObjectName("stat-number")
        layout.addWidget(self._value_label)

        self._subtitle_label = QLabel(subtitle) if subtitle else None
        if self._subtitle_label:
            self._subtitle_label.setObjectName("caption")
            layout.addWidget(self._subtitle_label)

        layout.addStretch()

    def update_value(self, value: str, subtitle: str | None = None) -> None:
        """Update the displayed value and optional subtitle."""
        self._value_label.setText(value)
        if subtitle is not None and self._subtitle_label is not None:
            self._subtitle_label.setText(subtitle)


class DashboardPage(QWidget):
    """Main dashboard showing overview metrics, monitoring status, and quick actions."""

    navigate_to = Signal(str)

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._monitoring_active = False
        self._face_detected = False
        self._current_blink_rate: float | None = None
        self._build_ui()
        self._connect_signals()
        self._load_historical_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        # Header
        header = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("page-title")
        header.addWidget(title)
        header.addStretch()

        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("secondary-button")
        settings_btn.setAccessibleName("Open settings page")
        settings_btn.clicked.connect(lambda: self.navigate_to.emit("settings"))
        header.addWidget(settings_btn)

        layout.addLayout(header)

        # Overview metrics row
        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(16)

        self._screen_time_card = MetricCard("Screen Time", "0h 0m", "Today")
        self._blink_rate_card = MetricCard(
            "Estimated Blink Rate", "--", "Enable Smart Mode"
        )
        self._breaks_card = MetricCard("Breaks Completed", "0", "Today")
        self._status_card = MetricCard("Smart Mode", "Inactive", "Camera off")

        metrics_layout.addWidget(self._screen_time_card, 0, 0)
        metrics_layout.addWidget(self._blink_rate_card, 0, 1)
        metrics_layout.addWidget(self._breaks_card, 0, 2)
        metrics_layout.addWidget(self._status_card, 0, 3)

        layout.addLayout(metrics_layout)

        # Monitoring card
        monitoring_card = self._build_monitoring_card()
        layout.addWidget(monitoring_card)

        # Quick actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self._start_btn = QPushButton("Start Smart Mode")
        self._start_btn.setAccessibleName("Toggle smart camera monitoring")
        self._start_btn.clicked.connect(self._toggle_monitoring)
        actions_layout.addWidget(self._start_btn)

        timer_btn = QPushButton("Start Timer")
        timer_btn.setObjectName("secondary-button")
        timer_btn.setAccessibleName("Navigate to timer page")
        timer_btn.clicked.connect(lambda: self.navigate_to.emit("monitoring"))
        actions_layout.addWidget(timer_btn)

        exercises_btn = QPushButton("Exercises")
        exercises_btn.setObjectName("secondary-button")
        exercises_btn.setAccessibleName("Navigate to exercises page")
        exercises_btn.clicked.connect(lambda: self.navigate_to.emit("exercises"))
        actions_layout.addWidget(exercises_btn)

        eye_care_btn = QPushButton("Eye Care")
        eye_care_btn.setObjectName("secondary-button")
        eye_care_btn.setAccessibleName("Navigate to eye care articles")
        eye_care_btn.clicked.connect(lambda: self.navigate_to.emit("eye_care"))
        actions_layout.addWidget(eye_care_btn)

        stats_btn = QPushButton("Statistics")
        stats_btn.setObjectName("secondary-button")
        stats_btn.setAccessibleName("Navigate to statistics page")
        stats_btn.clicked.connect(lambda: self.navigate_to.emit("statistics"))
        actions_layout.addWidget(stats_btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Recent activity card
        activity_card = QFrame()
        activity_card.setObjectName("card")
        activity_card.setFrameShape(QFrame.Shape.NoFrame)
        activity_layout = QVBoxLayout(activity_card)
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(8)
        activity_title = QLabel("Recent Activity")
        activity_title.setObjectName("section-title")
        activity_layout.addWidget(activity_title)

        self._activity_placeholder = QLabel(
            "No recent activity. Start a monitoring session to begin tracking."
        )
        self._activity_placeholder.setObjectName("subtitle")
        self._activity_placeholder.setWordWrap(True)
        activity_layout.addWidget(self._activity_placeholder)

        layout.addWidget(activity_card)

        layout.addStretch()

    def _build_monitoring_card(self) -> QFrame:
        """Build the live monitoring status card."""
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.Shape.NoFrame)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        header_layout = QHBoxLayout()
        title = QLabel("Live Monitoring")
        title.setObjectName("section-title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self._monitoring_status = QLabel("Inactive")
        self._monitoring_status.setObjectName("caption")
        header_layout.addWidget(self._monitoring_status)

        layout.addLayout(header_layout)

        # Monitoring details
        details_layout = QHBoxLayout()
        details_layout.setSpacing(32)

        # Face detection
        face_layout = QVBoxLayout()
        face_layout.setSpacing(4)
        face_label = QLabel("Face Detection")
        face_label.setObjectName("caption")
        face_layout.addWidget(face_label)
        self._face_status = QLabel("--")
        self._face_status.setObjectName("subtitle")
        face_layout.addWidget(self._face_status)
        details_layout.addLayout(face_layout)

        # Blink rate
        blink_layout = QVBoxLayout()
        blink_layout.setSpacing(4)
        blink_label = QLabel("Blink Rate")
        blink_label.setObjectName("caption")
        blink_layout.addWidget(blink_label)
        self._blink_display = QLabel("--")
        self._blink_display.setObjectName("subtitle")
        blink_layout.addWidget(self._blink_display)
        details_layout.addLayout(blink_layout)

        # Camera status
        camera_layout = QVBoxLayout()
        camera_layout.setSpacing(4)
        camera_label = QLabel("Camera")
        camera_label.setObjectName("caption")
        camera_layout.addWidget(camera_label)
        self._camera_status = QLabel("Off")
        self._camera_status.setObjectName("subtitle")
        camera_layout.addWidget(self._camera_status)
        details_layout.addLayout(camera_layout)

        details_layout.addStretch()
        layout.addLayout(details_layout)

        # Control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        self._session_btn = QPushButton("Start Session")
        self._session_btn.setAccessibleName("Start or stop monitoring session")
        self._session_btn.clicked.connect(self._toggle_monitoring)
        controls_layout.addWidget(self._session_btn)

        skip_btn = QPushButton("Skip")
        skip_btn.setObjectName("secondary-button")
        skip_btn.setAccessibleName("Skip current monitoring cycle")
        controls_layout.addWidget(skip_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        return card

    def _connect_signals(self) -> None:
        """Connect to monitoring service signals."""
        if self.deps.monitoring_service is None:
            return

        service = self.deps.monitoring_service
        service.monitoring_started.connect(self._on_monitoring_started)
        service.monitoring_stopped.connect(self._on_monitoring_stopped)
        service.face_state_changed.connect(self._on_face_state_changed)
        service.blink_rate_updated.connect(self._on_blink_rate_updated)
        service.error_occurred.connect(self._on_error_occurred)

    def _load_historical_data(self) -> None:
        """Load today's historical data from analytics service."""
        if self.deps.analytics_service is None:
            return

        summary = self.deps.analytics_service.get_today_summary()

        # Update screen time
        self._screen_time_card.update_value(
            summary.focus_hours_display,
            "Today"
        )

        # Update breaks
        self._breaks_card.update_value(
            str(summary.focus_sessions_completed),
            "Today"
        )

        # Update blink rate if available
        blink_rate = summary.blink_rate_display
        if blink_rate != "--":
            self._blink_rate_card.update_value(blink_rate, "Today")

    @Slot()
    def _toggle_monitoring(self) -> None:
        """Start or stop smart monitoring."""
        if self.deps.monitoring_service is None:
            return

        if self._monitoring_active:
            self.deps.monitoring_service.stop()
        else:
            self.deps.monitoring_service.start()

    @Slot()
    def _on_monitoring_started(self) -> None:
        """Handle monitoring started."""
        self._monitoring_active = True
        self._monitoring_status.setText("Active")
        self._camera_status.setText("On")
        self._face_status.setText("Scanning...")
        self._blink_display.setText("--")
        self._session_btn.setText("Stop Session")
        self._start_btn.setText("Stop Smart Mode")
        self._status_card.update_value("Active", "Camera on")
        self._blink_rate_card.update_value("--", "Collecting data...")

    @Slot()
    def _on_monitoring_stopped(self) -> None:
        """Handle monitoring stopped."""
        self._monitoring_active = False
        self._monitoring_status.setText("Inactive")
        self._camera_status.setText("Off")
        self._face_status.setText("--")
        self._blink_display.setText("--")
        self._session_btn.setText("Start Session")
        self._start_btn.setText("Start Smart Mode")
        self._status_card.update_value("Inactive", "Camera off")
        self._blink_rate_card.update_value("--", "Enable Smart Mode")
        # Refresh historical data
        self._load_historical_data()

    @Slot(bool)
    def _on_face_state_changed(self, detected: bool) -> None:
        """Handle face detection state change."""
        self._face_detected = detected
        if detected:
            self._face_status.setText("Detected")
            self._face_status.setStyleSheet("color: #4CAF50;")
        else:
            self._face_status.setText("Not Found")
            self._face_status.setStyleSheet("color: #FF9800;")

    @Slot(object, int)
    def _on_blink_rate_updated(self, rate: float | None, total_blinks: int) -> None:
        """Handle blink rate update."""
        self._current_blink_rate = rate
        if rate is not None:
            rate_str = f"{rate:.1f}/min"
            self._blink_display.setText(rate_str)
            self._blink_rate_card.update_value(rate_str, f"{total_blinks} total blinks")
        else:
            self._blink_display.setText("Measuring...")
            self._blink_rate_card.update_value("...", "Collecting data...")

    @Slot(str)
    def _on_error_occurred(self, message: str) -> None:
        """Handle monitoring error."""
        self._monitoring_status.setText("Error")
        self._camera_status.setText("Error")
        self._status_card.update_value("Error", message[:30])
