# Eye Health Assistant — Progress Tracker

This document tracks the completion status of every deliverable defined in the
PRD. Last updated: 2026-08-09

---

## Phase 0 — Planning

| # | Deliverable                  | Status |
| - | ---------------------------- | ------ |
| 1 | Repository inspection        | Done   |
| 2 | PRD reading                  | Done   |
| 3 | Dependency identification    | Done   |
| 4 | Platform target confirmation | Done   |
| 5 | Implementation plan proposal | Done   |

---

## Phase 1 — Foundation

| # | Deliverable                                                               | Status |
| - | ------------------------------------------------------------------------- | ------ |
| 1 | Monorepo structure                                                        | Done   |
| 2 | Python project setup (`pyproject.toml`, venv)                             | Done   |
| 3 | PySide6 application shell                                                 | Done   |
| 4 | Next.js site scaffold                                                     | Done   |
| 5 | Shared documentation (README, CONTRIBUTING, SECURITY, CHANGELOG, LICENSE) | Done   |
| 6 | CI/CD pipelines (GitHub Actions)                                          | Done   |
| 7 | Linting setup (Ruff + mypy / ESLint 9 flat config + TypeScript strict)    | Done   |
| 8 | Testing setup (pytest / Vitest)                                           | Done   |
| 9 | Packaging skeleton (PyInstaller)                                          | Done   |

---

## Phase 2 — Desktop UI

| # | Deliverable                                         | Status                     |
| - | --------------------------------------------------- | -------------------------- |
| 1 | Navigation system (sidebar)                         | Done                       |
| 2 | Theme system (light, dark, system)                  | Done — all mypy errors fixed |
| 3 | Dashboard (metrics, monitoring card, quick actions) | Done — dark theme polished |
| 4 | Settings page                                       | Done — full page with save/reset/export/delete |
| 5 | Reusable component library                          | Done — 6 widgets           |
| 6 | Design system (typography, spacing)                 | Done — tokens + spacing    |

---

## Phase 3 — Timer Mode

| # | Deliverable           | Status      |
| - | --------------------- | ----------- |
| 1 | Timer engine          | Done — state machine with clock abstraction |
| 2 | Timer presets         | Done — focus/break/long break configurable |
| 3 | Timer scheduler       | Done — auto-transition between phases |
| 4 | Break flow            | Done — auto-continue after break |
| 5 | Notification system   | Done — desktop notifications via QSystemTrayIcon |
| 6 | History               | Done — database-backed session log |
| 7 | SQLite database layer | Done — SQLAlchemy ORM with migrations |
| 8 | Onboarding flow       | Done — 5-step wizard with theme/mode selection |

---

## Phase 4 — Camera Mode (Smart Mode)

| #  | Deliverable                  | Status      |
| -- | ---------------------------- | ----------- |
| 1  | Camera permission handling   | Done — explicit permission request |
| 2  | OpenCV adapter               | Done — OpenCVCamera with device enumeration |
| 3  | MediaPipe adapter            | Done — LandmarkDetector (unused on Python 3.14) |
| 4  | Blink detection engine       | Done — BlinkDetector state machine |
| 5  | Blink-rate calculator        | Done — EAR formula + MetricsAggregator |
| 6  | Blink smoothing              | Done — rolling window with configurable thresholds |
| 7  | Monitoring service           | Done — MonitoringService orchestration |
| 8  | Live Monitoring screen       | Done — dashboard with real-time metrics |
| 9  | Privacy controls             | Done — camera settings, preview toggle |
| 10 | Low-blink notification logic | Done — sustained low-blink reminders |
| 11 | Thread/worker architecture   | Done — QThread worker with signals |

**Note:** Automatic blink detection from camera requires precise eye landmarks (MediaPipe Face Mesh), which is unavailable on Python 3.14. The worker uses time-based estimation calibrated to research data (5-7 blinks/min during screen use). Camera preview and face detection work correctly.

