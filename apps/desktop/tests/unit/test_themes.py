"""Unit tests for theme system."""

from eye_health_assistant.ui.themes import (
    DARK,
    LIGHT,
    ThemeColors,
    generate_stylesheet,
    get_theme,
)


def test_get_theme_light():
    """get_theme('light') should return LIGHT colors."""
    theme = get_theme("light")
    assert theme is LIGHT


def test_get_theme_dark():
    """get_theme('dark') should return DARK colors."""
    theme = get_theme("dark")
    assert theme is DARK


def test_get_theme_system():
    """get_theme('system') should return a valid theme."""
    theme = get_theme("system")
    assert isinstance(theme, ThemeColors)


def test_get_theme_unknown():
    """get_theme with unknown name should fall back to LIGHT."""
    theme = get_theme("unknown")
    assert theme is LIGHT


def test_theme_colors_have_required_fields():
    """Theme colors should have all required attributes."""
    for theme in [LIGHT, DARK]:
        assert theme.background_primary
        assert theme.text_primary
        assert theme.accent_primary
        assert theme.success
        assert theme.warning
        assert theme.error


def test_generate_stylesheet():
    """generate_stylesheet should return a non-empty string."""
    stylesheet = generate_stylesheet(LIGHT)
    assert isinstance(stylesheet, str)
    assert len(stylesheet) > 0
    assert "background-color" in stylesheet
