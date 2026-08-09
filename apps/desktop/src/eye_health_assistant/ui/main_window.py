"""Main application window with sidebar navigation."""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.ui.pages.dashboard import DashboardPage
from eye_health_assistant.ui.pages.exercises import ExercisesPage
from eye_health_assistant.ui.pages.eye_care import EyeCarePage
from eye_health_assistant.ui.pages.history import HistoryPage
from eye_health_assistant.ui.pages.monitoring import MonitoringPage
from eye_health_assistant.ui.pages.settings import SettingsPage
from eye_health_assistant.ui.pages.statistics import StatisticsPage
from eye_health_assistant.ui.themes.manager import ThemeManager, ThemeMode

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Primary application window with sidebar navigation and content area."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self.theme_manager = ThemeManager(self)

        self.setWindowTitle("Eye Health Assistant")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)

        # Apply default theme
        self.theme_manager.set_theme(ThemeMode.DARK)

        # Build UI
        self._build_ui()
        self._navigate_to("dashboard")

    def _build_ui(self) -> None:
        """Build the main UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = self._build_sidebar()
        main_layout.addWidget(self.sidebar)

        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Page container
        self.page_container = QWidget()
        self.page_layout = QVBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidget(self.page_container)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        content_layout.addWidget(scroll)

        main_layout.addWidget(content_widget, 1)

        # Pages registry
        self.pages: dict[str, QWidget] = {}
        self._create_pages()

    def _build_sidebar(self) -> QWidget:
        """Build the sidebar navigation."""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 16)
        sidebar_layout.setSpacing(4)

        # App title
        from PySide6.QtWidgets import QLabel

        title = QLabel("Eye Health")
        title.setObjectName("section-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(16)

        # Navigation items
        nav_items = [
            ("dashboard", "Dashboard"),
            ("monitoring", "Live Monitoring"),
            ("exercises", "Exercises"),
            ("eye_care", "Eye Care"),
            ("statistics", "Statistics"),
            ("history", "History"),
            ("settings", "Settings"),
        ]

        self.nav_buttons: dict[str, QPushButton] = {}
        for page_id, label in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav-button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _checked, pid=page_id: self._navigate_to(pid))
            self.nav_buttons[page_id] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Theme toggle
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.setObjectName("secondary-button")
        theme_btn.clicked.connect(self._toggle_theme)
        sidebar_layout.addWidget(theme_btn)

        return sidebar

    def _create_pages(self) -> None:
        """Create all page instances."""
        self.pages["dashboard"] = DashboardPage(deps=self.deps)
        dashboard = self.pages["dashboard"]
        dashboard.navigate_to.connect(self._navigate_to)  # type: ignore[attr-defined]

        if self.deps.timer_controller:
            monitoring = MonitoringPage(
                deps=self.deps,
                timer_controller=self.deps.timer_controller,
            )
            self.pages["monitoring"] = monitoring

        self.pages["exercises"] = ExercisesPage(deps=self.deps)
        self.pages["eye_care"] = EyeCarePage(deps=self.deps)
        self.pages["statistics"] = StatisticsPage(deps=self.deps)
        self.pages["history"] = HistoryPage(deps=self.deps)
        self.pages["settings"] = SettingsPage(deps=self.deps)

    def _navigate_to(self, page_id: str) -> None:
        """Navigate to a page by ID."""
        # Update nav buttons
        for btn_id, btn in self.nav_buttons.items():
            btn.setChecked(btn_id == page_id)

        # Show page
        page = self.pages.get(page_id)
        if page is None:
            # Placeholder for pages not yet implemented
            from PySide6.QtWidgets import QLabel

            placeholder = QLabel(f"{page_id.title()} — Coming Soon")
            placeholder.setObjectName("page-title")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            page = placeholder

        # Clear current page
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        self.page_layout.addWidget(page)

    @Slot()
    def _toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        current = self.theme_manager.current_mode
        if current == ThemeMode.DARK:
            self.theme_manager.set_theme(ThemeMode.LIGHT)
        else:
            self.theme_manager.set_theme(ThemeMode.DARK)
