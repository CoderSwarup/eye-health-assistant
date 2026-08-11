"""Exercise domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ExerciseStep:
    """A single step within an exercise."""

    title: str
    instruction: str
    duration_seconds: int


@dataclass(frozen=True)
class ExerciseAnimation:
    """Animation metadata for an exercise."""

    type: str


@dataclass(frozen=True)
class Exercise:
    """An eye exercise with structured steps and metadata."""

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
    related_articles: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    content_version: str = "1.0"
    updated_at: str = ""


@dataclass(frozen=True)
class ExerciseCompletion:
    """Record of a completed exercise session."""

    id: str
    exercise_id: str
    exercise_slug: str
    started_at: datetime
    completed_at: datetime
    duration_seconds: int
    content_version: str = "1.0"
