# Eye Health Assistant — Landing Website

The public-facing landing website for Eye Health Assistant. A premium, dark-first, motion-rich product website built with Next.js 16 and React 19.

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Next.js (App Router) | 16.3+ |
| Language | TypeScript | 5.7+ |
| UI Library | React | 19.2+ |
| CSS | Tailwind CSS v4 | 4.0+ |
| PostCSS Plugin | @tailwindcss/postcss | 4.0+ |
| Linter | ESLint 9 (flat config) | 9.0+ |
| Formatter | Prettier | 3.4+ |
| Tests | Vitest | 3.0+ |
| Utilities | clsx | 2.1+ |

## Folder Structure

```
apps/web/
├── app/                              # Next.js App Router
│   ├── globals.css                   # Tailwind CSS v4 entry + design tokens
│   ├── layout.tsx                    # Root layout (Inter font, metadata, body)
│   └── page.tsx                      # Landing page (assembles all sections)
├── components/
│   ├── layout/
│   │   ├── Navigation.tsx            # Sticky glass nav with mobile menu
│   │   └── Footer.tsx                # 4-column footer with links
│   └── sections/
│       ├── Hero.tsx                  # Hero with product mockup
│       ├── Features.tsx              # 6-card feature grid
│       ├── SmartMonitoring.tsx       # Camera pipeline visualization
│       ├── TimerMode.tsx             # Timer mockup with stats
│       ├── Privacy.tsx               # 4 privacy guarantees
│       ├── Exercises.tsx             # 4 exercise cards
│       ├── Statistics.tsx            # Chart mockup with insights
│       ├── HowItWorks.tsx            # 4-step flow
│       ├── EyeCare.tsx               # 6 educational topics
│       ├── CrossPlatform.tsx         # macOS/Windows cards
│       ├── FAQ.tsx                   # 10-question accordion
│       └── DownloadCTA.tsx           # Final download section
├── lib/
│   ├── site-config.ts                # Centralized config (links, URLs, social)
│   ├── use-scroll-animate.ts         # IntersectionObserver scroll hook
│   └── utils.ts                      # cn() utility
├── tests/
│   ├── site-config.test.ts           # Config validation tests
│   ├── faq-content.test.ts           # FAQ coverage tests
│   └── navigation.test.ts            # Nav structure tests
├── public/
│   ├── manifest.json                 # PWA manifest
│   └── robots.txt                    # Search engine directives
├── eslint.config.mjs                 # ESLint 9 flat config
├── postcss.config.mjs                # Tailwind CSS v4 PostCSS
├── tsconfig.json                     # TypeScript strict config
├── vitest.config.ts                  # Vitest test config
├── package.json                      # Dependencies and scripts
├── .env                              # Environment variables (gitignored)
└── .env.example                      # Environment variable template
```

## Quick Start

### 1. Install Dependencies

```bash
cd apps/web
npm install
```

Or from the project root:

```bash
make install-web
```

### 2. Run Development Server

```bash
# Using Makefile (from project root)
make run-web

# Or manually
cd apps/web
npm run dev
```

Visit `http://localhost:3000`.

### 3. Environment Variables

Copy the example and adjust as needed:

```bash
cp .env.example .env.local
```

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_SITE_URL` | Site URL for metadata | `http://localhost:3000` |
| `NEXT_PUBLIC_DOWNLOAD_WINDOWS_URL` | Windows download link | `#` |
| `NEXT_PUBLIC_DOWNLOAD_MACOS_URL` | macOS download link | `#` |

No API keys are required.

## Development Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Auto-fix lint issues |
| `npm run typecheck` | TypeScript type check |
| `npm run format` | Format with Prettier |
| `npm test` | Run tests |
| `npm run test:watch` | Run tests in watch mode |

### From Project Root

| Command | Description |
|---------|-------------|
| `make run-web` | Start dev server |
| `make test-web` | Run vitest |
| `make lint-web` | Run ESLint |
| `make build-web` | Production build |

## Design System

The website uses a **dark-first** design system defined as CSS custom properties in `globals.css`.

### Colors

```css
--color-bg-primary: #09090b      /* Near-black background */
--color-bg-surface: #111113      /* Dark surface */
--color-bg-elevated: #18181b     /* Elevated cards */
--color-fg-primary: #fafafa      /* Soft white text */
--color-fg-secondary: #a1a1aa    /* Muted gray text */
--color-accent: #06b6d4          /* Refined teal accent */
```

### Typography Scale

| Class | Usage | Size |
|-------|-------|------|
| `display` | Hero headline | clamp(2.5rem, 6vw, 5rem) |
| `heading-1` | Section headlines | clamp(2rem, 4vw, 3.5rem) |
| `heading-2` | Section subheads | clamp(1.5rem, 3vw, 2.5rem) |
| `heading-3` | Card titles | clamp(1.25rem, 2vw, 1.75rem) |
| `body-large` | Lead paragraphs | clamp(1.05rem, 1.5vw, 1.25rem) |
| `body` | Default text | 1rem |
| `body-small` | Secondary text | 0.875rem |
| `caption` | Labels | 0.75rem |
| `label` | Section labels | 0.6875rem uppercase |

### Animations

- Scroll-triggered via `data-animate` attribute + IntersectionObserver
- `prefers-reduced-motion` fully supported — all animations disabled
- Hero entrance: staggered fade-in-up with delays
- Cards: subtle hover elevation and border transitions
- Navigation: glass backdrop on scroll

## Adding a New Section

1. Create `components/sections/YourSection.tsx`
2. Use `'use client'` directive if it has interactivity
3. Import and add to `app/page.tsx`
4. Use design tokens from `globals.css` — never hardcode colors
5. Add `data-animate` to the section wrapper for scroll animation

## Testing

```bash
cd apps/web
npm test
```

Tests cover:
- Site configuration validation
- FAQ content completeness
- Navigation structure

Add tests in `tests/` using Vitest.

## Quality Checks

Before declaring any change complete:

```bash
# From project root
make check

# Or individually
cd apps/web
npm run lint
npm run typecheck
npm test
npm run build
```

All must pass.

## Production Build

```bash
cd apps/web
npm run build
npm run start
```

The build output is static/pre-rendered. Deploy the `.next` directory to any Next.js-compatible host.

## SEO

Implemented in `app/layout.tsx`:
- Title and meta description
- Open Graph metadata
- Twitter/X card metadata
- Canonical URL
- robots.txt
- Semantic HTML with accessible headings

Update `lib/site-config.ts` to change the site URL or social links.

## Styling Rules (Critical)

1. **`globals.css` must be imported in `layout.tsx`.** Without this, Tailwind CSS never loads.

2. **globals.css content:** Only `@import 'tailwindcss';` — nothing else needed for Tailwind v4.

3. **PostCSS config:** Use `@tailwindcss/postcss` plugin (not the old `tailwindcss` plugin).

4. **Never hardcode colors.** Use CSS variables from the design token system.

5. **Font:** Inter loaded via `next/font/google` — no external `<link>` tags.

## License

MIT License. See [LICENSE](../../LICENSE).
