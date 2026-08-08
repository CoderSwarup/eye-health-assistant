"""Test configuration."""

from pathlib import Path

import pytest


@pytest.fixture
def sample_config(tmp_path: Path):
    """Create a sample configuration for testing."""
    from eye_health_assistant.core.config import Config

    return Config(app_data_dir=tmp_path)
