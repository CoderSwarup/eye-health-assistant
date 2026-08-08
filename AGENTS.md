# AGENTS.md

Instructions for AI coding agents working on Eye Health Assistant.

## First Rule

Read `EYE_CARE_PRD.md` before making any architectural or product decision.
The PRD is the single source of truth. Never invent requirements that conflict
with it.

## Architecture

This is a **monorepo** with two independent applications:

```
apps/desktop/   → Python + PySide6 desktop app
apps/web/       → Next.js 16 landing website
```

The desktop app uses a **layered architecture**:

```
UI  →  Application  →  Domain  →  Infrastructure
```

### Layer Rules

| Layer | Contains | Must NOT contain |
|-------|----------|-----------------|
| UI | Windows, pages, widgets, themes, navigation | Database queries, CV algorithms, business logic |
| Application | Use cases, commands, queries, DTOs | UI widgets, infrastructure details |
| Domain | Models, enums, value objects, services | UI code, infrastructure code |
| Infrastructure | SQLite repos, camera adapters, notifications | Business logic |

### File Locations

```
src/eye_health_assistant/
├── app/            # Bootstrap, lifecycle, dependencies
├── core/           # Config, constants, exceptions, logging, Result type
├── domain/         # Models, enums, value objects, services
├── application/    # Use cases, commands, queries, DTOs
├── infrastructure/ # Database, camera, CV, notifications, filesystem
├── monitoring/     # Monitoring engine
├── blink/          # Blink detection
├── timer/          # Timer engine
├── analytics/      # Statistics, insights, scoring
├── exercises/      # Exercise catalog
├── content/        # Educational content loader
├── settings/       # Settings management
├── notifications/  # Notification service
└── ui/             # PySide6 UI layer
    ├── main_window.py
    ├── pages/
    ├── widgets/
    ├── dialogs/
    ├── themes/
    └── animations/
```

## Tech Stack — Do NOT Change

| Component | Technology | Required |
|-----------|-----------|----------|
| Desktop GUI | PySide6 | Yes |
| Camera | OpenCV | Optional `[camera]` extra |
| Face/Eye landmarks | MediaPipe | Optional `[camera]` extra |
| Numerical | NumPy | Yes |
| Database | SQLite via SQLAlchemy | Yes |
| Web frontend | Next.js 16 + React 19 | Yes |
| CSS | Tailwind CSS v4 | Yes |
| Python linter | Ruff | Yes |
| Python types | mypy | Yes |
| Python tests | pytest | Yes |
| Web linter | ESLint 9 (flat config) | Yes |
| Web types | TypeScript 5.7+ | Yes |
| Web tests | Vitest | Yes |

## Privacy Rules — Non-Negotiable

1. **Never persist webcam frames.** Process in memory only.
2. **Never upload camera data.** All processing is local.
3. **Never make medical or diagnostic claims.** Use "estimated", "wellness".
4. **Camera permission must be explicit.** Never silently request it.
5. **User data stays local.** No cloud accounts, no telemetry by default.
6. **Camera status must always be visible** in the UI when active.

## Code Rules

### Python

- Use type hints on all functions
- Use `from __future__ import annotations`
- Keep functions focused and small
- Prefer composition over inheritance
- Use the `Result` type (`Ok`/`Err`) for operations that can fail
- No database queries in UI code
- No computer vision algorithms in UI code

### TypeScript / React

- Use strict TypeScript
- Use App Router (not Pages Router)
- Use Tailwind CSS v4 for styling
- Use ESLint flat config (`eslint.config.mjs`)
- No `next lint` — use `eslint .` directly (Next.js 16 removed `next lint`)

### Desktop Styling (PySide6) — Critical Rules

These rules prevent the "line line" border-inheritance bugs. Follow them exactly.

1. **Global QWidget rule: NO borders.** Only set `background-color`, `color`, `font-family`, `font-size`. Never put `border` on `QWidget {{ }}` — it inherits to every child widget including QLabels inside cards.

2. **Labels inside cards must be explicitly borderless.** Always add this rule in `generate_stylesheet`:
   ```css
   #card QLabel, #metric-card QLabel {
       background-color: transparent;
       border: none;
   }
   ```

3. **Card object names:**
   - `#card` — main container cards (Live Monitoring, Recent Activity, etc.)
   - `#metric-card` — stat cards (Screen Time, Blink Rate, etc.)
   - Metric cards use `background_tertiary` color with `border: none`
   - Main cards use `card_bg` color with optional subtle `card_border`