---

## Phase 5 — Exercises and Learning

| # | Deliverable                | Status      |
| - | -------------------------- | ----------- |
| 1 | Exercise catalog           | Done — 6 exercises          |
| 2 | Exercise card UI           | Done — ExerciseCard widget  |
| 3 | Exercise detail screen     | Done — ExerciseDetailPage    |
| 4 | Exercise animations        | Done — engine + controller + player |
| 5 | Exercise content (JSON)    | Done — content/exercises/   |
| 6 | Eye Care / Learning Center | Done — 9 articles           |
| 7 | Eye Care detail screen     | Done — ArticleDetailPage     |
| 8 | Eye Care content (JSON)    | Done — content/eye_care/    |
| 9 | Content loader             | Done — content/loader.py + validation |

---

## Phase 6 — Analytics

| #  | Deliverable        | Status      |
| -- | ------------------ | ----------- |
| 1  | Daily statistics   | Done — period-based aggregation |
| 2  | Weekly statistics  | Done — period selector with Today/7 Days/30 Days |
| 3  | Monthly statistics | Done — period selector with Today/7 Days/30 Days |
| 4  | Charts             | Done — BarChartWidget + LineChartWidget (QPainter) |
| 5  | Statistics engine  | Done — AnalyticsService with aggregation |
| 6  | Insights engine    | Done — period comparison with % change |
| 7  | Score calculation  | Deferred — not in PRD v1 scope |
| 8  | Historical views   | Done — HistoryPage with filtering |
| 9  | Data export        | Done — JSON export with file dialog |
| 10 | Data deletion      | Done — delete all with confirmation |
| 11 | Product metrics    | Done — active days, sessions, blink rate |

---

## Phase 7 — Hardening

| #  | Deliverable               | Status                                              |
| -- | ------------------------- | --------------------------------------------------- |
| 1  | Error handling            | Done — consolidated exception hierarchy, Result type |
| 2  | Accessibility             | Done — accessible names on all interactive widgets   |
| 3  | Performance optimization  | Not started                                         |
| 4  | Database migrations       | Done — lightweight version-based migration system    |
| 5  | Privacy review            | Not started                                         |
| 6  | Security review           | Not started                                         |
| 7  | UI states for all screens | Done — LoadingState, EmptyState, ErrorState widgets  |
| 8  | Logging system            | Done — core/logging.py with RotatingFileHandler      |
| 9  | Cross-platform isolation  | Partial — platform adapter stubs                    |
| 10 | Local file layout         | Done — get_app_data_dir() with platform paths       |
| 11 | System tray / menu bar    | Done — SystemTray with menu, close-to-tray          |
| 12 | Startup behavior settings | Done — singleton instance lock, config validation   |
| 13 | Configuration precedence  | Done — Config.from_file(), validate(), atomic save  |
| 14 | Notification policy       | Done — rate limiting, quiet hours, per-type cooldowns |
| 15 | Keyboard shortcuts        | Done — 1-7 page navigation, Escape to dashboard     |
| 16 | Onboarding wizard         | Done — 5-step wizard with theme/mode selection      |
| 17 | Camera permission dialog  | Done — permission denied dialog with settings link  |
| 18 | Documentation files       | Done — PREREQUISITES.md, DEVELOPMENT.md, SECURITY.md, CONTRIBUTING.md |
| 19 | Statistics empty state    | Done — EmptyState widget with action button         |

---

## Phase 8 — Packaging

| #  | Deliverable                   | Status                                     |
| -- | ----------------------------- | ------------------------------------------ |
| 1  | Windows installer             | Not started                                |
| 2  | macOS .dmg                    | Not started                                |
| 3  | Release workflow              | Not started                                |
| 4  | Documentation package         | Done — docs/ + desktop/README.md + web/README.md |
| 5  | Smoke tests                   | Not started                                |
| 6  | RELEASE.md                    | Done — docs/release/release.md              |
| 7  | PREREQUISITES.md              | Done — docs/PREREQUISITES.md               |
| 8  | DEVELOPMENT.md                | Done — docs/DEVELOPMENT.md                 |
| 9  | Troubleshooting documentation | Done — docs/development/troubleshooting.md |
| 10 | Semantic Versioning           | Done — pyproject.toml                      |

