"""Dashboard page - the primary screen of the application."""

from __future__ import annotations

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

        title_label = QLabel(title)
        title_label.setObjectName("caption")
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setObjectName("stat-number")
        layout.addWidget(value_label)

        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setObjectName("caption")
            layout.addWidget(sub_label)

        layout.addStretch()


class DashboardPage(QWidget):
    """Main dashboard showing overview metrics, monitoring status, and quick actions."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._build_ui()

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
        header.addWidget(settings_btn)

        layout.addLayout(header)

        # Overview metrics row
        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(16)

        metrics = [
            ("Screen Time", "0h 0m", "Today"),
            ("Estimated Blink Rate", "--", "Enable Smart Mode"),
            ("Breaks Completed", "0", "Today"),
            ("Monitoring", "Inactive", "Start a session"),
        ]

        for i, (title_text, value, subtitle) in enumerate(metrics):
            card = MetricCard(title_text, value, subtitle)
            metrics_layout.addWidget(card, i // 2, i % 2)

        layout.addLayout(metrics_layout)

        # Monitoring card
        monitoring_card = self._build_monitoring_card()
        layout.addWidget(monitoring_card)

        # Quick actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        actions = [
            ("Start Timer", True),
            ("Start Smart Mode", True),
            ("Exercises", False),
            ("Eye Care", False),
            ("Statistics", False),
        ]

        for label, primary in actions:
            btn = QPushButton(label)
            if not primary:
                btn.setObjectName("secondary-button")
            actions_layout.addWidget(btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Recent activity placeholder
        activity_card = QFrame()
        activity_card.setObjectName("card")
        activity_card.setFrameShape(QFrame.Shape.NoFrame)
        activity_layout = QVBoxLayout(activity_card)
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(8)
        activity_title = QLabel("Recent Activity")
        activity_title.setObjectName("section-title")
        activity_layout.addWidget(activity_title)

        activity_placeholder = QLabel(
            "No recent activity. Start a monitoring session to begin tracking."
        )
        activity_placeholder.setObjectName("subtitle")
        activity_placeholder.setWordWrap(True)
        activity_layout.addWidget(activity_placeholder)

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

        status = QLabel("Inactive")
        status.setObjectName("caption")
        header_layout.addWidget(status)

        layout.addLayout(header_layout)

        # Monitoring details
        details_layout = QHBoxLayout()
        details_layout.setSpacing(32)

        details = [
            ("Mode", "Timer"),
            ("Duration", "0m"),
            ("Next Break", "--"),
        ]

        for label, value in details:
            detail_layout = QVBoxLayout()
            detail_layout.setSpacing(4)

            lbl = QLabel(label)
            lbl.setObjectName("caption")
            detail_layout.addWidget(lbl)

            val = QLabel(value)
            val.setObjectName("subtitle")
            detail_layout.addWidget(val)

            details_layout.addLayout(detail_layout)

        details_layout.addStretch()
        layout.addLayout(details_layout)

        # Control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        start_btn = QPushButton("Start Session")
        controls_layout.addWidget(start_btn)

        skip_btn = QPushButton("Skip")
        skip_btn.setObjectName("secondary-button")
        controls_layout.addWidget(skip_btn)

        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        return card
