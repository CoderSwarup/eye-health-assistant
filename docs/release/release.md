# Release Process

## Versioning

This project uses Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes or major feature additions
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

---

## Local Testing (Before Release)

Test the built app locally before pushing to release.

### macOS

```bash
# 1. Build
make build-desktop

# 2. Run the .app bundle
open apps/desktop/dist/EyeHealthAssistant.app

# 3. Or run the executable directly
./apps/desktop/dist/EyeHealthAssistant.app/Contents/MacOS/EyeHealthAssistant
```

### Windows

```bash
# 1. Build (run on Windows machine or CI)
cd apps/desktop
.venv\Scripts\pyinstaller.exe --windowed --name EyeHealthAssistant src\eye_health_assistant\main.py

# 2. Run the .exe
dist\EyeHealthAssistant.exe
```

### What to Test Locally

Before pushing to release, verify:

| # | Test | Pass? |
|---|------|-------|
| 1 | App launches without crash | |
| 2 | Sidebar navigation works (all pages) | |
| 3 | Dashboard displays correctly | |
| 4 | Theme switching (light/dark) works | |
| 5 | No visual artifacts (borders, lines) | |
| 6 | Ctrl+C / Cmd+Q exits cleanly | |
| 7 | Window resizes properly | |

---

## Prerequisites

### Desktop Build

```bash
# Install dev dependencies (includes PyInstaller)
cd apps/desktop
python3 -m venv .venv
.venv/bin/pip3 install -e ".[dev]"

# Verify PyInstaller is available
.venv/bin/pyinstaller --version
```

### Web Build

```bash
cd apps/web
npm install
```

---

## Release Steps

### 1. Local Testing Complete

```bash
# Run local tests above, confirm all pass
```

### 2. Update Version

```bash
# Update version in:
# - apps/desktop/pyproject.toml  (line: version = "X.Y.Z")
# - apps/desktop/src/eye_health_assistant/__init__.py  (__version__)
# - apps/web/package.json  (line: "version": "X.Y.Z")
```

### 3. Update Changelog

Add entries to `docs/CHANGELOG.md` under the new version heading.

### 4. Create Release Branch

```bash
git checkout -b release/v1.0.0
```

### 5. Run Full Quality Checks

```bash
make check
```

### 6. Build Artifacts

```bash
# Desktop (macOS — must run on target platform)
make build-desktop
# Produces: apps/desktop/dist/EyeHealthAssistant.app

# Web (server-rendered)
make build-web
# Produces: apps/web/.next/
```

### 7. Package Desktop for Distribution

#### macOS (.dmg)

```bash
# PyInstaller produces a .app bundle
# Create a .dmg for distribution:
cd apps/desktop/dist
hdiutil create -volname "Eye Health Assistant" \
  -srcfolder EyeHealthAssistant.app \
  -ov -format UDZO \
  EyeHealthAssistant-macOS-arm64-v$(grep 'version' ../pyproject.toml | head -1 | sed 's/.*"\(.*\)".*/\1/').dmg
```

#### Windows (.exe)

```bash
# Build on Windows CI or local Windows machine
cd apps/desktop
.venv\Scripts\pyinstaller.exe --windowed --name EyeHealthAssistant src\eye_health_assistant\main.py
# Produces: apps/desktop/dist/EyeHealthAssistant.exe
```

### 8. Tag Release

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 9. Create GitHub Release

- Upload build artifacts (`.app`, `.dmg`, `.exe`)
- Write release notes
- Mark as latest

---

## Build Artifact Naming

```
EyeHealthAssistant-Windows-x64-v1.0.0.exe
EyeHealthAssistant-macOS-arm64-v1.0.0.dmg
EyeHealthAssistant-macOS-x64-v1.0.0.dmg
```

## Build Commands Reference

| Command | Description | Output |
|---------|-------------|--------|
| `make build-desktop` | Build desktop app with PyInstaller | `apps/desktop/dist/EyeHealthAssistant.app` |
| `make build-web` | Build web app with Next.js | `apps/web/.next/` |
| `make check` | Run all quality checks | — |
| `make clean` | Clean build artifacts | — |

---

## Platform-Specific Notes

### macOS

- Application should be code-signed for distribution
- Notarization recommended (Apple Developer account required)
- `.dmg` is the standard distribution format
- Architecture: ARM64 (Apple Silicon) or x64 (Intel)

### Windows

- `.exe` installer for end users
- Code signing recommended for trusted installation
- Architecture: x64

### Linux

- `.AppImage` or `.deb` for distribution
- PyInstaller works on Linux as well

---

## Troubleshooting

### PyInstaller not found

```bash
# Ensure dev dependencies are installed
cd apps/desktop
.venv/bin/pip3 install -e ".[dev]"
```

### PyInstaller missing modules

```bash
# Add hidden imports if PyInstaller misses them
cd apps/desktop
.venv/bin/pyinstaller --windowed --name EyeHealthAssistant \
  --hidden-import PySide6.QtWidgets \
  --hidden-import PySide6.QtCore \
  --hidden-import PySide6.QtGui \
  src/eye_health_assistant/main.py
```

### Build fails with import errors

```bash
# Clean and rebuild
make clean
cd apps/desktop && .venv/bin/pip3 install -e ".[dev]"
make build-desktop
```

### App crashes on launch (macOS)

```bash
# Run from terminal to see error output
./apps/desktop/dist/EyeHealthAssistant.app/Contents/MacOS/EyeHealthAssistant
```

### App shows blank window

```bash
# Check if theme resources are bundled
ls apps/desktop/dist/EyeHealthAssistant.app/Contents/Resources/
```

---

## Smoke Tests (Post-Build)

After building, verify on a clean system:

1. Launch application
2. Complete onboarding
3. Test Timer Mode
4. Test Smart Mode (if camera available)
5. Verify theme switching
6. Verify data export
7. Verify data deletion

---

## Rollback

If a release has critical issues:
1. Mark the release as pre-release
2. Create a patch release with fixes
3. Communicate to users through the landing website