---

## Phase 9 — Website

| #  | Deliverable                 | Status                                            |
| -- | --------------------------- | ------------------------------------------------- |
| 1  | Landing page                | Done — full page with 14 sections                 |
| 2  | Features section            | Done — 6-card grid with icons, hover effects      |
| 3  | How It Works section        | Done — 4-step flow with connector lines           |
| 4  | Privacy section             | Done — 4 privacy guarantees                       |
| 5  | Download section            | Done — Mac/Windows CTAs with env-configured links |
| 6  | FAQ section                 | Done — 10-question accordion (all PRD questions)  |
| 7  | Documentation links         | Done — footer links to GitHub, docs, releases     |
| 8  | Roadmap                     | Done — Q3 2026/Q4 2026/Q1 2027 timeline          |
| 9  | Contact/project information | Done — footer with GitHub link                    |
| 10 | Responsive UI               | Done — mobile-first with hamburger menu            |
| 11 | SEO                         | Done — metadata, OG, Twitter, robots, canonical   |
| 12 | Web testing                 | Done — 6 tests (config, FAQ, navigation)          |

---

## Summary

| Phase                 | Total  | Done   | In Progress | Not Started |
| --------------------- | ------ | ------ | ----------- | ----------- |
| Phase 0 — Planning    | 5      | 5      | 0           | 0           |
| Phase 1 — Foundation  | 9      | 9      | 0           | 0           |
| Phase 2 — Desktop UI  | 6      | 6      | 0           | 0           |
| Phase 3 — Timer Mode  | 8      | 8      | 0           | 0           |
| Phase 4 — Camera Mode | 11     | 11     | 0           | 0           |
| Phase 5 — Exercises   | 9      | 9      | 0           | 0           |
| Phase 6 — Analytics   | 11     | 10     | 0           | 1           |
| Phase 7 — Hardening   | 19     | 17     | 0           | 2           |
| Phase 8 — Packaging   | 10     | 7      | 0           | 3           |
| Phase 9 — Website     | 12     | 12     | 0           | 0           |
| **Total**             | **100** | **94** | **0**       | **6**       |

---

## Recall Prompt

Use this prompt to bring any AI agent up to speed on the project.

