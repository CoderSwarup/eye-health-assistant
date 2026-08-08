"""Theme manager for applying and switching themes at runtime."""

from __future__ import annotations

import logging
from enum import Enum

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

from eye_health_assistant.ui.themes import (
    DARK,
    LIGHT,
    ThemeColors,
    generate_stylesheet,
)

logger = logging.getLogger(__name__)


class ThemeMode(Enum):
    """Theme mode options."""

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


def _is_system_dark() -> bool:
    """Detect if the system is using dark mode."""
    palette = QPalette()
    return bool(palette.window().color().lightness() < 128)


class ThemeManager(QObject):
    """Manages theme application and switching."""

    theme_changed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._current_mode = ThemeMode.SYSTEM
        self._current_theme = DARK

    @property
    def current_colors(self) -> ThemeColors:
        return self._current_theme

    @property
    def current_mode(self) -> ThemeMode:
        return self._current_mode

    def set_theme(self, mode: ThemeMode) -> None:
        """Apply a theme by mode."""
        self._current_mode = mode

        if mode == ThemeMode.SYSTEM:
            is_dark = _is_system_dark()
            self._current_theme = DARK if is_dark else LIGHT
        elif mode == ThemeMode.DARK:
            self._current_theme = DARK
        else:
            self._current_theme = LIGHT

        self._apply()
        self.theme_changed.emit(mode.value)
        logger.info("Theme changed to %s", mode.value)

    def _apply(self) -> None:
        """Apply the current theme to the application."""
        app = QApplication.instance()
        if app is None:
            return

        stylesheet = generate_stylesheet(self._current_theme)
        app.setStyleSheet(stylesheet)  # type: ignore[attr-defined]
