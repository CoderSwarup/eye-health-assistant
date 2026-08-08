"""Article domain models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ArticleSection:
    """A structured section within an article."""

    title: str
    content: str
    type: str = "text"


@dataclass(frozen=True)
class ArticleSource:
    """A reference source for an article."""

    title: str
    organization: str
    url: str = ""
    published_at: str = ""


@dataclass(frozen=True)
class Article:
    """An eye care article with structured sections and metadata."""

    id: str
    slug: str
    title: str
    summary: str
    category: str
    tags: list[str] = field(default_factory=list)
    reading_time_minutes: int = 3
    difficulty: str = "Beginner"
    featured: bool = False
    order: int = 0
    hero: str = ""
    sections: list[ArticleSection] = field(default_factory=list)
    quick_tips: list[str] = field(default_factory=list)
    related_exercises: list[str] = field(default_factory=list)
    sources: list[ArticleSource] = field(default_factory=list)
    disclaimer: str = (
        "This content is for general educational and wellness purposes "
        "and is not a medical diagnosis or substitute for professional eye care."
    )
    content_version: str = "1.0"
    updated_at: str = ""
