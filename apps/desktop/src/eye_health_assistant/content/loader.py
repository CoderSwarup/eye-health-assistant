"""Content loader — reads, validates, and returns domain models from JSON files."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from eye_health_assistant.content.validation import (
    validate_articles,
    validate_exercises,
)
from eye_health_assistant.core.result import Err, Ok, Result
from eye_health_assistant.domain.models.article import (
    Article,
    ArticleSection,
    ArticleSource,
)
from eye_health_assistant.domain.models.exercise import (
    Exercise,
    ExerciseAnimation,
    ExerciseStep,
)

logger = logging.getLogger(__name__)

_CONTENT_DIR = Path(__file__).parent


class ContentError(Exception):
    """Error loading or validating content."""


def _parse_article(data: dict) -> Article:
    """Parse a raw JSON dict into an Article domain model."""
    sections = [
        ArticleSection(
            title=s.get("title", ""),
            content=s.get("content", ""),
            type=s.get("type", "text"),
        )
        for s in data.get("sections", [])
    ]
    sources = [
        ArticleSource(
            title=s.get("title", ""),
            organization=s.get("organization", ""),
            url=s.get("url", ""),
            published_at=s.get("published_at", ""),
        )
        for s in data.get("sources", [])
    ]
    return Article(
        id=data["id"],
        slug=data.get("slug", data["id"]),
        title=data["title"],
        summary=data.get("summary", ""),
        category=data.get("category", ""),
        tags=data.get("tags", []),
        reading_time_minutes=data.get("reading_time_minutes", 3),
        difficulty=data.get("difficulty", "Beginner"),
        featured=data.get("featured", False),
        order=data.get("order", 0),
        hero=data.get("hero", ""),
        sections=sections,
        quick_tips=data.get("quick_tips", []),
        related_exercises=data.get("related_exercises", []),
        sources=sources,
        disclaimer=data.get("disclaimer", ""),
        content_version=data.get("content_version", "1.0"),
        updated_at=data.get("updated_at", ""),
    )


def _parse_exercise(data: dict) -> Exercise:
    """Parse a raw JSON dict into an Exercise domain model."""
    steps = [
        ExerciseStep(
            title=s.get("title", ""),
            instruction=s.get("instruction", ""),
            duration_seconds=s.get("duration_seconds", 0),
        )
        for s in data.get("steps", [])
    ]
    anim_data = data.get("animation", {})
    animation = ExerciseAnimation(type=anim_data.get("type", "look_away"))
    return Exercise(
        id=data["id"],
        slug=data.get("slug", data["id"]),
        title=data["title"],
        short_title=data.get("short_title", data["title"]),
        description=data.get("description", ""),
        purpose=data.get("purpose", ""),
        category=data.get("category", ""),
        difficulty=data.get("difficulty", "Beginner"),
        duration_seconds=data.get("duration_seconds", 0),
        recommended_frequency=data.get("recommended_frequency", ""),
        steps=steps,
        safety_note=data.get("safety_note", ""),
        animation=animation,
        completion_message=data.get("completion_message", ""),
        related_articles=data.get("related_articles", []),
        tags=data.get("tags", []),
        content_version=data.get("content_version", "1.0"),
        updated_at=data.get("updated_at", ""),
    )


def load_articles() -> Result[list[Article], ContentError]:
    """Load and validate all eye care articles."""
    path = _CONTENT_DIR / "eye_care" / "eye_care.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return Err(ContentError(f"Content file not found: {path}"))

    errors = validate_articles(raw)
    if errors:
        msgs = [f"{e.item_id}.{e.field}: {e.message}" for e in errors]
        return Err(ContentError(f"Validation: {'; '.join(msgs)}"))

    return Ok([_parse_article(item) for item in raw])


def load_exercises() -> Result[list[Exercise], ContentError]:
    """Load and validate all exercises."""
    path = _CONTENT_DIR / "exercises" / "exercises.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return Err(ContentError(f"Content file not found: {path}"))

    errors = validate_exercises(raw)
    if errors:
        msgs = [f"{e.item_id}.{e.field}: {e.message}" for e in errors]
        return Err(ContentError(f"Validation: {'; '.join(msgs)}"))

    return Ok([_parse_exercise(item) for item in raw])


def get_article_by_slug(slug: str) -> Result[Article, ContentError]:
    """Get a single article by its slug."""
    result = load_articles()
    if isinstance(result, Err):
        return result
    for article in result.value:
        if article.slug == slug:
            return Ok(article)
    return Err(ContentError(f"Article not found: {slug}"))


def get_exercise_by_slug(slug: str) -> Result[Exercise, ContentError]:
    """Get a single exercise by its slug."""
    result = load_exercises()
    if isinstance(result, Err):
        return result
    for exercise in result.value:
        if exercise.slug == slug:
            return Ok(exercise)
    return Err(ContentError(f"Exercise not found: {slug}"))


def get_related_exercises(
    article_slug: str,
) -> Result[list[Exercise], ContentError]:
    """Get exercises related to a given article."""
    article_result = get_article_by_slug(article_slug)
    if isinstance(article_result, Err):
        return article_result
    article = article_result.value
    if not article.related_exercises:
        return Ok([])

    exercises_result = load_exercises()
    if isinstance(exercises_result, Err):
        return exercises_result

    slug_set = set(article.related_exercises)
    return Ok([e for e in exercises_result.value if e.slug in slug_set])


def get_related_articles(
    exercise_slug: str,
) -> Result[list[Article], ContentError]:
    """Get articles related to a given exercise."""
    exercise_result = get_exercise_by_slug(exercise_slug)
    if isinstance(exercise_result, Err):
        return exercise_result
    exercise = exercise_result.value
    if not exercise.related_articles:
        return Ok([])

    articles_result = load_articles()
    if isinstance(articles_result, Err):
        return articles_result

    slug_set = set(exercise.related_articles)
    return Ok([a for a in articles_result.value if a.slug in slug_set])


def get_articles_by_category(
    category: str,
) -> Result[list[Article], ContentError]:
    """Get all articles in a given category."""
    result = load_articles()
    if isinstance(result, Err):
        return result
    return Ok([a for a in result.value if a.category == category])


def get_exercises_by_category(
    category: str,
) -> Result[list[Exercise], ContentError]:
    """Get all exercises in a given category."""
    result = load_exercises()
    if isinstance(result, Err):
        return result
    return Ok([e for e in result.value if e.category == category])


def get_article_categories() -> Result[list[str], ContentError]:
    """Get all unique article categories."""
    result = load_articles()
    if isinstance(result, Err):
        return result
    return Ok(sorted({a.category for a in result.value}))


def get_exercise_categories() -> Result[list[str], ContentError]:
    """Get all unique exercise categories."""
    result = load_exercises()
    if isinstance(result, Err):
        return result
    return Ok(sorted({e.category for e in result.value}))
