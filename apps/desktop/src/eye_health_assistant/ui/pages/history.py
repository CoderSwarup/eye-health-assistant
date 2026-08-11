"""History page — session log with filtering and data management."""

from __future__ import annotations

from typing import cast

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.domain.models.timer_session import TimerSession


class SessionCard(QFrame):
    """Card for a single past session."""

    def __init__(
        self,
        session: TimerSession,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        mode_label = QLabel(session.mode.value.title())
        mode_label.setObjectName("section-title")
        header_row.addWidget(mode_label)
        header_row.addStretch()

        if session.started_at:
            date_str = session.started_at.strftime("%Y-%m-%d %H:%M")
        else:
            date_str = "Unknown"
        date_label = QLabel(date_str)
        date_label.setObjectName("caption")
        header_row.addWidget(date_label)

        info_layout.addLayout(header_row)

        detail_row = QHBoxLayout()
        detail_row.setSpacing(16)

        duration_min = session.focus_duration // 60
        duration_label = QLabel(f"Duration: {duration_min} min")
        duration_label.setObjectName("subtitle")
        detail_row.addWidget(duration_label)

        sessions_label = QLabel(
            f"Focus sessions: {session.completed_focus_sessions}"
        )
        sessions_label.setObjectName("caption")
        detail_row.addWidget(sessions_label)

        detail_row.addStretch()
        info_layout.addLayout(detail_row)

        layout.addLayout(info_layout, 1)


class MonitoringSessionCard(QFrame):
    """Card for a monitoring session."""

    def __init__(
        self,
        _session_id: str,
        _device_index: int,
        started_at: str,
        duration: float | None,
        total_blinks: int | None,
        avg_rate: float | None,
        status: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        mode_label = QLabel("Smart Mode")
        mode_label.setObjectName("section-title")
        header_row.addWidget(mode_label)
        header_row.addStretch()

        date_label = QLabel(started_at)
        date_label.setObjectName("caption")
        header_row.addWidget(date_label)

        info_layout.addLayout(header_row)

        detail_row = QHBoxLayout()
        detail_row.setSpacing(16)

        if duration is not None:
            duration_min = int(duration) // 60
            duration_sec = int(duration) % 60
            duration_label = QLabel(f"Duration: {duration_min}m {duration_sec}s")
        else:
            duration_label = QLabel("Duration: Active")
        duration_label.setObjectName("subtitle")
        detail_row.addWidget(duration_label)

        if total_blinks is not None:
            blinks_label = QLabel(f"Blinks: {total_blinks}")
            blinks_label.setObjectName("caption")
            detail_row.addWidget(blinks_label)

        if avg_rate is not None:
            rate_label = QLabel(f"Avg Rate: {avg_rate:.1f}/min")
            rate_label.setObjectName("caption")
            detail_row.addWidget(rate_label)

        status_label = QLabel(f"Status: {status.title()}")
        status_label.setObjectName("caption")
        detail_row.addWidget(status_label)

        detail_row.addStretch()
        info_layout.addLayout(detail_row)

        layout.addLayout(info_layout, 1)


class HistoryPage(QWidget):
    """Session history page with filtering."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._session_list_layout: QVBoxLayout | None = None
        self._empty_state: QFrame | None = None
        self._current_filter = "all"
        self._build_ui()
        self._load_sessions()

    def _build_ui(self) -> None:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        header = QHBoxLayout()
        title = QLabel("History")
        title.setObjectName("page-title")
        header.addWidget(title)
        header.addStretch()

        # Filter buttons
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        for label in ["All", "Timer", "Smart Mode"]:
            btn = QPushButton(label)
            btn.setObjectName("secondary-button")
            filter_type = label.lower().replace(" ", "_")
            btn.clicked.connect(
                lambda _checked, f=filter_type: self._on_filter(f)
            )
            filter_layout.addWidget(btn)
        header.addLayout(filter_layout)

        layout.addLayout(header)

        # Session list container
        self._session_list = QFrame()
        self._session_list.setObjectName("card")
        self._session_list.setFrameShape(QFrame.Shape.NoFrame)
        self._session_list_layout = QVBoxLayout(self._session_list)
        self._session_list_layout.setContentsMargins(0, 0, 0, 0)
        self._session_list_layout.setSpacing(8)
        layout.addWidget(self._session_list)

        # Empty state
        self._empty_state = QFrame()
        self._empty_state.setObjectName("card")
        self._empty_state.setFrameShape(QFrame.Shape.NoFrame)

        empty_layout = QVBoxLayout(self._empty_state)
        empty_layout.setContentsMargins(0, 0, 0, 0)
        empty_layout.setSpacing(8)

        empty_title = QLabel("No Sessions Yet")
        empty_title.setObjectName("section-title")
        empty_layout.addWidget(empty_title)

        empty_msg = QLabel(
            "Start a Timer or Smart Mode session to "
            "begin tracking your eye health history."
        )
        empty_msg.setObjectName("subtitle")
        empty_msg.setWordWrap(True)
        empty_layout.addWidget(empty_msg)

        layout.addWidget(self._empty_state)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _on_filter(self, filter_type: str) -> None:
        """Handle filter button click."""
        self._current_filter = filter_type
        self._load_sessions()

    def _load_sessions(self) -> None:
        """Load sessions from the database with current filter."""
        if self.deps.session_repository is None:
            return

        # Clear existing cards
        if self._session_list_layout:
            while self._session_list_layout.count():
                item = self._session_list_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)

        has_sessions = False

        # Timer sessions
        if self._current_filter in ("all", "timer"):
            sessions = self.deps.session_repository.get_recent(limit=50)
            for session in sessions:
                timer_card = SessionCard(session)
                if self._session_list_layout:
                    self._session_list_layout.addWidget(timer_card)
                has_sessions = True

        # Monitoring sessions
        if self._current_filter in ("all", "smart_mode"):
            monitoring_sessions = []
            if self.deps.monitoring_repository is not None:
                try:
                    monitoring_sessions = (
                        self.deps.monitoring_repository.get_recent_sessions(limit=20)
                    )
                except Exception:
                    monitoring_sessions = []

            for ms in monitoring_sessions:
                if ms.started_at:
                    started_at = ms.started_at.strftime("%Y-%m-%d %H:%M")
                else:
                    started_at = "Unknown"
                monitoring_card = MonitoringSessionCard(
                    _session_id=cast(str, ms.id),
                    _device_index=cast(int, ms.device_index),
                    started_at=started_at,
                    duration=cast(float | None, ms.duration_seconds),
                    total_blinks=cast(int | None, ms.total_blinks),
                    avg_rate=cast(float | None, ms.average_blink_rate),
                    status=cast(str, ms.status),
                )
                if self._session_list_layout:
                    self._session_list_layout.addWidget(monitoring_card)
                has_sessions = True

        if has_sessions:
            if self._session_list:
                self._session_list.show()
            if self._empty_state:
                self._empty_state.hide()
        else:
            if self._session_list:
                self._session_list.hide()
            if self._empty_state:
                self._empty_state.show()
