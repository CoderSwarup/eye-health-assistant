"""Content validation — validates JSON content against schemas."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}
VALID_EXERCISE_CATEGORIES = {
    "Blinking",
    "Distance Viewing",
    "Focus Shifting",
    "Eye Rest",
    "Warm-Up",
    "Guided Break",
}
VALID_ARTICLE_CATEGORIES = {
    "Screen Habits",
    "Breaks",
    "Blinking",
    "Workspace",
    "Lighting",
    "Screen Position",
    "Environment",
    "Wellness",
    "Guidance",
}
VALID_ANIMATION_TYPES = {
    "blink",
    "look_away",
    "distance_focus",
    "eye_rolling",
    "palming",
    "figure_eight",
    "near_far",
}
VALID_SECTION_TYPES = {"text", "list", "checklist", "tip"}


@dataclass(frozen=True)
class ValidationError:
    """A single validation error."""

    field: str
    message: str
    item_id: str = ""


def validate_article(data: dict, index: int = 0) -> list[ValidationError]:
    """Validate a single article dictionary. Returns list of errors."""
    errors: list[ValidationError] = []
    item_id = data.get("id", f"article_{index}")

    required = ["id", "slug", "title", "summary", "category"]
    for field_name in required:
        if field_name not in data:
            errors.append(
                ValidationError(
                    field=field_name, message="required", item_id=item_id
                )
            )

    if "category" in data and data["category"] not in VALID_ARTICLE_CATEGORIES:
        errors.append(
            ValidationError(
                field="category",
                message=f"invalid category: {data['category']}",
                item_id=item_id,
            )
        )

    if "reading_time_minutes" in data:
        val = data["reading_time_minutes"]
        if not isinstance(val, int) or val < 1:
            errors.append(
                ValidationError(
                    field="reading_time_minutes",
                    message="must be a positive integer",
                    item_id=item_id,
                )
            )

    if "sections" in data and isinstance(data["sections"], list):
        for i, section in enumerate(data["sections"]):
            if not isinstance(section, dict):
                errors.append(
                    ValidationError(
                        field=f"sections[{i}]",
                        message="must be a dict",
                        item_id=item_id,
                    )
                )
                continue
            for sf in ["title", "content"]:
                if sf not in section:
                    errors.append(
                        ValidationError(
                            field=f"sections[{i}].{sf}",
                            message="required",
                            item_id=item_id,
                        )
                    )
            if "type" in section and section["type"] not in VALID_SECTION_TYPES:
                errors.append(
                    ValidationError(
                        field=f"sections[{i}].type",
                        message=f"invalid type: {section['type']}",
                        item_id=item_id,
                    )
                )

    if "sources" in data and isinstance(data["sources"], list):
        for i, source in enumerate(data["sources"]):
            if not isinstance(source, dict):
                errors.append(
                    ValidationError(
                        field=f"sources[{i}]",
                        message="must be a dict",
                        item_id=item_id,
                    )
                )
                continue
            for sf in ["title", "organization"]:
                if sf not in source:
                    errors.append(
                        ValidationError(
                            field=f"sources[{i}].{sf}",
                            message="required",
                            item_id=item_id,
                        )
                    )

    return errors


def validate_exercise(data: dict, index: int = 0) -> list[ValidationError]:
    """Validate a single exercise dictionary. Returns list of errors."""
    errors: list[ValidationError] = []
    item_id = data.get("id", f"exercise_{index}")

    required = ["id", "slug", "title", "description", "category", "duration_seconds"]
    for field_name in required:
        if field_name not in data:
            errors.append(
                ValidationError(
                    field=field_name, message="required", item_id=item_id
                )
            )

    if "category" in data and data["category"] not in VALID_EXERCISE_CATEGORIES:
        errors.append(
            ValidationError(
                field="category",
                message=f"invalid category: {data['category']}",
                item_id=item_id,
            )
        )

    if "difficulty" in data and data["difficulty"] not in VALID_DIFFICULTIES:
        errors.append(
            ValidationError(
                field="difficulty",
                message=f"invalid difficulty: {data['difficulty']}",
                item_id=item_id,
            )
        )

    if "duration_seconds" in data:
        val = data["duration_seconds"]
        if not isinstance(val, int) or val < 1:
            errors.append(
                ValidationError(
                    field="duration_seconds",
                    message="must be a positive integer",
                    item_id=item_id,
                )
            )

    if "steps" in data and isinstance(data["steps"], list):
        for i, step in enumerate(data["steps"]):
            if not isinstance(step, dict):
                errors.append(
                    ValidationError(
                        field=f"steps[{i}]",
                        message="must be a dict",
                        item_id=item_id,
                    )
                )
                continue
            for sf in ["title", "instruction", "duration_seconds"]:
                if sf not in step:
                    errors.append(
                        ValidationError(
                            field=f"steps[{i}].{sf}",
                            message="required",
                            item_id=item_id,
                        )
                    )

    if "animation" in data and isinstance(data["animation"], dict):
        anim_type = data["animation"].get("type", "")
        if anim_type not in VALID_ANIMATION_TYPES:
            errors.append(
                ValidationError(
                    field="animation.type",
                    message=f"invalid animation type: {anim_type}",
                    item_id=item_id,
                )
            )

    return errors


def validate_articles(data: list[dict]) -> list[ValidationError]:
    """Validate all articles. Returns list of errors."""
    errors: list[ValidationError] = []
    ids: set[str] = set()

    for i, item in enumerate(data):
        errors.extend(validate_article(item, i))
        item_id = item.get("id", "")
        if item_id in ids:
            errors.append(
                ValidationError(
                    field="id",
                    message=f"duplicate id: {item_id}",
                    item_id=item_id,
                )
            )
        ids.add(item_id)

    return errors


def validate_exercises(data: list[dict]) -> list[ValidationError]:
    """Validate all exercises. Returns list of errors."""
    errors: list[ValidationError] = []
    ids: set[str] = set()

    for i, item in enumerate(data):
        errors.extend(validate_exercise(item, i))
        item_id = item.get("id", "")
        if item_id in ids:
            errors.append(
                ValidationError(
                    field="id",
                    message=f"duplicate id: {item_id}",
                    item_id=item_id,
                )
            )
        ids.add(item_id)

    return errors
