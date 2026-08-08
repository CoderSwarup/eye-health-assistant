# Architecture Overview

## Monorepo Structure

Eye Health Assistant uses a monorepo structure containing two independent applications:

```
eye-health-assistant/
├── apps/
│   ├── desktop/          # Python + PySide6 desktop application
│   └── web/              # Next.js informational landing website
├── packages/
│   ├── config/           # Shared configuration
│   ├── design-tokens/    # Visual design system tokens
│   └── docs/             # Shared documentation
├── docs/                 # Project documentation
└── scripts/              # Development scripts
```

## Desktop Application Architecture

The desktop application uses a layered architecture:

```
UI Layer (PySide6)
    ↓
Application Layer (Services, Commands, Queries)
    ↓
Domain Layer (Models, Enums, Value Objects, Services)
    ↓
Infrastructure Layer (Database, Camera, Notifications, Filesystem)
```

### Layer Responsibilities

#### UI Layer
- Windows, pages, widgets, dialogs
- Theme system (light/dark)
- Navigation
- Event handling (user interactions)
- **Must not** contain database queries or computer vision algorithms

#### Application Layer
- Coordinates use cases
- Manages application flow
- Validates commands
- Orchestrates domain services

#### Domain Layer
- Business models (MonitoringSession, BlinkSample, Exercise, etc.)
- Domain services (blink calculation, scoring)
- Value objects (time ranges, measurements)
- Platform-independent business logic

#### Infrastructure Layer
- SQLite database repositories
- Camera adapters (OpenCV)
- Computer vision adapters (MediaPipe)
- OS notification adapters
- Filesystem operations
- Platform-specific implementations

### Key Design Principles

1. **Dependency Rule**: Dependencies flow inward. UI depends on Application, which depends on Domain. Infrastructure implements interfaces defined in Domain/Application.

2. **Separation of Concerns**: Each layer has a single responsibility.

3. **Testability**: Business logic can be tested without UI or infrastructure.

4. **Cross-Platform**: Platform-specific code is isolated behind adapters.

## Web Application

The Next.js landing website is:
- Purely informational
- Not required for desktop app functionality
- Independent deployment
- Responsive and accessible

## Privacy Architecture

- All data processing is local
- Camera frames are processed in memory, never persisted
- SQLite is the only storage for user data
- No network calls from the desktop application
- User has full control over data export and deletion
