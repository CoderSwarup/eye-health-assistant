"""Statistics page — usage metrics and trends."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies

SUMMARY_METRICS = [
    ("Total Screen Time", "0h 0m", "This week"),
    ("Avg Blink Rate", "--", "Enable Smart Mode"),
    ("Breaks Completed", "0", "This week"),
    ("Sessions Tracked", "0", "All time"),
]

TREND_ITEMS = [
    ("Screen Time", "No data yet. Complete a session to see trends."),
    ("Blink Rate", "No data yet. Enable Smart Mode to track blink rate."),
    ("Breaks Taken", "No data yet. Start a timer to begin tracking breaks."),
]


class StatCard(QFrame):
    """Summary metric card."""

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("metric-card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("caption")
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setObjectName("stat-number")
        layout.addWidget(value_label)

        sub_label = QLabel(subtitle)
        sub_label.setObjectName("caption")
        layout.addWidget(sub_label)

        layout.addStretch()


class TrendCard(QFrame):
    """Trend section card."""

    def __init__(self, title: str, message: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("section-title")
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)

        msg_label = QLabel(message)
        msg_label.setObjectName("subtitle")
        msg_label.setWordWrap(True)
        layout.addWidget(msg_label)

        chart_placeholder = QLabel("Chart will appear here with data.")
        chart_placeholder.setObjectName("caption")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setMinimumHeight(60)
        layout.addWidget(chart_placeholder)


class StatisticsPage(QWidget):
    """Statistics and analytics page."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        header = QHBoxLayout()
        title = QLabel("Statistics")
        title.setObjectName("page-title")
        header.addWidget(title)
        header.addStretch()

        period_btns = QHBoxLayout()
        period_btns.setSpacing(10)
        for label in ["Daily", "Weekly", "Monthly"]:
            btn = QPushButton(label)
            btn.setObjectName("secondary-button")
            period_btns.addWidget(btn)
        header.addLayout(period_btns)

        layout.addLayout(header)

        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(16)
        for label, value, sub in SUMMARY_METRICS:
            stat_card = StatCard(label, value, sub)
            summary_layout.addWidget(stat_card)
        layout.addLayout(summary_layout)

        for trend_title, msg in TREND_ITEMS:
            trend_card = TrendCard(trend_title, msg)
            layout.addWidget(trend_card)

        export_btn = QPushButton("Export Data")
        export_btn.setObjectName("secondary-button")
        layout.addWidget(export_btn)

        layout.addStretch()
