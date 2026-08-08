"""Settings page — application preferences and configuration."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies


def _build_section(title: str) -> tuple[QFrame, QVBoxLayout]:
    """Create a styled card section with a title."""
    card = QFrame()
    card.setObjectName("card")
    card.setFrameShape(QFrame.Shape.NoFrame)

    layout = QVBoxLayout(card)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(16)

    label = QLabel(title)
    label.setObjectName("section-title")
    layout.addWidget(label)

    return card, layout


def _build_row(label_text: str, widget: QWidget) -> QHBoxLayout:
    """Create a label + widget row."""
    row = QHBoxLayout()
    row.setSpacing(12)

    label = QLabel(label_text)
    label.setObjectName("subtitle")
    row.addWidget(label)

    row.addStretch()
    row.addWidget(widget)

    return row


class SettingsPage(QWidget):
    """Application settings and preferences page."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        # Header
        title = QLabel("Settings")
        title.setObjectName("page-title")
        layout.addWidget(title)

        # --- Appearance ---
        appearance_card, appearance_layout = _build_section("Appearance")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        appearance_layout.addLayout(_build_row("Theme", self.theme_combo))

        layout.addWidget(appearance_card)

        # --- Timer Defaults ---
        timer_card, timer_layout = _build_section("Timer Defaults")

        self.focus_spin = QSpinBox()
        self.focus_spin.setRange(1, 120)
        self.focus_spin.setSuffix(" min")
        timer_layout.addLayout(_build_row("Focus Duration", self.focus_spin))

        self.break_spin = QSpinBox()
        self.break_spin.setRange(5, 300)
        self.break_spin.setSuffix(" sec")
        timer_layout.addLayout(_build_row("Break Duration", self.break_spin))

        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 30)
        self.long_break_spin.setSuffix(" min")
        timer_layout.addLayout(_build_row("Long Break Duration", self.long_break_spin))

        layout.addWidget(timer_card)

        # --- Notifications ---
        notif_card, notif_layout = _build_section("Notifications")

        self.notifications_check = QCheckBox("Enable notifications")
        self.notifications_check.setObjectName("subtitle")
        notif_layout.addWidget(self.notifications_check)

        self.notif_interval_spin = QSpinBox()
        self.notif_interval_spin.setRange(60, 1800)
        self.notif_interval_spin.setSuffix(" sec")
        notif_layout.addLayout(
            _build_row("Min Notification Interval", self.notif_interval_spin)
        )

        layout.addWidget(notif_card)

        # --- Smart Mode ---
        smart_card, smart_layout = _build_section("Smart Mode (Camera)")

        self.blink_threshold_spin = QDoubleSpinBox()
        self.blink_threshold_spin.setRange(5.0, 30.0)
        self.blink_threshold_spin.setSingleStep(0.5)
        self.blink_threshold_spin.setSuffix(" blinks/min")
        smart_layout.addLayout(
            _build_row("Blink Rate Threshold", self.blink_threshold_spin)
        )

        self.rolling_window_spin = QSpinBox()
        self.rolling_window_spin.setRange(1, 10)
        self.rolling_window_spin.setSuffix(" min")
        smart_layout.addLayout(_build_row("Rolling Window", self.rolling_window_spin))

        layout.addWidget(smart_card)

        # --- Data ---
        data_card, data_layout = _build_section("Data")

        export_btn = QPushButton("Export Data")
        export_btn.setObjectName("secondary-button")
        data_layout.addWidget(export_btn)

        delete_btn = QPushButton("Delete All Data")
        delete_btn.setObjectName("danger-button")
        data_layout.addWidget(delete_btn)

        layout.addWidget(data_card)

        layout.addStretch()

    def _load_values(self) -> None:
        """Load current config values into widgets."""
        config = self.deps.config

        # Theme
        theme_map = {"light": 0, "dark": 1, "system": 2}
        self.theme_combo.setCurrentIndex(theme_map.get(config.theme, 2))

        # Timer
        self.focus_spin.setValue(config.focus_duration // 60)
        self.break_spin.setValue(config.break_duration)
        self.long_break_spin.setValue(config.long_break_duration // 60)

        # Notifications
        self.notifications_check.setChecked(config.notifications_enabled)
        self.notif_interval_spin.setValue(config.min_notification_interval)

        # Smart Mode
        self.blink_threshold_spin.setValue(config.blink_rate_threshold)
        self.rolling_window_spin.setValue(config.rolling_window_minutes)

    def save(self) -> None:
        """Save current widget values back to config."""
        config = self.deps.config

        theme_values = {0: "light", 1: "dark", 2: "system"}
        config.theme = theme_values.get(self.theme_combo.currentIndex(), "system")

        config.focus_duration = self.focus_spin.value() * 60
        config.break_duration = self.break_spin.value()
        config.long_break_duration = self.long_break_spin.value() * 60

        config.notifications_enabled = self.notifications_check.isChecked()
        config.min_notification_interval = self.notif_interval_spin.value()

        config.blink_rate_threshold = self.blink_threshold_spin.value()
        config.rolling_window_minutes = self.rolling_window_spin.value()
