"""Exercise animation system.

Provides a reusable animation engine for eye exercise visualizations.
"""

from eye_health_assistant.ui.animations.engine import (
    AnimationEngine,
    AnimationState,
    BlinkAnimation,
    LookAwayAnimation,
    NearFarAnimation,
    create_animation,
)

__all__ = [
    "AnimationEngine",
    "AnimationState",
    "BlinkAnimation",
    "LookAwayAnimation",
    "NearFarAnimation",
    "create_animation",
]