4. **Font family: Qt-compatible only.** Use `Helvetica, Arial, sans-serif`. Never use CSS-only aliases like `-apple-system`, `BlinkMacSystemFont`, or `SF Pro Text` — Qt doesn't recognize them and emits warnings.

5. **Layout spacing rules:**
   - Page outer margins: `36, 28, 36, 28`
   - Section spacing: `28px`
   - Card grid spacing: `16px`
   - Card inner padding: `24px` (via stylesheet, not setContentsMargins)
   - Button spacing: `10px`
   - All card layouts: `setContentsMargins(0, 0, 0, 0)` — padding comes from stylesheet only

6. **Adding a new page:** Follow `dashboard.py` as the reference implementation. Use `MetricCard` for stats, `QFrame` with `#card` for containers. Never set borders directly on widgets.

7. **QFrame rule:** All `QFrame` instances must call `setFrameShape(QFrame.Shape.NoFrame)` in the constructor. Qt's default frame style draws borders even when the stylesheet says `border: none`. This is the primary cause of "line line" artifacts.

### Web Styling (Tailwind CSS v4) — Critical Rules

1. **`globals.css` must be imported in `layout.tsx`.** Without this import, Tailwind CSS is never loaded and you get raw unstyled HTML. Always have `import './globals.css';` in `app/layout.tsx`.

2. **globals.css content:** Only `@import 'tailwindcss';` — nothing else needed for Tailwind v4.

3. **PostCSS config:** Use `@tailwindcss/postcss` plugin (not the old `tailwindcss` plugin). Config in `postcss.config.mjs`:
   ```js
   const config = { plugins: { '@tailwindcss/postcss': {} } };
   ```

### General

- Never add cloud services without explicit approval
- Never add secrets or API keys to source code
- Use platform-aware paths (no hardcoded `C:\` or `/Users/`)
- Follow existing naming conventions in the codebase

## Testing Rules

### Python Tests

```bash
cd apps/desktop && pytest              # Run all
cd apps/desktop && pytest -v           # Verbose
cd apps/desktop && pytest tests/unit/  # Unit only
```

- Test business logic in isolation
- Use mocks for camera and platform code
- Never depend on a physical camera in tests
- Use deterministic fixtures

### Web Tests

```bash
cd apps/web && npm test
```

### Quality Checks Before Declaring Done

```bash
make check   # Runs: lint + test
```

This runs `ruff check`, `mypy`, `pytest`, and `eslint`. All must pass.

## Making Changes

### Adding a New Page

1. Create `src/eye_health_assistant/ui/pages/your_page.py`
2. Add a `YourPage(QWidget)` class
3. Register it in `ui/main_window.py` `_create_pages()`
4. Add nav entry in `_build_sidebar()`

### Adding a Database Model

1. Define model in `domain/models/`
2. Create repository in `infrastructure/database/`
3. Add to application layer service
4. Write integration tests

### Adding an Exercise

1. Add JSON content file in `content/exercises/`
2. Update exercise catalog in `exercises/catalog.py`
3. Add UI card in exercises page

### Adding an Eye Care Article

1. Add JSON content file in `content/eye_care/`
2. Update content loader in `content/loader.py`

### Adding a Notification

1. Define notification type in `notifications/`
2. Add policy logic in `notifications/policies.py`
3. Wire into monitoring/timer services

## Common Mistakes to Avoid

- Putting business logic in UI widgets
- Importing infrastructure in the domain layer
- Writing SQL directly in UI code
- Making medical claims in UI text
- Adding cloud dependencies
- Persisting camera frames
- Skipping tests to move faster
- Rewriting working code unnecessarily
- Putting `border` on global `QWidget` rule (causes line-inheritance bug)
- Using CSS-only fonts like `-apple-system` in Qt stylesheets
- Forgetting to import `globals.css` in Next.js `layout.tsx`
- Not calling `setContentsMargins(0,0,0,0)` on card layouts

## Commands Reference

```bash
make help              # List all commands
make install           # Install all dependencies
make check             # Full quality check (lint + test)
make format            # Format all code
make lint              # Run all linters
make test              # Run all tests
make build-desktop     # Build desktop app
make build-web         # Build web app
make clean             # Clean build artifacts
```
