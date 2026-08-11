"""Structured application logging with rotation."""

from __future__ import annotations

import logging
import logging.handlers
import sys
import threading
import traceback
from pathlib import Path
from types import TracebackType
from typing import Any

# Global lock for thread-safe logging setup
_setup_lock = threading.Lock()
_initialized = False


def setup_logging(level: str = "INFO", log_dir: Path | None = None) -> None:
    """Configure application logging with rotation.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_dir: Optional directory for log files.
    """
    global _initialized

    with _setup_lock:
        if _initialized:
            return

        numeric_level = getattr(logging, level.upper(), logging.INFO)

        handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

        if log_dir is not None:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / "app.log"

            # Rotating file handler: 5MB max, keep 3 backups
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=3,
                encoding="utf-8",
            )
            file_handler.setLevel(numeric_level)
            handlers.append(file_handler)

        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=handlers,
        )

        # Suppress noisy third-party loggers
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("matplotlib").setLevel(logging.WARNING)
        logging.getLogger("PIL").setLevel(logging.WARNING)

        # Install global exception handler
        _install_exception_hook()

        _initialized = True
        logging.info("Logging initialized at level %s", level)


def _install_exception_hook() -> None:
    """Install a global exception hook to capture unhandled exceptions."""
    original_excepthook = sys.excepthook

    def _exception_hook(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        # Ignore KeyboardInterrupt and SystemExit
        if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
            if original_excepthook is not None:
                original_excepthook(exc_type, exc_value, exc_traceback)
            return

        # Log the exception
        logger = logging.getLogger("eye_health_assistant.unhandled")
        logger.critical(
            "Unhandled exception:\n%s",
            "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)),
        )

    sys.excepthook = _exception_hook


def install_thread_excepthook() -> None:
    """Install an exception hook for threading module."""
    original_init = threading.Thread.__init__

    def _thread_init(
        self: threading.Thread,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        original_init(self, *args, **kwargs)
        original_run = self.run

        def _wrapped_run() -> None:
            try:
                original_run()
            except Exception:
                logger = logging.getLogger("eye_health_assistant.thread")
                logger.exception("Unhandled exception in thread %s", self.name)

        self.run = _wrapped_run  # type: ignore[method-assign]

    threading.Thread.__init__ = _thread_init  # type: ignore[method-assign]
