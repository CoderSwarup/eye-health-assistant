"""Unit tests for core configuration."""

from pathlib import Path

from eye_health_assistant.core.config import Config, get_app_data_dir


def test_get_app_data_dir_returns_path():
    """App data directory should return a Path."""
    result = get_app_data_dir()
    assert isinstance(result, Path)


def test_get_app_data_dir_creates_directory():
    """App data directory should be created if it doesn't exist."""
    result = get_app_data_dir()
    assert result.exists()


def test_config_default_database_path():
    """Config should create a default database path."""
    config = Config()
    assert config.database_path is not None
    assert config.database_path.name == "app.sqlite"


def test_config_from_nonexistent_file():
    """Config from nonexistent file should return defaults."""
    config = Config.from_file(Path("/nonexistent/config.json"))
    assert config.theme == "system"
    assert config.language == "en"


def test_config_save_and_load(tmp_path: Path):
    """Config should be saveable and loadable."""
    config = Config(theme="dark")
    config_path = tmp_path / "config.json"
    config.save(config_path)

    loaded = Config.from_file(config_path)
    assert loaded.theme == "dark"
