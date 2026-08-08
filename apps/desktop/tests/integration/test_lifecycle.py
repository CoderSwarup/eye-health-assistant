"""Integration tests for application lifecycle."""

from eye_health_assistant.app.lifecycle import ApplicationLifecycle
from eye_health_assistant.core.config import Config


def test_lifecycle_initialize(tmp_path):
    """Lifecycle should initialize successfully."""
    config = Config(app_data_dir=tmp_path)
    lifecycle = ApplicationLifecycle(config)
    lifecycle.initialize()
    assert lifecycle._initialized is True


def test_lifecycle_shutdown(tmp_path):
    """Lifecycle should shut down successfully."""
    config = Config(app_data_dir=tmp_path)
    lifecycle = ApplicationLifecycle(config)
    lifecycle.initialize()
    lifecycle.shutdown()
    assert lifecycle._initialized is False


def test_lifecycle_double_initialize(tmp_path):
    """Double initialization should be safe."""
    config = Config(app_data_dir=tmp_path)
    lifecycle = ApplicationLifecycle(config)
    lifecycle.initialize()
    lifecycle.initialize()  # Should not raise
    assert lifecycle._initialized is True


def test_lifecycle_creates_directories(tmp_path):
    """Lifecycle should create required directories."""
    config = Config(app_data_dir=tmp_path)
    lifecycle = ApplicationLifecycle(config)
    lifecycle.initialize()

    assert (tmp_path / "database").exists()
    assert (tmp_path / "logs").exists()
    assert (tmp_path / "exports").exists()
    assert (tmp_path / "cache").exists()
