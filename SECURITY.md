# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to the maintainers. All security vulnerabilities will be promptly addressed.

## Privacy by Design

This application is built with privacy as a core requirement:

- **No cloud storage** for core application data
- **No webcam uploads** - all camera processing happens locally
- **No raw video recording** by default
- **No account required** for normal use
- **No API keys or secrets** stored in the application
- **Local SQLite database** for all user data
- **User-controlled data** with export and delete capabilities

## Security Measures

- Secure local file permissions
- Safe database handling with parameterized queries
- Input validation on all user-facing interfaces
- Dependency vulnerability scanning in CI
- No hardcoded secrets or credentials
- Platform-appropriate application data directories

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Data Handling

- Camera frames are processed in memory and never persisted by default
- Database files use standard SQLite with appropriate file permissions
- Export functionality writes to user-selected locations only
- All user data can be deleted at any time through the application settings
