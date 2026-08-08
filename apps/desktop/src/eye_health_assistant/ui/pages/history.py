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


class SessionCard(QFrame):
    """Card for a single past session."""

    def __init__(
        self,
        session_type: str,
        duration: str,
        date: str,
        details: str,
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

        type_label = QLabel(session_type)
        type_label.setObjectName("section-title")
        header_row.addWidget(type_label)
        header_row.addStretch()

        date_label = QLabel(date)
        date_label.setObjectName("caption")
        header_row.addWidget(date_label)

        info_layout.addLayout(header_row)

        detail_row = QHBoxLayout()
        detail_row.setSpacing(16)

        duration_label = QLabel(f"Duration: {duration}")
        duration_label.setObjectName("subtitle")
        detail_row.addWidget(duration_label)

        details_label = QLabel(details)
        details_label.setObjectName("caption")
        detail_row.addWidget(details_label)

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
        self._build_ui()

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

        empty_state = QFrame()
        empty_state.setObjectName("card")
        empty_state.setFrameShape(QFrame.Shape.NoFrame)

        empty_layout = QVBoxLayout(empty_state)
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

        layout.addWidget(empty_state)

        layout.addStretch()
