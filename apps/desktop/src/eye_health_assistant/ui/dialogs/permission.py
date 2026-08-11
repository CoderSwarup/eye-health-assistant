"""Camera permission dialog — shown when camera access is denied."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CameraPermissionDialog(QDialog):
    """Dialog explaining camera permission denial and offering alternatives."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Camera Permission Required")
        self.setMinimumWidth(420)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel("Camera Access Unavailable")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Description
        description = QLabel(
            "Eye Health Assistant needs camera access to monitor blink rate "
            "and eye movement in Smart Mode.\n\n"
            "Camera access was denied or is unavailable. You can:\n\n"
            "  Use Timer Mode instead (no camera required)\n"
            "  Grant camera permission in System Settings\n"
            "  Restart the app after granting permission"
        )
        description.setObjectName("subtitle")
        description.setWordWrap(True)
        layout.addWidget(description)

        layout.addSpacing(16)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self._settings_btn = QPushButton("Open System Settings")
        self._settings_btn.setAccessibleName(
            "Open system settings to grant camera permission"
        )
        self._settings_btn.clicked.connect(self._open_settings)
        btn_layout.addWidget(self._settings_btn)

        self._timer_btn = QPushButton("Use Timer Mode")
        self._timer_btn.setAccessibleName(
            "Switch to Timer Mode which does not require camera"
        )
        self._timer_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self._timer_btn)

        layout.addLayout(btn_layout)

    def _open_settings(self) -> None:
        """Open system camera settings (platform-specific)."""
        import subprocess
        import sys

        try:
            if sys.platform == "darwin":
                subprocess.run(
                    ["open", "x-apple.systempreferences:com.apple.preference"
                     ".security?Privacy_Camera"],
                    check=False,
                )
            elif sys.platform == "win32":
                subprocess.run(
                    ["start", "ms-settings:privacy-webcam"],
                    check=False,
                    shell=True,
                )
            else:
                subprocess.run(
                    ["xdg-open",
                     "x-apple.systempreferences:com.apple.preference"
                     ".security?Privacy_Camera"],
                    check=False,
                )
        except Exception:
            pass  # Best effort — don't crash if settings can't open
