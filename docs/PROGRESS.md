# Eye Health Assistant — Progress Tracker

This document tracks the completion status of every deliverable defined in the
PRD. Last updated: 2026-08-08

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
| 4 | Settings page                                       | Not started                |
| 5 | Reusable component library                          | Partial — MetricCard only  |
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
| 1 | Timer engine          | Not started |
| 2 | Timer presets         | Not started |
| 3 | Timer scheduler       | Not started |
| 4 | Break flow            | Not started |
| 5 | Notification system   | Not started |
| 6 | History               | Not started |
| 7 | SQLite database layer | Not started |
| 8 | Onboarding flow       | Not started |

---

## Phase 4 — Camera Mode (Smart Mode)

| #  | Deliverable                  | Status      |
| -- | ---------------------------- | ----------- |
| 1  | Camera permission handling   | Not started |
| 2  | OpenCV adapter               | Not started |
| 3  | MediaPipe adapter            | Not started |
| 4  | Blink detection engine       | Not started |
| 5  | Blink-rate calculator        | Not started |
| 6  | Blink smoothing              | Not started |
| 7  | Monitoring service           | Not started |
| 8  | Live Monitoring screen       | Not started |
| 9  | Privacy controls             | Not started |
| 10 | Low-blink notification logic | Not started |
| 11 | Thread/worker architecture   | Not started |

---

## Phase 5 — Exercises and Learning

| # | Deliverable                | Status      |
| - | -------------------------- | ----------- |
| 1 | Exercise catalog           | Not started |
| 2 | Exercise card UI           | Not started |
| 3 | Exercise detail screen     | Not started |
| 4 | Exercise animations        | Not started |
| 5 | Exercise content (JSON)    | Not started |
| 6 | Eye Care / Learning Center | Not started |
| 7 | Eye Care detail screen     | Not started |
| 8 | Eye Care content (JSON)    | Not started |
| 9 | Content loader             | Not started |

---

## Phase 6 — Analytics

| #  | Deliverable        | Status      |
| -- | ------------------ | ----------- |
| 1  | Daily statistics   | Not started |
| 2  | Weekly statistics  | Not started |
| 3  | Monthly statistics | Not started |
| 4  | Charts             | Not started |
| 5  | Statistics engine  | Not started |
| 6  | Insights engine    | Not started |
| 7  | Score calculation  | Not started |
| 8  | Historical views   | Not started |
| 9  | Data export        | Not started |
| 10 | Data deletion      | Not started |
| 11 | Product metrics    | Not started |

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
| Phase 2 — Desktop UI  | 6      | 4      | 0           | 2           |
| Phase 3 — Timer Mode  | 8      | 0      | 0           | 8           |
| Phase 4 — Camera Mode | 11     | 0      | 0           | 11          |
| Phase 5 — Exercises   | 9      | 0      | 0           | 9           |
| Phase 6 — Analytics   | 11     | 0      | 0           | 11          |
| Phase 7 — Hardening   | 13     | 3      | 0           | 10          |
| Phase 8 — Packaging   | 10     | 5      | 0           | 5           |
| Phase 9 — Website     | 12     | 11     | 0           | 1           |
| **Total**             | **93** | **37** | **0**       | **56**      |

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
- Phase 2: Mostly complete — dashboard, theme, navigation done; dark theme polished; all mypy errors fixed
  - Remaining: Settings page, full component library
- Phase 3-7: Not started (Timer, Camera, Exercises, Analytics, Hardening)
- Phase 8: Partially done — docs, troubleshooting, versioning, release process, PyInstaller build working
  - Remaining: Windows installer, macOS .dmg, release workflow, smoke tests, PREREQUISITES.md, DEVELOPMENT.md
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
1. Desktop: Settings page
2. Desktop: Remaining dashboard pages (exercises, eye care, statistics, history)
3. SQLite database layer (SQLAlchemy models, repositories)
4. Timer mode (engine, presets, scheduler, break flow)
5. Notification system
6. Website: Roadmap section
7. Smart Mode (camera, blink detection, monitoring)
8. Packaging: macOS .dmg, Windows .exe installer, release workflow

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

IMPORTANT RULE — Update Progress After Every Change:
After completing ANY work (new feature, bug fix, refactor, etc.):
1. Update docs/PROGRESS.md — mark the deliverable as Done, update the Status column
2. Update the Summary table — recalculate Done/In Progress/Not Started counts
3. Update the Recall Prompt — reflect the new current state and next priorities
4. Keep the file accurate so any AI agent can pick up where you left off
This is mandatory. Never leave PROGRESS.md stale after making changes.
```
