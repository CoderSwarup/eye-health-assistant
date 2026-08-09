"""System tray integration for background operation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon, QWidget

from eye_health_assistant.core.constants import APP_NAME

if TYPE_CHECKING:
    from eye_health_assistant.app.dependencies import Dependencies

logger = logging.getLogger(__name__)


class SystemTray(QSystemTrayIcon):
    """System tray icon with menu for background operation."""

    show_window = Signal()
    start_timer = Signal()
    start_smart_mode = Signal()
    stop_smart_mode = Signal()
    open_exercises = Signal()
    open_settings = Signal()
    quit_app = Signal()

    def __init__(
        self,
        deps: Dependencies,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.deps = deps
        self._monitoring_active = False

        self._setup_icon()
        self._setup_menu()
        self._connect_signals()

        self.activated.connect(self._on_activated)
        self.setToolTip(APP_NAME)

    def _setup_icon(self) -> None:
        """Set up the tray icon."""
        from PySide6.QtWidgets import QApplication

        # Use a simple icon - in production, use a proper icon file
        app = QApplication.instance()
        if app is not None and isinstance(app, QApplication):
            self.setIcon(app.style().standardIcon(
                app.style().StandardPixmap.SP_ComputerIcon
            ))

    def _setup_menu(self) -> None:
        """Set up the tray context menu."""
        menu = QMenu()

        # Show Dashboard
        show_action = QAction("Open Dashboard", menu)
        show_action.triggered.connect(self.show_window.emit)
        menu.addAction(show_action)

        menu.addSeparator()

        # Timer actions
        self._timer_action = QAction("Start Timer", menu)
        self._timer_action.triggered.connect(self.start_timer.emit)
        menu.addAction(self._timer_action)

        # Smart Mode actions
        self._smart_action = QAction("Start Smart Mode", menu)
        self._smart_action.triggered.connect(self._toggle_smart_mode)
        menu.addAction(self._smart_action)

        menu.addSeparator()

        # Exercises
        exercises_action = QAction("Open Exercises", menu)
        exercises_action.triggered.connect(self.open_exercises.emit)
        menu.addAction(exercises_action)

        # Settings
        settings_action = QAction("Settings", menu)
        settings_action.triggered.connect(self.open_settings.emit)
        menu.addAction(settings_action)

        menu.addSeparator()

        # Quit
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.quit_app.emit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def _connect_signals(self) -> None:
        """Connect to monitoring service signals."""
        if self.deps.monitoring_service is None:
            return

        service = self.deps.monitoring_service
        service.monitoring_started.connect(self._on_monitoring_started)
        service.monitoring_stopped.connect(self._on_monitoring_stopped)

    def _toggle_smart_mode(self) -> None:
        """Toggle smart mode monitoring."""
        if self._monitoring_active:
            self.stop_smart_mode.emit()
        else:
            self.start_smart_mode.emit()

    def _on_monitoring_started(self) -> None:
        """Handle monitoring started."""
        self._monitoring_active = True
        self._smart_action.setText("Stop Smart Mode")
        self.showMessage(
            APP_NAME,
            "Smart Mode monitoring started",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )

    def _on_monitoring_stopped(self) -> None:
        """Handle monitoring stopped."""
        self._monitoring_active = False
        self._smart_action.setText("Start Smart Mode")

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window.emit()
        elif reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Single click on some platforms
            pass

    def show_monitoring_status(self, active: bool) -> None:
        """Update the tray icon to reflect monitoring status."""
        if active:
            self.setToolTip(f"{APP_NAME} - Smart Mode Active")
        else:
            self.setToolTip(APP_NAME)
