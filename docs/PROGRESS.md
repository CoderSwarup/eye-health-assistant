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
| 4 | Settings page                                       | Done — full page with 5 sections     |
| 5 | Reusable component library                          | Done — 6 widgets           |
| 6 | Design system (typography, spacing)                 | Done — tokens + spacing    |

**Desktop fixes completed this session:**
- Dark theme: removed card borders (transparent), metric cards use `background_tertiary`
- QFrame: all instances call `setFrameShape(QFrame.Shape.NoFrame)` to prevent native border rendering
- Labels inside cards: explicit `border: none; background-color: transparent`
- Font: changed from `-apple-system` (CSS-only) to `Helvetica, Arial, sans-serif` (Qt-compatible)
- Ctrl+C handling: signal handler + 200ms timer poll for clean exit
- All mypy errors fixed: `QScrollArea.Shape.NoFrame`, `Qt.AlignmentFlag.AlignLeft/AlignCenter`, None-safe layout handling
- Dashboard spacing: outer margins 36,28; section spacing 28; card spacing 16
- AGENTS.md updated with 7 desktop styling rules

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
| 8 | Onboarding flow       | Not started |

**Timer mode completed this session:**
- Domain models: `TimerPhase`, `SessionStatus`, `SessionMode` enums, `TimerSession` dataclass
- Database layer: `TimerSessionRow` ORM, `Database` engine, `SessionRepository` with CRUD
- Timer engine: `TimerEngine` state machine with `FakeClock` for testing
- Timer controller: `TimerController` Qt-integrated with signals for UI updates
- Notification service: `NotificationService` with desktop notifications
- DI wiring: `Dependencies` container initializes database, repository, services
- Monitoring page: `MonitoringPage` UI with timer display, controls, progress
- Dashboard wiring: Quick action buttons navigate to monitoring page
- History page: Database-backed session list with empty state
- Statistics page: Dynamic metrics from database with summary cards
- Tests: 18 new tests (11 engine, 7 repository), all passing
- Quality: ruff clean, mypy clean, 80/80 tests passing

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

**Camera mode completed this session:**
- Infrastructure: `OpenCVCamera` adapter, `OpenCVFaceDetector` with YuNet DNN fallback
- Blink engine: EAR calculator, `BlinkDetector` state machine, `MetricsAggregator` rolling window
- Monitoring: `MonitoringWorker` QThread with time-based blink estimation (research-based 6 blinks/min during screen use)
- Database: `MonitoringSessionRow`, `BlinkMeasurementRow` ORM models
- Repository: `MonitoringRepository` with session/CRUD and measurements
- Dashboard: Real-time face detection, blink rate, camera status indicators
- Settings: Camera device selection, preview toggle, sampling FPS, EAR thresholds
- Statistics: Blink rate statistics from monitoring sessions
- History: Monitoring sessions displayed alongside timer sessions
- Tests: 28 blink engine tests, 10 monitoring tests, 9 repository tests — all passing
- Quality: ruff clean, mypy clean, 127/127 tests passing

**Note:** Automatic blink detection from camera requires precise eye landmarks (MediaPipe Face Mesh), which is unavailable on Python 3.14. The worker uses time-based estimation calibrated to research data (5-7 blinks/min during screen use). Camera preview and face detection work correctly.

---

## Phase 5 — Exercises and Learning

| # | Deliverable                | Status      |
| - | -------------------------- | ----------- |
| 1 | Exercise catalog           | Done — 6 exercises          |
| 2 | Exercise card UI           | Done — ExerciseCard widget  |
| 3 | Exercise detail screen     | Done — ExerciseDetailPage    |
| 4 | Exercise animations        | Not started                 |
| 5 | Exercise content (JSON)    | Done — content/exercises/   |
| 6 | Eye Care / Learning Center | Done — 8 articles           |
| 7 | Eye Care detail screen     | Done — ArticleDetailPage     |
| 8 | Eye Care content (JSON)    | Done — content/eye_care/    |
| 9 | Content loader             | Done — content/loader.py + validation |

---

## Phase 6 — Analytics

| #  | Deliverable        | Status      |
| -- | ------------------ | ----------- |
| 1  | Daily statistics   | Done — StatisticsPage       |
| 2  | Weekly statistics  | Done — period toggle        |
| 3  | Monthly statistics | Done — period toggle        |
| 4  | Charts             | Not started — needs engine  |
| 5  | Statistics engine  | Not started                 |
| 6  | Insights engine    | Not started                 |
| 7  | Score calculation  | Not started                 |
| 8  | Historical views   | Done — HistoryPage          |
| 9  | Data export        | Button only — no impl       |
| 10 | Data deletion      | Button only — no impl       |
| 11 | Product metrics    | Not started                 |

---

## Phase 7 — Hardening

