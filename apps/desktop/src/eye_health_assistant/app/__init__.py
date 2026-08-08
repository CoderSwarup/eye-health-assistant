"""Application bootstrap and lifecycle management."""

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.app.lifecycle import ApplicationLifecycle

__all__ = ["ApplicationLifecycle", "Dependencies"]
