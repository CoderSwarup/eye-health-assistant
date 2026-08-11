"""Settings page — application preferences and configuration."""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies

logger = logging.getLogger(__name__)


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

        # Status label for save feedback
        self._status_label = QLabel("")
        self._status_label.setObjectName("subtitle")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._status_label.setVisible(False)
        layout.addWidget(self._status_label)

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

        # --- Quiet Hours ---
        quiet_card, quiet_layout = _build_section("Quiet Hours")

        self.quiet_hours_check = QCheckBox("Enable quiet hours")
        self.quiet_hours_check.setObjectName("subtitle")
        quiet_layout.addWidget(self.quiet_hours_check)

        from PySide6.QtCore import QTime

        self.quiet_start_edit = QTimeEdit()
        self.quiet_start_edit.setDisplayFormat("HH:mm")
        self.quiet_start_edit.setTime(QTime(22, 0))
        quiet_layout.addLayout(_build_row("Start Time", self.quiet_start_edit))

        self.quiet_end_edit = QTimeEdit()
        self.quiet_end_edit.setDisplayFormat("HH:mm")
        self.quiet_end_edit.setTime(QTime(7, 0))
        quiet_layout.addLayout(_build_row("End Time", self.quiet_end_edit))

        layout.addWidget(quiet_card)

        # --- Sound ---
        sound_card, sound_layout = _build_section("Sound")

        self.sound_check = QCheckBox("Enable notification sounds")
        self.sound_check.setObjectName("subtitle")
        sound_layout.addWidget(self.sound_check)

        layout.addWidget(sound_card)

        # --- Startup Behavior ---
        startup_card, startup_layout = _build_section("Startup Behavior")

        self.start_minimized_check = QCheckBox("Start minimized to tray")
        self.start_minimized_check.setObjectName("subtitle")
        startup_layout.addWidget(self.start_minimized_check)

        self.start_on_login_check = QCheckBox("Start on login")
        self.start_on_login_check.setObjectName("subtitle")
        startup_layout.addWidget(self.start_on_login_check)

        self.start_monitoring_check = QCheckBox("Start monitoring automatically")
        self.start_monitoring_check.setObjectName("subtitle")
        startup_layout.addWidget(self.start_monitoring_check)

        layout.addWidget(startup_card)

        # --- Smart Mode (Camera) ---
        smart_card, smart_layout = _build_section("Smart Mode (Camera)")

        self.camera_enabled_check = QCheckBox("Enable camera monitoring")
        self.camera_enabled_check.setObjectName("subtitle")
        smart_layout.addWidget(self.camera_enabled_check)

        self.camera_device_combo = QComboBox()
        self.camera_device_combo.setMinimumWidth(200)
        self._populate_camera_devices()
        smart_layout.addLayout(_build_row("Camera Device", self.camera_device_combo))

        self.camera_preview_check = QCheckBox(
            "Show camera preview (privacy: never persisted)"
        )
        self.camera_preview_check.setObjectName("subtitle")
        smart_layout.addWidget(self.camera_preview_check)

        self.sampling_fps_spin = QSpinBox()
        self.sampling_fps_spin.setRange(1, 30)
        self.sampling_fps_spin.setSuffix(" fps")
        smart_layout.addLayout(_build_row("Sampling FPS", self.sampling_fps_spin))

        self.min_observation_spin = QSpinBox()
        self.min_observation_spin.setRange(1, 60)
        self.min_observation_spin.setSuffix(" sec")
        smart_layout.addLayout(
            _build_row("Min Observation Time", self.min_observation_spin)
        )

        layout.addWidget(smart_card)

        # --- Blink Detection ---
        blink_card, blink_layout = _build_section("Blink Detection Thresholds")

        self.close_threshold_spin = QDoubleSpinBox()
        self.close_threshold_spin.setRange(0.1, 0.5)
        self.close_threshold_spin.setSingleStep(0.01)
        self.close_threshold_spin.setDecimals(2)
        blink_layout.addLayout(
            _build_row("Close Threshold (EAR)", self.close_threshold_spin)
        )

        self.open_threshold_spin = QDoubleSpinBox()
        self.open_threshold_spin.setRange(0.1, 0.5)
        self.open_threshold_spin.setSingleStep(0.01)
        self.open_threshold_spin.setDecimals(2)
        blink_layout.addLayout(
            _build_row("Open Threshold (EAR)", self.open_threshold_spin)
        )

        self.closed_threshold_spin = QDoubleSpinBox()
        self.closed_threshold_spin.setRange(0.05, 0.3)
        self.closed_threshold_spin.setSingleStep(0.01)
        self.closed_threshold_spin.setDecimals(2)
        blink_layout.addLayout(
            _build_row("Closed Threshold (EAR)", self.closed_threshold_spin)
        )

        layout.addWidget(blink_card)

        # --- Analytics ---
        analytics_card, analytics_layout = _build_section("Analytics")

        self.blink_threshold_spin = QDoubleSpinBox()
        self.blink_threshold_spin.setRange(5.0, 30.0)
        self.blink_threshold_spin.setSingleStep(0.5)
        self.blink_threshold_spin.setSuffix(" blinks/min")
        analytics_layout.addLayout(
            _build_row("Low Blink Rate Threshold", self.blink_threshold_spin)
        )

        self.rolling_window_spin = QSpinBox()
        self.rolling_window_spin.setRange(1, 10)
        self.rolling_window_spin.setSuffix(" min")
        analytics_layout.addLayout(
            _build_row("Rolling Window", self.rolling_window_spin)
        )

        self.sustained_low_spin = QSpinBox()
        self.sustained_low_spin.setRange(10, 300)
        self.sustained_low_spin.setSuffix(" sec")
        analytics_layout.addLayout(
            _build_row("Sustained Low Blink Alert", self.sustained_low_spin)
        )

        layout.addWidget(analytics_card)

        # --- Data ---
        data_card, data_layout = _build_section("Data")

        self._export_btn = QPushButton("Export Data")
        self._export_btn.setObjectName("secondary-button")
        self._export_btn.setAccessibleName("Export all data as JSON file")
        self._export_btn.clicked.connect(self._on_export)
        data_layout.addWidget(self._export_btn)

        self._delete_btn = QPushButton("Delete All Data")
        self._delete_btn.setObjectName("danger-button")
        self._delete_btn.setAccessibleName("Permanently delete all application data")
        self._delete_btn.clicked.connect(self._on_delete_all)
        data_layout.addWidget(self._delete_btn)

        layout.addWidget(data_card)

        # --- Action buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self._reset_btn = QPushButton("Reset to Defaults")
        self._reset_btn.setObjectName("secondary-button")
        self._reset_btn.setAccessibleName("Reset all settings to default values")
        self._reset_btn.clicked.connect(self._on_reset)
        btn_layout.addWidget(self._reset_btn)

        btn_layout.addStretch()

        self._save_btn = QPushButton("Save Settings")
        self._save_btn.setObjectName("primary-button")
        self._save_btn.setAccessibleName("Save current settings to disk")
        self._save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(self._save_btn)

        layout.addLayout(btn_layout)

        layout.addStretch()

    def _populate_camera_devices(self) -> None:
        """Populate the camera device dropdown with available devices."""
        self.camera_device_combo.clear()
        if self.deps.monitoring_service is not None:
            try:
                devices = self.deps.monitoring_service.get_available_cameras()
                for idx in devices:
                    self.camera_device_combo.addItem(f"Camera {idx}", idx)
            except Exception:
                self.camera_device_combo.addItem("Default (0)", 0)
        else:
            self.camera_device_combo.addItem("Default (0)", 0)

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

        # Quiet Hours
        self.quiet_hours_check.setChecked(
            config.quiet_hours_start != "" or config.quiet_hours_end != ""
        )
        from PySide6.QtCore import QTime

        try:
            start_parts = config.quiet_hours_start.split(":")
            self.quiet_start_edit.setTime(
                QTime(int(start_parts[0]), int(start_parts[1]))
            )
        except (ValueError, IndexError):
            self.quiet_start_edit.setTime(QTime(22, 0))
        try:
            end_parts = config.quiet_hours_end.split(":")
            self.quiet_end_edit.setTime(
                QTime(int(end_parts[0]), int(end_parts[1]))
            )
        except (ValueError, IndexError):
            self.quiet_end_edit.setTime(QTime(7, 0))

        # Sound
        self.sound_check.setChecked(config.notification_sound_enabled)

        # Startup
        self.start_minimized_check.setChecked(config.start_minimized)
        self.start_on_login_check.setChecked(config.start_on_login)
        self.start_monitoring_check.setChecked(config.start_monitoring_auto)

        # Smart Mode
        self.camera_enabled_check.setChecked(config.camera_enabled)
        self.camera_preview_check.setChecked(config.camera_preview_enabled)
        self.sampling_fps_spin.setValue(config.sampling_fps)
        self.min_observation_spin.setValue(config.min_observation_seconds)

        # Blink Detection
        self.close_threshold_spin.setValue(config.ear_close_threshold)
        self.open_threshold_spin.setValue(config.ear_open_threshold)
        self.closed_threshold_spin.setValue(config.ear_closed_threshold)

        # Analytics
        self.blink_threshold_spin.setValue(config.blink_rate_threshold)
        self.rolling_window_spin.setValue(config.rolling_window_minutes)
        self.sustained_low_spin.setValue(config.sustained_low_blink_seconds)

    def _apply_values_to_config(self) -> None:
        """Apply widget values to the config object (without saving)."""
        config = self.deps.config

        theme_values = {0: "light", 1: "dark", 2: "system"}
        config.theme = theme_values.get(self.theme_combo.currentIndex(), "system")

        config.focus_duration = self.focus_spin.value() * 60
        config.break_duration = self.break_spin.value()
        config.long_break_duration = self.long_break_spin.value() * 60

        config.notifications_enabled = self.notifications_check.isChecked()
        config.min_notification_interval = self.notif_interval_spin.value()

        # Quiet Hours
        if self.quiet_hours_check.isChecked():
            config.quiet_hours_start = self.quiet_start_edit.time().toString("HH:mm")
            config.quiet_hours_end = self.quiet_end_edit.time().toString("HH:mm")
        else:
            config.quiet_hours_start = ""
            config.quiet_hours_end = ""

        # Sound
        config.notification_sound_enabled = self.sound_check.isChecked()

        # Startup
        config.start_minimized = self.start_minimized_check.isChecked()
        config.start_on_login = self.start_on_login_check.isChecked()
        config.start_monitoring_auto = self.start_monitoring_check.isChecked()

        # Smart Mode
        config.camera_enabled = self.camera_enabled_check.isChecked()
        device_data = self.camera_device_combo.currentData()
        if device_data is not None:
            config.camera_device_index = device_data
        config.camera_preview_enabled = self.camera_preview_check.isChecked()
        config.sampling_fps = self.sampling_fps_spin.value()
        config.min_observation_seconds = self.min_observation_spin.value()

        # Blink Detection
        config.ear_close_threshold = self.close_threshold_spin.value()
        config.ear_open_threshold = self.open_threshold_spin.value()
        config.ear_closed_threshold = self.closed_threshold_spin.value()

        # Analytics
        config.blink_rate_threshold = self.blink_threshold_spin.value()
        config.rolling_window_minutes = self.rolling_window_spin.value()
        config.sustained_low_blink_seconds = self.sustained_low_spin.value()

    def _show_status(self, message: str, is_error: bool = False) -> None:
        """Show a status message to the user."""
        self._status_label.setText(message)
        self._status_label.setVisible(True)
        if is_error:
            self._status_label.setStyleSheet("color: #ef4444;")
        else:
            self._status_label.setStyleSheet("color: #22c55e;")

    def _on_save(self) -> None:
        """Save settings with validation."""
        self._apply_values_to_config()
        errors = self.deps.save_config()

        if errors:
            self._show_status(
                "Validation errors:\n" + "\n".join(f"  - {e}" for e in errors),
                is_error=True,
            )
            logger.warning("Settings save failed: %s", errors)
        else:
            self._show_status("Settings saved successfully.")
            logger.info("Settings saved")

    def _on_reset(self) -> None:
        """Reset all settings to defaults."""
        from PySide6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all settings to their default values?\n\n"
            "This will not save until you click Save.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.deps.config = type(self.deps.config)()  # Create default config
            self._load_values()
            self._show_status("Settings reset to defaults. Click Save to apply.")

    def _on_export(self) -> None:
        """Export all data as JSON."""
        import json
        from datetime import datetime

        from PySide6.QtWidgets import QFileDialog, QMessageBox

        if self.deps.analytics_service is None:
            QMessageBox.warning(
                self,
                "Export",
                "Analytics service not available.",
            )
            return

        data = self.deps.analytics_service.export_all_data()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            f"eye_health_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)",
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    f"Data exported to:\n{file_path}\n\n"
                    f"Timer sessions: {len(data.get('timer_sessions', []))}\n"
                    f"Monitoring sessions: {len(data.get('monitoring_sessions', []))}\n"
                    f"Blink measurements: {len(data.get('blink_measurements', []))}",
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export data:\n{e}",
                )

    def _on_delete_all(self) -> None:
        """Delete all data with confirmation."""
        from PySide6.QtWidgets import QMessageBox

        if self.deps.analytics_service is None:
            return

        reply = QMessageBox.warning(
            self,
            "Delete All Data",
            "This will permanently delete:\n\n"
            "- All timer sessions\n"
            "- All monitoring sessions\n"
            "- All blink measurements\n"
            "- All statistics history\n\n"
            "This action cannot be undone.\n\n"
            "Are you sure you want to delete all data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            count = self.deps.analytics_service.delete_all_data()
            QMessageBox.information(
                self,
                "Data Deleted",
                f"Successfully deleted {count} records.",
            )
