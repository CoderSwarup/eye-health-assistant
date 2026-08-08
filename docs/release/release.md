# Release Process

## Versioning

This project uses Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes or major feature additions
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Release Steps

### 1. Update Version

```bash
# Update version in:
# - apps/desktop/pyproject.toml
# - apps/desktop/src/eye_health_assistant/__init__.py
# - apps/web/package.json
# - package.json at root (if applicable)
```

### 2. Update Changelog

Add entries to `CHANGELOG.md` under the new version heading.

### 3. Create Release Branch

```bash
git checkout -b release/v1.0.0
```

### 4. Run Full Quality Checks

```bash
make check
```

### 5. Build Artifacts

```bash
# Desktop (on macOS)
make build-desktop
# Produces: EyeHealthAssistant-macOS-arm64-v1.0.0.dmg

# Desktop (on Windows CI)
# Produces: EyeHealthAssistant-Windows-x64-v1.0.0.exe

# Web
make build-web
```

### 6. Tag Release

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 7. Create GitHub Release

- Upload build artifacts
- Write release notes
- Mark as latest

## Build Artifact Naming

```
EyeHealthAssistant-Windows-x64-v1.0.0.exe
EyeHealthAssistant-macOS-arm64-v1.0.0.dmg
EyeHealthAssistant-macOS-x64-v1.0.0.dmg
```

## Platform-Specific Notes

### macOS

- Application should be code-signed
- Notarization recommended for distribution
- `.dmg` is the standard distribution format

### Windows

- `.exe` installer for end users
- Code signing recommended for trusted installation

## Smoke Tests

After building:

1. Install on a clean system
2. Launch application
3. Complete onboarding
4. Test Timer Mode
5. Test Smart Mode (if camera available)
6. Verify theme switching
7. Verify data export
8. Verify data deletion

## Rollback

If a release has critical issues:
1. Mark the release as pre-release
2. Create a patch release with fixes
3. Communicate to users through the landing website
