"""Tests for content validation and loading."""

from __future__ import annotations

from eye_health_assistant.content.loader import (
    get_article_by_slug,
    get_article_categories,
    get_articles_by_category,
    get_exercise_by_slug,
    get_exercise_categories,
    get_exercises_by_category,
    get_related_articles,
    get_related_exercises,
    load_articles,
    load_exercises,
)
from eye_health_assistant.content.validation import (
    validate_article,
    validate_articles,
    validate_exercise,
)
from eye_health_assistant.core.result import Err, Ok

# --- Validation tests ---


class TestArticleValidation:
    def test_valid_article_passes(self) -> None:
        data = {
            "id": "test-article",
            "slug": "test-article",
            "title": "Test Article",
            "summary": "A test.",
            "category": "Screen Habits",
        }
        errors = validate_article(data)
        assert errors == []

    def test_missing_required_field(self) -> None:
        data = {"id": "test", "title": "Test"}
        errors = validate_article(data)
        fields = {e.field for e in errors}
        assert "slug" in fields
        assert "summary" in fields
        assert "category" in fields

    def test_invalid_category(self) -> None:
        data = {
            "id": "test",
            "slug": "test",
            "title": "Test",
            "summary": "Test",
            "category": "Invalid Category",
        }
        errors = validate_article(data)
        assert any("category" in e.field for e in errors)

    def test_duplicate_ids_detected(self) -> None:
        data = [
            {
                "id": "dup",
                "slug": "dup",
                "title": "A",
                "summary": "A",
                "category": "Screen Habits",
            },
            {
                "id": "dup",
                "slug": "dup-2",
                "title": "B",
                "summary": "B",
                "category": "Breaks",
            },
        ]
        errors = validate_articles(data)
        assert any("duplicate" in e.message for e in errors)


class TestExerciseValidation:
    def test_valid_exercise_passes(self) -> None:
        data = {
            "id": "test-ex",
            "slug": "test-ex",
            "title": "Test Exercise",
            "description": "A test.",
            "category": "Blinking",
            "duration_seconds": 60,
        }
        errors = validate_exercise(data)
        assert errors == []

    def test_missing_required_field(self) -> None:
        data = {"id": "test", "title": "Test"}
        errors = validate_exercise(data)
        fields = {e.field for e in errors}
        assert "slug" in fields
        assert "description" in fields
        assert "category" in fields
        assert "duration_seconds" in fields

    def test_invalid_category(self) -> None:
        data = {
            "id": "test",
            "slug": "test",
            "title": "Test",
            "description": "Test",
            "category": "Invalid",
            "duration_seconds": 60,
        }
        errors = validate_exercise(data)
        assert any("category" in e.field for e in errors)

    def test_invalid_difficulty(self) -> None:
        data = {
            "id": "test",
            "slug": "test",
            "title": "Test",
            "description": "Test",
            "category": "Blinking",
            "duration_seconds": 60,
            "difficulty": "Extreme",
        }
        errors = validate_exercise(data)
        assert any("difficulty" in e.field for e in errors)

    def test_invalid_duration(self) -> None:
        data = {
            "id": "test",
            "slug": "test",
            "title": "Test",
            "description": "Test",
            "category": "Blinking",
            "duration_seconds": -5,
        }
        errors = validate_exercise(data)
        assert any("duration_seconds" in e.field for e in errors)


# --- Loader tests ---


class TestLoadArticles:
    def test_load_returns_ok(self) -> None:
        result = load_articles()
        assert isinstance(result, Ok)
        assert len(result.value) > 0

    def test_articles_have_required_fields(self) -> None:
        result = load_articles()
        assert isinstance(result, Ok)
        for article in result.value:
            assert article.id
            assert article.slug
            assert article.title
            assert article.summary
            assert article.category

    def test_articles_have_sections(self) -> None:
        result = load_articles()
        assert isinstance(result, Ok)
        for article in result.value:
            assert len(article.sections) > 0

    def test_get_article_by_slug(self) -> None:
        result = load_articles()
        assert isinstance(result, Ok)
        slug = result.value[0].slug
        article_result = get_article_by_slug(slug)
        assert isinstance(article_result, Ok)
        assert article_result.value.slug == slug

    def test_get_article_by_missing_slug(self) -> None:
        result = get_article_by_slug("nonexistent")
        assert isinstance(result, Err)

    def test_get_article_categories(self) -> None:
        result = get_article_categories()
        assert isinstance(result, Ok)
        assert len(result.value) > 0

    def test_get_articles_by_category(self) -> None:
        result = get_article_categories()
        assert isinstance(result, Ok)
        category = result.value[0]
        filtered = get_articles_by_category(category)
        assert isinstance(filtered, Ok)
        assert all(a.category == category for a in filtered.value)


class TestLoadExercises:
    def test_load_returns_ok(self) -> None:
        result = load_exercises()
        assert isinstance(result, Ok)
        assert len(result.value) > 0

    def test_exercises_have_required_fields(self) -> None:
        result = load_exercises()
        assert isinstance(result, Ok)
        for ex in result.value:
            assert ex.id
            assert ex.slug
            assert ex.title
            assert ex.description
            assert ex.category
            assert ex.duration_seconds > 0

    def test_exercises_have_steps(self) -> None:
        result = load_exercises()
        assert isinstance(result, Ok)
        for ex in result.value:
            assert len(ex.steps) > 0
            for step in ex.steps:
                assert step.title
                assert step.instruction
                assert step.duration_seconds > 0

    def test_get_exercise_by_slug(self) -> None:
        result = load_exercises()
        assert isinstance(result, Ok)
        slug = result.value[0].slug
        ex_result = get_exercise_by_slug(slug)
        assert isinstance(ex_result, Ok)
        assert ex_result.value.slug == slug

    def test_get_exercise_by_missing_slug(self) -> None:
        result = get_exercise_by_slug("nonexistent")
        assert isinstance(result, Err)

    def test_get_exercise_categories(self) -> None:
        result = get_exercise_categories()
        assert isinstance(result, Ok)
        assert len(result.value) > 0

    def test_get_exercises_by_category(self) -> None:
        result = get_exercise_categories()
        assert isinstance(result, Ok)
        category = result.value[0]
        filtered = get_exercises_by_category(category)
        assert isinstance(filtered, Ok)
        assert all(e.category == category for e in filtered.value)


# --- Cross-linking tests ---


class TestCrossLinking:
    def test_related_exercises_for_article(self) -> None:
        articles = load_articles()
        assert isinstance(articles, Ok)
        article = articles.value[0]
        if article.related_exercises:
            result = get_related_exercises(article.slug)
            assert isinstance(result, Ok)
            slugs = {e.slug for e in result.value}
            for rel in article.related_exercises:
                assert rel in slugs

    def test_related_articles_for_exercise(self) -> None:
        exercises = load_exercises()
        assert isinstance(exercises, Ok)
        exercise = exercises.value[0]
        if exercise.related_articles:
            result = get_related_articles(exercise.slug)
            assert isinstance(result, Ok)
            slugs = {a.slug for a in result.value}
            for rel in exercise.related_articles:
                assert rel in slugs

    def test_no_circular_reference_errors(self) -> None:
        articles = load_articles()
        exercises = load_exercises()
        assert isinstance(articles, Ok)
        assert isinstance(exercises, Ok)
        article_slugs = {a.slug for a in articles.value}
        exercise_slugs = {e.slug for e in exercises.value}
        for article in articles.value:
            for rel in article.related_exercises:
                assert rel in exercise_slugs
        for exercise in exercises.value:
            for rel in exercise.related_articles:
                assert rel in article_slugs
