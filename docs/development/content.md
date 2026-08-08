# Content System

This document describes the content architecture for the Eye Health Assistant desktop application.

## Overview

Content is stored as JSON files and loaded at runtime by the content loader. The system supports:

- Eye care articles with structured sections
- Eye exercises with guided steps
- Category filtering
- Cross-linking between articles and exercises
- Content validation at load time

## File Structure

```
content/
├── __init__.py
├── loader.py          # Content loading API
├── validation.py      # Schema validation
├── eye_care/
│   └── eye_care.json  # All articles
└── exercises/
    └── exercises.json # All exercises
```

## Domain Models

### Article

```python
@dataclass(frozen=True)
class Article:
    id: str
    slug: str
    title: str
    summary: str
    category: str
    tags: list[str]
    reading_time_minutes: int
    difficulty: str
    featured: bool
    order: int
    hero: str
    sections: list[ArticleSection]
    quick_tips: list[str]
    related_exercises: list[str]
    sources: list[ArticleSource]
    disclaimer: str
    content_version: str
    updated_at: str
```

### Exercise

```python
@dataclass(frozen=True)
class Exercise:
    id: str
    slug: str
    title: str
    short_title: str
    description: str
    purpose: str
    category: str
    difficulty: str
    duration_seconds: int
    recommended_frequency: str
    steps: list[ExerciseStep]
    safety_note: str
    animation: ExerciseAnimation
    completion_message: str
    related_articles: list[str]
    tags: list[str]
    content_version: str
    updated_at: str
```

## Adding an Article

1. Add a new entry to `content/eye_care/eye_care.json`
2. Use a stable semantic ID and slug
3. Include at least one section with `title` and `content`
4. Set `related_exercises` to exercise slugs where relevant
5. Include `sources` for factual health claims
6. The content validator will check required fields at load time

## Adding an Exercise

1. Add a new entry to `content/exercises/exercises.json`
2. Use a stable semantic ID and slug
3. Include structured steps with `title`, `instruction`, and `duration_seconds`
4. Set `related_articles` to article slugs where relevant
5. Include `safety_note` if appropriate
6. Set `animation.type` to one of: `blink`, `look_away`, `distance_focus`, `eye_rolling`, `palming`, `figure_eight`, `near_far`

## Adding a Category

1. Add the category to the JSON file's `category` field
2. Add it to `VALID_ARTICLE_CATEGORIES` or `VALID_EXERCISE_CATEGORIES` in `validation.py`
3. The filter UI will pick it up automatically

## Content Validation

Validation runs automatically when content is loaded. Invalid content returns an error instead of crashing the app.

Validate manually:

```python
from eye_health_assistant.content.loader import load_articles, load_exercises

articles = load_articles()  # Returns Result[list[Article], ContentError]
exercises = load_exercises()
```

## Cross-Linking

Articles reference exercises by slug:

```json
{
  "related_exercises": ["gentle-blinking", "distance-viewing"]
}
```

Exercises reference articles by slug:

```json
{
  "related_articles": ["20-20-20-rule", "healthy-blinking-habits"]
}
```

The detail pages render related content automatically.

## Animation Types

| Type | Description |
|------|-------------|
| `blink` | Blinking animation |
| `look_away` | Looking at a distant object |
| `distance_focus` | Focusing on far objects |
| `eye_rolling` | Circular eye movements |
| `palming` | Palms over closed eyes |
| `figure_eight` | Tracing infinity pattern |
| `near_far` | Shifting focus near to far |

The UI layer interprets these types. Content describes what should happen, not how to render it.

## Content Versioning

Every content object has a `content_version` field (default `"1.0"`). This supports future content migrations without breaking historical records.