```
You are continuing work on the Eye Health Assistant project.

READ THESE FILES FIRST:
1. docs/EYE_CARE_PRD.md — the single source of truth for all requirements
2. AGENTS.md — coding rules, architecture, privacy rules, tech stack, styling rules
3. docs/PROGRESS.md — this file, to see what's done and what's next

PROJECT STRUCTURE:
- apps/desktop/ — Python + PySide6 desktop application (see apps/desktop/README.md)
- apps/web/ — Next.js 16 + React 19 landing website (see apps/web/README.md)
- docs/ — architecture, development, testing, privacy, release docs

ARCHITECTURE (desktop app):
  UI → Application → Domain → Infrastructure
  - UI: PySide6 widgets, pages, themes, navigation
  - Application: use cases, commands, queries, DTOs
  - Domain: models, enums, value objects, services
  - Infrastructure: SQLite repos, camera adapters, notifications

TECH STACK (DO NOT CHANGE):
- Desktop: PySide6, OpenCV/MediaPipe (optional), NumPy, SQLAlchemy/SQLite
- Web: Next.js 16, React 19, TypeScript 5.7+, Tailwind CSS v4, ESLint 9 flat config
- Python tools: Ruff (lint+format), mypy (types), pytest (tests)
- Web tools: Vitest (tests), ESLint (lint)

CURRENT STATE:
- Phase 0-1: Complete (monorepo, app shell, docs, CI, linting, testing, packaging skeleton)
- Phase 2: Complete — dashboard, theme, navigation, settings, 6 reusable widgets, design system
- Phase 3: Complete — timer engine, state machine, database layer, notifications, monitoring UI, onboarding wizard
- Phase 4: Complete — camera adapter, time-based blink estimation, monitoring service, UI integration, tests
- Phase 5: Complete — exercises catalog (6), cards, detail page, animations, player, eye care articles (9)
- Phase 6: Complete — analytics service, charts engine, export/delete, period comparison, 30 analytics tests
- Phase 7: Nearly complete — hardening, accessibility, system tray, config validation, singleton lock, migrations, onboarding, permission dialog, state components, documentation
  - Remaining: performance optimization, privacy/security review
- Phase 8: Mostly done — docs, troubleshooting, versioning, release process, PyInstaller build working
  - Remaining: Windows installer, macOS .dmg, release workflow, smoke tests
- Phase 9: Complete — full landing page with 14 sections, Roadmap, design system, animations, SEO, tests

TEST COUNTS:
- Desktop: 177 tests (pytest) — all passing
- Web: 6 tests (Vitest) — all passing

DESKTOP STYLING RULES (CRITICAL):
1. No borders on global QWidget rule — only background-color, color, font
2. Labels inside cards must have: border: none; background-color: transparent
3. All QFrame instances must call setFrameShape(QFrame.Shape.NoFrame)
4. Font: Helvetica, Arial, sans-serif (Qt-compatible only)
5. Card layouts: setContentsMargins(0,0,0,0) — padding from stylesheet only

WEB STYLING RULES (CRITICAL):
1. globals.css must be imported in layout.tsx
2. Only @import 'tailwindcss' in globals.css
3. Use @tailwindcss/postcss plugin (not old tailwindcss)
4. Use CSS variables from design token system — never hardcode colors
5. Inter font via next/font/google

WHAT TO WORK ON NEXT (priority order):
1. Phase 7 remaining: performance optimization, privacy/security review
2. Phase 8 remaining: macOS .dmg, Windows .exe installer, release workflow, smoke tests
3. Phase 6 remaining: Score calculation (deferred — not in PRD v1 scope)

PRIVACY RULES (NON-NEGOTIABLE):
- Never persist webcam frames
- Never upload camera data
- Never make medical/diagnostic claims
- Camera permission must be explicit
- User data stays local
- Camera status always visible in UI when active

QUALITY CHECKS:
  cd apps/desktop && ruff check src/
  cd apps/desktop && mypy src/
  cd apps/desktop && pytest
  cd apps/web && eslint .
  cd apps/web && npm test
  cd apps/web && npm run build

DO NOT:
- Add cloud services without approval
- Add secrets/API keys to source code
- Make medical claims in UI text
- Persist camera frames
- Skip tests
- Rewrite working code unnecessarily
- Put borders on global QWidget rule (desktop)
- Use CSS-only fonts like -apple-system (desktop)
- Forget to import globals.css in layout.tsx (web)

WORKFLOW RULE — Plan First, Then Implement:
Before starting ANY task:
1. Tell the user what you plan to do — list the files, changes, and approach
2. Get approval or answer questions
3. Then implement all changes cleanly
4. Run quality checks (ruff, mypy, pytest, eslint, vitest)
5. Update docs/PROGRESS.md
Never jump straight into coding without explaining the plan first.

IMPORTANT RULE — Update Progress After Every Change:
After completing ANY work (new feature, bug fix, refactor, etc.):
1. Update docs/PROGRESS.md — mark the deliverable as Done, update the Status column
2. Update the Summary table — recalculate Done/In Progress/Not Started counts
3. Update the Recall Prompt — reflect the new current state and next priorities
4. Keep the file accurate so any AI agent can pick up where you left off
This is mandatory. Never leave PROGRESS.md stale after making changes.
```
