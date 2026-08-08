"""Theme system for Eye Health Assistant.

Provides light, dark, and system-aware themes using a consistent design token approach.
The design follows a premium, calm, monochrome-first aesthetic with neutral colors
as the foundation and sparing accent colors for success, warning, and active states.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemeColors:
    """Design token color values for a theme."""

    # Backgrounds
    background_primary: str
    background_secondary: str
    background_tertiary: str
    background_elevated: str

    # Foregrounds / text
    text_primary: str
    text_secondary: str
    text_tertiary: str
    text_inverse: str

    # Borders
    border_primary: str
    border_secondary: str
    border_focus: str

    # Accent colors
    accent_primary: str
    accent_primary_hover: str
    accent_secondary: str

    # Status colors
    success: str
    warning: str
    error: str
    info: str

    # Interactive
    button_primary_bg: str
    button_primary_text: str
    button_secondary_bg: str
    button_secondary_text: str
    button_danger_bg: str
    button_danger_text: str

    # Sidebar
    sidebar_bg: str
    sidebar_active_bg: str
    sidebar_active_text: str
    sidebar_hover_bg: str

    # Cards
    card_bg: str
    card_border: str
    card_shadow: str

    # Input
    input_bg: str
    input_border: str
    input_border_focus: str

    # Overlay
    overlay_bg: str
    modal_bg: str


LIGHT = ThemeColors(
    # Backgrounds
    background_primary="#FFFFFF",
    background_secondary="#F8F9FA",
    background_tertiary="#F1F3F5",
    background_elevated="#FFFFFF",
    # Foregrounds
    text_primary="#1A1A1A",
    text_secondary="#6C757D",
    text_tertiary="#ADB5BD",
    text_inverse="#FFFFFF",
    # Borders
    border_primary="#DEE2E6",
    border_secondary="#E9ECEF",
    border_focus="#495057",
    # Accent
    accent_primary="#2563EB",
    accent_primary_hover="#1D4ED8",
    accent_secondary="#7C3AED",
    # Status
    success="#16A34A",
    warning="#D97706",
    error="#DC2626",
    info="#2563EB",
    # Buttons
    button_primary_bg="#2563EB",
    button_primary_text="#FFFFFF",
    button_secondary_bg="#F1F3F5",
    button_secondary_text="#1A1A1A",
    button_danger_bg="#DC2626",
    button_danger_text="#FFFFFF",
    # Sidebar
    sidebar_bg="#F8F9FA",
    sidebar_active_bg="#E9ECEF",
    sidebar_active_text="#1A1A1A",
    sidebar_hover_bg="#F1F3F5",
    # Cards
    card_bg="#FFFFFF",
    card_border="#DEE2E6",
    card_shadow="rgba(0, 0, 0, 0.04)",
    # Input
    input_bg="#FFFFFF",
    input_border="#DEE2E6",
    input_border_focus="#2563EB",
    # Overlay
    overlay_bg="rgba(0, 0, 0, 0.4)",
    modal_bg="#FFFFFF",
)

DARK = ThemeColors(
    # Backgrounds
    background_primary="#111111",
    background_secondary="#1A1A1A",
    background_tertiary="#222222",
    background_elevated="#1E1E1E",
    # Foregrounds
    text_primary="#E5E5E5",
    text_secondary="#A0A0A0",
    text_tertiary="#666666",
    text_inverse="#111111",
    # Borders
    border_primary="#333333",
    border_secondary="#2A2A2A",
    border_focus="#666666",
    # Accent
    accent_primary="#3B82F6",
    accent_primary_hover="#60A5FA",
    accent_secondary="#8B5CF6",
    # Status
    success="#22C55E",
    warning="#FBBF24",
    error="#EF4444",
    info="#3B82F6",
    # Buttons
    button_primary_bg="#3B82F6",
    button_primary_text="#FFFFFF",
    button_secondary_bg="#2A2A2A",
    button_secondary_text="#E5E5E5",
    button_danger_bg="#EF4444",
    button_danger_text="#FFFFFF",
    # Sidebar
    sidebar_bg="#161618",
    sidebar_active_bg="#2A2A2A",
    sidebar_active_text="#E5E5E5",
    sidebar_hover_bg="#1E1E20",
    # Cards
    card_bg="#1C1C1E",
    card_border="transparent",
    card_shadow="0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)",
    # Input
    input_bg="#222222",
    input_border="#333333",
    input_border_focus="#3B82F6",
    # Overlay
    overlay_bg="rgba(0, 0, 0, 0.6)",
    modal_bg="#1E1E1E",
)

THEMES: dict[str, ThemeColors] = {
    "light": LIGHT,
    "dark": DARK,
}


def get_theme(name: str) -> ThemeColors:
    """Get theme colors by name.

    Args:
        name: Theme name ('light', 'dark', or 'system').

    Returns:
        ThemeColors for the requested theme. Falls back to 'light' if unknown.
    """
    if name == "system":
        return DARK  # Will be resolved by the widget using system detection
    return THEMES.get(name, LIGHT)


def generate_stylesheet(colors: ThemeColors) -> str:
    """Generate a Qt stylesheet from theme colors.

    Args:
        colors: Theme color tokens.

    Returns:
        Qt stylesheet string.
    """
    return f"""
    /* === Global — NO border on QWidget, only color/font === */
    QWidget {{
        background-color: {colors.background_primary};
        color: {colors.text_primary};
        font-family: Helvetica, Arial, sans-serif;
        font-size: 13px;
        border: none;
    }}

    /* === Main Window === */
    QMainWindow {{
        background-color: {colors.background_primary};
    }}

    /* === Sidebar / Navigation === */
    #sidebar {{
        background-color: {colors.sidebar_bg};
        border-right: 1px solid {colors.border_secondary};
        min-width: 230px;
        max-width: 230px;
    }}

    #nav-button {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 11px 16px;
        text-align: left;
        color: {colors.text_secondary};
        font-size: 13px;
        margin: 2px 8px;
    }}

    #nav-button:hover {{
        background-color: {colors.sidebar_hover_bg};
        color: {colors.text_primary};
    }}

    #nav-button:checked {{
        background-color: {colors.sidebar_active_bg};
        color: {colors.sidebar_active_text};
        font-weight: 500;
    }}

    /* === Cards === */
    #card {{
        background-color: {colors.card_bg};
        border: 1px solid {colors.card_border};
        border-radius: 14px;
        padding: 24px;
    }}

    #metric-card {{
        background-color: {colors.background_tertiary};
        border: none;
        border-radius: 12px;
        padding: 20px 20px 16px 20px;
        min-height: 110px;
    }}

    /* === Labels inside cards — force no border/background === */
    #card QLabel, #metric-card QLabel {{
        background-color: transparent;
        border: none;
    }}

    /* === Buttons === */
    QPushButton {{
        background-color: {colors.button_primary_bg};
        color: {colors.button_primary_text};
        border: none;
        border-radius: 8px;
        padding: 9px 20px;
        font-weight: 500;
        font-size: 13px;
        min-height: 18px;
    }}

    QPushButton:hover {{
        background-color: {colors.accent_primary_hover};
    }}

    QPushButton:pressed {{
        background-color: {colors.accent_primary};
    }}

    QPushButton:disabled {{
        background-color: {colors.background_tertiary};
        color: {colors.text_tertiary};
    }}

    #secondary-button {{
        background-color: {colors.button_secondary_bg};
        color: {colors.button_secondary_text};
        border: 1px solid {colors.border_secondary};
    }}

    #secondary-button:hover {{
        background-color: {colors.border_secondary};
    }}

    #danger-button {{
        background-color: {colors.button_danger_bg};
        color: {colors.button_danger_text};
    }}

    /* === Inputs === */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: {colors.input_bg};
        border: 1px solid {colors.input_border};
        border-radius: 8px;
        padding: 8px 12px;
        color: {colors.text_primary};
        font-size: 13px;
    }}

    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border-color: {colors.input_border_focus};
    }}

    /* === Progress === */
    QProgressBar {{
        background-color: {colors.background_tertiary};
        border: none;
        border-radius: 4px;
        height: 8px;
        text-align: center;
    }}

    QProgressBar::chunk {{
        background-color: {colors.accent_primary};
        border-radius: 4px;
    }}

    /* === Scrollbar === */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background-color: {colors.border_primary};
        border-radius: 4px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {colors.text_tertiary};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}

    /* === Labels === */
    #page-title {{
        font-size: 24px;
        font-weight: 600;
        color: {colors.text_primary};
        padding: 0;
    }}

    #section-title {{
        font-size: 16px;
        font-weight: 600;
        color: {colors.text_primary};
        padding: 0;
    }}

    #subtitle {{
        font-size: 14px;
        color: {colors.text_secondary};
        padding: 0;
    }}

    #caption {{
        font-size: 11px;
        color: {colors.text_tertiary};
        padding: 0;
    }}

    /* === Stat Number === */
    #stat-number {{
        font-size: 30px;
        font-weight: 700;
        color: {colors.text_primary};
        padding: 0;
    }}

    /* === Toggle === */
    QCheckBox {{
        spacing: 8px;
    }}

    QCheckBox::indicator {{
        width: 40px;
        height: 22px;
        border-radius: 11px;
        background-color: {colors.border_primary};
    }}

    QCheckBox::indicator:checked {{
        background-color: {colors.accent_primary};
    }}

    /* === ToolTip === */
    QToolTip {{
        background-color: {colors.background_elevated};
        color: {colors.text_primary};
        border: 1px solid {colors.border_primary};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}
    """
