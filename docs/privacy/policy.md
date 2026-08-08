# Privacy Policy

## Overview

Eye Health Assistant is designed with privacy as a core product requirement. This document explains how the application handles user data.

## Data Collection

### What We Collect

**Nothing.** The desktop application does not collect, transmit, or store any data on external servers.

### What the Application Stores Locally

The application stores the following data locally on your device:

- Application settings and preferences
- Monitoring session history
- Break session records
- Exercise completion records
- Aggregated statistics
- Educational content

### What We Never Store

- Webcam video or images
- Camera frames of any kind
- Personal identification information
- Usage analytics (unless explicitly opt-in in the future)
- API keys or credentials

## Camera Usage

### Smart Mode

When Smart Mode is enabled:

1. Camera permission is explicitly requested
2. Camera status is always visible in the UI
3. Frames are processed in memory only
4. **No frames are saved to disk**
5. **No frames are transmitted over a network**
6. Only derived metrics (blink count, estimated rate) are stored
7. Camera can be disabled instantly at any time

### Timer Mode

Timer Mode does not use the camera at all.

## Data Storage

- All data is stored in a local SQLite database
- Database location follows OS conventions:
  - **macOS**: `~/Library/Application Support/EyeHealthAssistant/`
  - **Windows**: `AppData/Local/EyeHealthAssistant/`
  - **Linux**: `~/.local/share/EyeHealthAssistant/`

## Data Control

Users can:

- **Export** all their data (JSON or CSV)
- **Delete** selected history
- **Delete** all history
- **Reset** the entire application

## Network Activity

The desktop application makes **no network requests** during normal operation. The only network dependency is the optional Next.js landing website, which is a separate informational site.

## Third-Party Services

The application does not use:

- Analytics services
- Crash reporting services
- Advertising networks
- Cloud storage services
- Account/authentication services

## Children's Privacy

The application does not knowingly collect information from children under 13.

## Changes to This Policy

Any changes to the privacy model will be:

1. Documented in the CHANGELOG
2. Reflected in this document
3. Clearly communicated to users through the application

## Contact

If you have questions about this privacy policy, please open an issue on the project repository.

## Medical Disclaimer

Eye Health Assistant is a wellness and educational tool. It is not intended to diagnose, treat, cure, or prevent disease. If you experience persistent, severe, or concerning eye symptoms, please consult a qualified eye-care professional.
