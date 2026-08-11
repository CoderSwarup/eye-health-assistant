"""Reusable UI state components: loading, empty, and error states."""

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


class LoadingState(QWidget):
    """Centered loading spinner placeholder."""

    def __init__(
        self, message: str = "Loading...", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 60, 0, 60)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        spinner = QLabel("...")
        spinner.setObjectName("page-title")
        spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(spinner)

        label = QLabel(message)
        label.setObjectName("subtitle")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)


class EmptyState(QWidget):
    """Centered empty state with icon, message, and optional action button."""

    action_clicked = Signal()

    def __init__(
        self,
        message: str = "Nothing here yet.",
        description: str = "",
        action_label: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 60, 0, 60)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("--")
        icon.setObjectName("page-title")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        layout.addSpacing(16)

        msg = QLabel(message)
        msg.setObjectName("section-title")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)

        if description:
            desc = QLabel(description)
            desc.setObjectName("subtitle")
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc.setWordWrap(True)
            layout.addWidget(desc)

        if action_label:
            layout.addSpacing(16)
            btn = QPushButton(action_label)
            btn.setAccessibleName(action_label)
            btn.clicked.connect(self.action_clicked.emit)
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()
            btn_layout.addWidget(btn)
            btn_layout.addStretch()
            layout.addLayout(btn_layout)


class ErrorState(QWidget):
    """Centered error state with message and retry button."""

    retry_clicked = Signal()

    def __init__(
        self,
        message: str = "Something went wrong.",
        description: str = "",
        retry_label: str = "Retry",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 60, 0, 60)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("!")
        icon.setObjectName("page-title")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        layout.addSpacing(16)

        msg = QLabel(message)
        msg.setObjectName("section-title")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)

        if description:
            desc = QLabel(description)
            desc.setObjectName("subtitle")
            desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc.setWordWrap(True)
            layout.addWidget(desc)

        layout.addSpacing(16)

        btn = QPushButton(retry_label)
        btn.setAccessibleName(retry_label)
        btn.clicked.connect(self.retry_clicked.emit)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)


class DatabaseErrorBanner(QFrame):
    """Warning banner shown when database is unavailable."""

    def __init__(
        self, error_message: str = "", parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        icon = QLabel("!")
        icon.setObjectName("section-title")
        layout.addWidget(icon)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title = QLabel("Database Unavailable")
        title.setObjectName("section-title")
        text_layout.addWidget(title)

        description = QLabel(
            "History and statistics features are temporarily disabled."
        )
        description.setObjectName("subtitle")
        text_layout.addWidget(description)

        if error_message:
            detail = QLabel(error_message)
            detail.setObjectName("caption")
            detail.setWordWrap(True)
            text_layout.addWidget(detail)

        layout.addLayout(text_layout, 1)
