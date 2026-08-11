# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- macOS DMG packaging script
- Windows build script
- Version bump script
- GitHub Actions release workflow
- Release documentation

## [0.1.0] - 2026-08-09

### Added

#### Foundation
- Monorepo structure with desktop and web applications
- Python desktop application skeleton with PySide6
- Next.js 16 landing website with React 19 and Tailwind CSS v4
- CI/CD pipelines (GitHub Actions) for desktop, web, and security
- Linting setup (Ruff, mypy, ESLint 9 flat config)
- Testing setup (pytest, Vitest)
- PyInstaller packaging configuration

#### Desktop UI
- Navigation system with sidebar and keyboard shortcuts (1-7, Escape)
- Theme system (light, dark, system) with runtime switching
- Dashboard with metrics cards, monitoring status, quick actions
- Settings page with 9 sections (Appearance, Timer, Notifications, Quiet Hours, Sound, Startup, Camera, Thresholds, Analytics, Data)
- Reusable component library (MetricCard, Toggle, Slider, ProgressBar, etc.)
- Design system with typography tokens and spacing scale

#### Timer Mode
- Timer engine with state machine and clock abstraction
- Timer presets (focus/break/long break) with configurable durations
- Auto-transition between focus and break phases
- Notification system with desktop notifications
- History tracking with database-backed session log

#### Smart Mode (Camera)
- Camera permission handling with explicit request
- OpenCV camera adapter with device enumeration
- MediaPipe face/eye landmark detector
- OpenCV fallback face detector
- Time-based blink estimation (calibrated to research data)
- Blink rate smoothing with rolling window
- Monitoring service with Qt signals
- Live Monitoring screen with real-time metrics

#### Exercises
- Exercise catalog with 6 guided exercises
- Exercise card UI with category filtering
- Exercise detail screen with step-by-step instructions
- Exercise animations with engine and controller
- Exercise player with countdown, progress, pause/resume
- Content loaded from JSON files with validation

#### Eye Care
- Eye Care / Learning Center with 9 educational articles
- Article detail screen with sections, related exercises, disclaimer
- Content loaded from JSON files with validation

#### Analytics
- Daily, weekly, monthly statistics
- Period selector (Today, 7 Days, 30 Days)
- Bar charts and line charts (QPainter)
- Period comparison with percentage change
- Data export (JSON) with file dialog
- Data deletion with confirmation

#### Production Hardening
- Graceful database error handling with degraded mode
- Notification policy layer with rate limiting, quiet hours, per-type cooldowns
- Database migrations system (version-based)
- Keyboard navigation and accessibility (focus styling, screen reader labels)
- Onboarding wizard (5 steps: Welcome, Privacy, Mode, Theme, Finish)
- Camera permission denied dialog with system settings link
- Reusable UI state components (LoadingState, EmptyState, ErrorState)
- System tray with context menu and close-to-tray
- Singleton instance lock (PID file)
- Logging with RotatingFileHandler and global exception hooks

#### Documentation
- PRD (Product Requirements Document)
- AGENTS.md (AI coding agent instructions)
- PREREQUISITES.md (system requirements)
- DEVELOPMENT.md (development guide)
- SECURITY.md (security policy)
- CONTRIBUTING.md (contribution guidelines)
- Release process documentation
- CI/CD pipeline documentation

#### Website
- Hero section with product value proposition
- Features section (6-card grid)
- Smart Monitoring section
- Timer Mode section
- Privacy section (4 guarantees)
- Exercises section
- Statistics section
- How It Works section (4-step flow)
- Eye Care section
- Cross-Platform section
- Roadmap section (Q3 2026 - Q1 2027)
- FAQ section (10 questions)
- Download CTA section
- Navigation with mobile hamburger menu
- Footer with links and documentation
- SEO metadata (Open Graph, Twitter, robots, canonical)
- Responsive design with Tailwind CSS v4

### Changed
- N/A (initial release)

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- CI/CD workflow issues with logging and versions
- Package-lock.json synchronization
- Build path corrections
- File path handling across platforms

### Security
- Privacy-first architecture (no cloud, no telemetry)
- Camera processing local-only (no frames stored or uploaded)
- No medical/diagnostic claims
- Explicit camera permission handling
- Local SQLite database only
