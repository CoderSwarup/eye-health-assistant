"""Statistics page — usage metrics and trends."""

from __future__ import annotations

from typing import cast

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

        self._title_label = QLabel(title)
        self._title_label.setObjectName("caption")
        layout.addWidget(self._title_label)

        self._value_label = QLabel(value)
        self._value_label.setObjectName("stat-number")
        layout.addWidget(self._value_label)

        self._subtitle_label = QLabel(subtitle)
        self._subtitle_label.setObjectName("caption")
        layout.addWidget(self._subtitle_label)

        layout.addStretch()

    def update_value(self, value: str, subtitle: str | None = None) -> None:
        """Update the displayed value and optional subtitle."""
        self._value_label.setText(value)
        if subtitle is not None:
            self._subtitle_label.setText(subtitle)


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
        self._summary_cards: list[StatCard] = []
        self._build_ui()
        self._load_statistics()

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

        # Summary metrics
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(16)
        self._summary_container = summary_layout
        layout.addLayout(summary_layout)

        # Trend cards
        self._trends_container = QVBoxLayout()
        self._trends_container.setSpacing(16)
        layout.addLayout(self._trends_container)

        export_btn = QPushButton("Export Data")
        export_btn.setObjectName("secondary-button")
        layout.addWidget(export_btn)

        layout.addStretch()

    def _load_statistics(self) -> None:
        """Load statistics from the database."""
        if self.deps.session_repository is None:
            self._show_placeholder_stats()
            return

        sessions = self.deps.session_repository.get_recent(limit=100)
        today_sessions = self.deps.session_repository.get_today()

        # Calculate summary metrics
        total_focus_time = sum(s.focus_duration for s in sessions)
        total_breaks = sum(s.completed_focus_sessions for s in sessions)
        total_sessions = len(sessions)

        total_hours = total_focus_time // 3600
        total_minutes = (total_focus_time % 3600) // 60
        time_str = f"{total_hours}h {total_minutes}m"

        today_focus = sum(s.focus_duration for s in today_sessions)
        today_hours = today_focus // 3600
        today_minutes = (today_focus % 3600) // 60
        today_str = f"{today_hours}h {today_minutes}m"

        # Get blink rate stats if available
        blink_stats = self._get_blink_statistics()

        # Summary cards
        summary_data = [
            ("Total Screen Time", time_str, "All time"),
            ("Today's Focus", today_str, "Today"),
            ("Breaks Completed", str(total_breaks), "All time"),
            ("Sessions Tracked", str(total_sessions), "All time"),
        ]

        if blink_stats:
            avg_rate = blink_stats.get("avg_rate")
            rate_str = f"{avg_rate:.1f}/min" if avg_rate else "--"
            sessions_count = blink_stats["total_sessions"]
            summary_data.append(
                ("Avg Blink Rate", rate_str, f"{sessions_count} sessions")
            )

        for title_text, value, subtitle in summary_data:
            card = StatCard(title_text, value, subtitle)
            self._summary_container.addWidget(card)
            self._summary_cards.append(card)

        # Trend cards
        trends = [
            ("Screen Time", "Complete more sessions to see screen time trends."),
            ("Breaks Taken", f"Completed {total_breaks} focus sessions total."),
            ("Session History", f"{total_sessions} sessions tracked total."),
        ]

        if blink_stats:
            avg_rate = blink_stats.get("avg_rate")
            if avg_rate:
                trends.append(
                    (
                        "Blink Rate",
                        f"Average blink rate: {avg_rate:.1f}/min across "
                        f"{blink_stats['total_sessions']} monitoring sessions.",
                    )
                )
            else:
                trends.append(
                    (
                        "Blink Rate",
                        "No blink data yet. Start Smart Mode to track blink rate.",
                    )
                )
        else:
            trends.append(
                (
                    "Blink Rate",
                    "No blink data yet. Enable Smart Mode to track blink rate.",
                )
            )

        for trend_title, msg in trends:
            trend_card = TrendCard(trend_title, msg)
            self._trends_container.addWidget(trend_card)

    def _get_blink_statistics(self) -> dict | None:
        """Get blink rate statistics from monitoring sessions."""
        if self.deps.monitoring_repository is None:
            return None

        try:
            sessions = self.deps.monitoring_repository.get_recent_sessions(limit=100)
            if not sessions:
                return None

            total_blinks = 0
            total_duration = 0.0
            rates: list[float] = []

            for session in sessions:
                if session.total_blinks is not None:
                    total_blinks += cast(int, session.total_blinks)
                if session.duration_seconds is not None:
                    total_duration += cast(float, session.duration_seconds)
                if (
                    session.average_blink_rate is not None
                    and session.valid_observation_seconds is not None
                    and cast(float, session.valid_observation_seconds) > 0
                ):
                    rates.append(cast(float, session.average_blink_rate))

            if not rates:
                return {
                    "total_sessions": len(sessions),
                    "total_blinks": total_blinks,
                    "avg_rate": None,
                }

            avg_rate = sum(rates) / len(rates)
            return {
                "total_sessions": len(sessions),
                "total_blinks": total_blinks,
                "avg_rate": avg_rate,
            }
        except Exception:
            return None

    def _show_placeholder_stats(self) -> None:
        """Show placeholder stats when no repository is available."""
        summary_data = [
            ("Total Screen Time", "0h 0m", "This week"),
            ("Avg Blink Rate", "--", "Enable Smart Mode"),
            ("Breaks Completed", "0", "This week"),
            ("Sessions Tracked", "0", "All time"),
        ]
        for title_text, value, subtitle in summary_data:
            card = StatCard(title_text, value, subtitle)
            self._summary_container.addWidget(card)

        trends = [
            ("Screen Time", "No data yet. Complete a session to see trends."),
            ("Blink Rate", "No data yet. Enable Smart Mode to track blink rate."),
            ("Breaks Taken", "No data yet. Start a timer to begin tracking breaks."),
        ]
        for trend_title, msg in trends:
            trend_card = TrendCard(trend_title, msg)
            self._trends_container.addWidget(trend_card)