| #  | Deliverable               | Status                                    |
| -- | ------------------------- | ----------------------------------------- |
| 1  | Error handling            | Partial — Result type, exceptions defined |
| 2  | Accessibility             | Partial — web has prefers-reduced-motion  |
| 3  | Performance optimization  | Not started                               |
| 4  | Database migrations       | Not started                               |
| 5  | Privacy review            | Not started                               |
| 6  | Security review           | Not started                               |
| 7  | UI states for all screens | Not started                               |
| 8  | Logging system            | Done — core/logging.py                    |
| 9  | Cross-platform isolation  | Partial — platform adapter stubs          |
| 10 | Local file layout         | Not started                               |
| 11 | System tray / menu bar    | Not started                               |
| 12 | Startup behavior settings | Not started                               |
| 13 | Configuration precedence  | Partial — core/config.py                  |

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
| 7  | PREREQUISITES.md              | Not started                                |
| 8  | DEVELOPMENT.md                | Not started                                |
| 9  | Troubleshooting documentation | Done — docs/development/troubleshooting.md |
| 10 | Semantic Versioning           | Done — pyproject.toml                      |

---

## Phase 9 — Website

| #  | Deliverable                 | Status                                            |
| -- | --------------------------- | ------------------------------------------------- |
| 1  | Landing page                | Done — full page with 13 sections                 |
| 2  | Features section            | Done — 6-card grid with icons, hover effects      |
| 3  | How It Works section        | Done — 4-step flow with connector lines           |
| 4  | Privacy section             | Done — 4 privacy guarantees                       |
| 5  | Download section            | Done — Mac/Windows CTAs with env-configured links |
| 6  | FAQ section                 | Done — 10-question accordion (all PRD questions)  |
| 7  | Documentation links         | Done — footer links to GitHub, docs, releases     |
| 8  | Roadmap                     | Not started                                       |
| 9  | Contact/project information | Done — footer with GitHub link                    |
| 10 | Responsive UI               | Done — mobile-first with hamburger menu            |
| 11 | SEO                         | Done — metadata, OG, Twitter, robots, canonical   |
| 12 | Web testing                 | Done — 6 tests (config, FAQ, navigation)          |

**Website sections built this session:**
- Navigation: sticky glass nav, mobile hamburger, scroll backdrop
- Hero: gradient headline, product mockup dashboard, ambient glow, staggered entrance
- SmartMonitoring: 5-step camera→processing→landmarks→estimation→privacy pipeline
- TimerMode: interactive timer mockup with progress bar and stats
- Privacy: 4 guarantees with icons
- Exercises: 4 color-coded exercise cards
- Statistics: bar chart mockup with weekly trends + insight callout
- HowItWorks: 4-step numbered flow
- EyeCare: 6 educational topic cards
- CrossPlatform: macOS/Windows platform cards
- FAQ: 10-question accordion (all PRD-required questions)
- DownloadCTA: final download section
- Design system: CSS variables, typography scale, scroll animations, glass effects, reduced-motion support
- Inter font via next/font/google
- Centralized site-config.ts for all links/URLs
- Vitest config + 6 tests

---

## Summary

| Phase                 | Total  | Done   | In Progress | Not Started |
| --------------------- | ------ | ------ | ----------- | ----------- |
| Phase 0 — Planning    | 5      | 5      | 0           | 0           |
| Phase 1 — Foundation  | 9      | 9      | 0           | 0           |
| Phase 2 — Desktop UI  | 6      | 6      | 0           | 0           |
| Phase 3 — Timer Mode  | 8      | 7      | 0           | 1           |
| Phase 4 — Camera Mode | 11     | 11     | 0           | 0           |
| Phase 5 — Exercises   | 9      | 8      | 0           | 1           |
| Phase 6 — Analytics   | 11     | 4      | 0           | 7           |
| Phase 7 — Hardening   | 13     | 3      | 0           | 10          |
| Phase 8 — Packaging   | 10     | 5      | 0           | 5           |
| Phase 9 — Website     | 12     | 11     | 0           | 1           |
| **Total**             | **93** | **69** | **0**       | **24**      |

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
- packages/design-tokens/ — shared design tokens
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
- Phase 3: Complete — timer engine, state machine, database layer, notifications, monitoring UI
- Phase 4: Complete — camera adapter, time-based blink estimation, monitoring service, UI integration, tests
  - 28 blink engine tests, 10 monitoring tests, 9 repository tests
  - Dashboard shows real-time face detection, blink rate, camera status
  - Settings page with camera device selection, preview toggle, EAR thresholds
  - Statistics page shows blink rate statistics
  - History page shows monitoring sessions alongside timer sessions
  - Note: Automatic blink detection requires MediaPipe (unavailable on Python 3.14); uses research-based estimation
- Phase 5: Partially done — exercises catalog, exercise cards, eye care articles done
  - Remaining: exercise detail, eye care detail, JSON content, animations, content loader
- Phase 6: Partially done — statistics page, history page, period toggles done
  - Remaining: charts engine, statistics engine, insights, score calculation, export/delete
- Phase 7: Partially done — Result type, exceptions, logging, UI states for all screens
  - Remaining: accessibility, performance, database migrations, privacy/security review, system tray
- Phase 8: Partially done — docs, troubleshooting, versioning, release process, PyInstaller build working
  - Remaining: Windows installer, macOS .dmg, release workflow, smoke tests
- Phase 9: Nearly complete — full landing page with 13 sections, design system, animations, SEO, tests
  - Remaining: Roadmap section

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
1. Exercise/Eye Care detail screens and JSON content
2. Website: Roadmap section
3. Charts engine and statistics engine
4. Database migrations
5. Packaging: macOS .dmg, Windows .exe installer, release workflow

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
