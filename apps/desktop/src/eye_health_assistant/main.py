"""Application entry point."""

from __future__ import annotations

import signal
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.ui.main_window import MainWindow

_interrupted = False


def _handle_sigint(*_args: object) -> None:
    global _interrupted
    _interrupted = True


def main() -> int:
    """Run the Eye Health Assistant application.

    Returns:
        Exit code.
    """
    # Allow Ctrl+C to work by handling SIGINT via timer
    signal.signal(signal.SIGINT, _handle_sigint)
    signal.signal(signal.SIGTERM, _handle_sigint)

    # Create Qt application FIRST
    app = QApplication(sys.argv)
    app.setApplicationName("Eye Health Assistant")
    app.setOrganizationName("EyeHealthAssistant")
    app.setApplicationVersion("0.1.0")

    # Initialize dependencies AFTER QApplication exists
    deps = Dependencies()
    deps.initialize(parent=app)

    # Create and show main window
    window = MainWindow(deps=deps)
    window.show()

    # Poll for SIGINT every 200ms so Ctrl+C works
    def _check_interrupt() -> None:
        if _interrupted:
            app.quit()
        else:
            QTimer.singleShot(200, _check_interrupt)

    QTimer.singleShot(200, _check_interrupt)

    # Run event loop
    exit_code: int = app.exec()

    # Clean up
    deps.shutdown()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
