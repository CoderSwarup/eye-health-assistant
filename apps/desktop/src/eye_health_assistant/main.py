"""Application entry point."""

from __future__ import annotations

import contextlib
import logging
import os
import signal
import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.core.constants import APP_NAME, VERSION
from eye_health_assistant.core.logging import setup_logging
from eye_health_assistant.ui.main_window import MainWindow

_interrupted = False
_lock_file: Path | None = None


def _handle_sigint(*_args: object) -> None:
    global _interrupted
    _interrupted = True


def _acquire_instance_lock() -> bool:
    """Try to acquire a singleton instance lock. Returns True if successful."""
    global _lock_file
    lock_dir = Path(tempfile.gettempdir()) / "eye_health_assistant"
    lock_dir.mkdir(parents=True, exist_ok=True)
    _lock_file = lock_dir / "app.lock"

    if _lock_file.exists():
        # Check if the process is still running
        try:
            pid = int(_lock_file.read_text().strip())
            # On Unix, check if process exists
            try:
                os.kill(pid, 0)
                # Process exists - another instance is running
                return False
            except (ProcessLookupError, PermissionError):
                # Process doesn't exist - stale lock
                _lock_file.unlink(missing_ok=True)
        except (ValueError, OSError):
            # Invalid lock file - remove it
            _lock_file.unlink(missing_ok=True)

    # Write our PID
    _lock_file.write_text(str(os.getpid()))
    return True


def _release_instance_lock() -> None:
    """Release the singleton instance lock."""
    global _lock_file
    if _lock_file and _lock_file.exists():
        with contextlib.suppress(OSError):
            _lock_file.unlink()
        _lock_file = None


def main() -> int:
    """Run the Eye Health Assistant application.

    Returns:
        Exit code.
    """
    # Setup basic logging first (before any other imports that might log)
    setup_logging(level="INFO")

    # Check for singleton instance
    if not _acquire_instance_lock():
        print(f"{APP_NAME} is already running.", file=sys.stderr)
        return 1

    try:
        # Allow Ctrl+C to work by handling SIGINT via timer
        signal.signal(signal.SIGINT, _handle_sigint)
        signal.signal(signal.SIGTERM, _handle_sigint)

        # Create Qt application FIRST
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setOrganizationName("EyeHealthAssistant")
        app.setApplicationVersion(VERSION)

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

    except Exception as e:
        logging.critical("Fatal error during startup: %s", e, exc_info=True)
        return 1

    finally:
        _release_instance_lock()


if __name__ == "__main__":
    sys.exit(main())
