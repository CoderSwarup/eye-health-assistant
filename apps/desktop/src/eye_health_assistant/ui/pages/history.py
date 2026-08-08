"""History page — session log and past activity."""

from __future__ import annotations

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

        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("danger-button")
        layout.addWidget(delete_btn)


class HistoryPage(QWidget):
    """Session history page."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._session_list_layout: QVBoxLayout | None = None
        self._empty_state: QFrame | None = None
        self._build_ui()
        self._load_sessions()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        header = QHBoxLayout()
        title = QLabel("History")
        title.setObjectName("page-title")
        header.addWidget(title)
        header.addStretch()

        clear_btn = QPushButton("Clear All")
        clear_btn.setObjectName("danger-button")
        header.addWidget(clear_btn)

        layout.addLayout(header)

        subtitle = QLabel("Past monitoring sessions and activity log.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

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

    def _load_sessions(self) -> None:
        """Load sessions from the database."""
        if self.deps.session_repository is None:
            return

        sessions = self.deps.session_repository.get_recent(limit=50)

        # Clear existing cards
        if self._session_list_layout:
            while self._session_list_layout.count():
                item = self._session_list_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)

        if sessions:
            if self._session_list:
                self._session_list.show()
            if self._empty_state:
                self._empty_state.hide()

            if self._session_list_layout:
                for session in sessions:
                    card = SessionCard(session)
                    self._session_list_layout.addWidget(card)
        else:
            if self._session_list:
                self._session_list.hide()
            if self._empty_state:
                self._empty_state.show()
