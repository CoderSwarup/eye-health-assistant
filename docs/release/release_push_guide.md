# Release Push Guide

This document explains how to create a production release of Eye Health
Assistant.

## Prerequisites

Before releasing, ensure you have:

- [ ] Git installed and configured
- [ ] Push access to the repository
- [ ] Python 3.12+ installed locally
- [ ] All dependencies installed (`pip install -e ".[dev]"`)
- [ ] Clean working directory (no uncommitted changes)

## Version Selection

Eye Health Assistant uses Semantic Versioning:

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes or major redesign
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, minor improvements

Current version: `0.1.0` (as defined in
`apps/desktop/src/eye_health_assistant/core/constants.py`)

## Before Releasing

### 1. Ensure all tests pass

```bash
cd apps/desktop
python -m pytest tests/ -v
```

### 2. Ensure linting and type checking passes

```bash
cd apps/desktop
ruff check src/
mypy src/
```

### 3. Build and test locally BEFORE pushing

**This is the most important step.** Always verify the build works on your
machine before creating a release tag.

#### macOS Local Build & Test

```bash
# Step 1: Clean previous builds
cd apps/desktop
rm -rf build dist

# Step 2: Build with PyInstaller
pyinstaller EyeHealthAssistant.spec --noconfirm --clean

# Step 3: Verify the app bundle was created
ls -la "dist/Eye Health Assistant.app"

# Step 4: Launch the app
open "dist/Eye Health Assistant.app"

# Step 5: Test these features manually:
#   - Dashboard loads with metric cards
#   - Navigate to Settings (click Settings in sidebar)
#   - Navigate to Exercises (click Exercises in sidebar)
#   - Navigate to Eye Care (click Eye Care in sidebar)
#   - Navigate to Statistics (click Statistics in sidebar)
#   - Navigate to History (click History in sidebar)
#   - Toggle theme (click Toggle Theme in sidebar)
#   - Open Settings and verify all sections load
#   - Close the app (click X or Cmd+Q)

# Step 6: Verify content files are bundled
ls "dist/Eye Health Assistant.app/Contents/Resources/eye_health_assistant/content/exercises/"
ls "dist/Eye Health Assistant.app/Contents/Resources/eye_health_assistant/content/eye_care/"

# Step 7: Check app info
cat "dist/Eye Health Assistant.app/Contents/Info.plist"
```

**What to look for:**

- App launches without crash
- Dashboard shows metric cards (Screen Time, Blink Rate, Breaks, Smart Mode)
- All 7 pages are accessible via sidebar
- Theme toggles between light and dark
- Settings page loads all sections
- Exercises page shows exercise cards
- Eye Care page shows article cards
- No error dialogs appear

#### Windows Local Build & Test

```cmd
:: Step 1: Clean previous builds
cd apps-desktop
rmdir /s /q build
rmdir /s /q dist

:: Step 2: Build with PyInstaller
pyinstaller EyeHealthAssistant.spec --noconfirm --clean

:: Step 3: Verify the executable was created
dir "dist\EyeHealthAssistant\EyeHealthAssistant.exe"

:: Step 4: Launch the app
"dist\EyeHealthAssistant\EyeHealthAssistant.exe"

:: Step 5: Test these features manually:
::   - Dashboard loads with metric cards
::   - Navigate to all pages via sidebar
::   - Toggle theme
::   - Open Settings and verify all sections
::   - Close the app

:: Step 6: Verify content files are bundled
dir "dist\EyeHealthAssistant\eye_health_assistant\content\exercises\"
dir "dist\EyeHealthAssistant\eye_health_assistant\content\eye_care\"
```

**What to look for:**

- App launches without crash or antivirus warning
- Dashboard shows metric cards
- All pages accessible
- Theme toggles work
- No missing DLL errors

#### Quick Build & Test Script (macOS)

```bash
# One-command build and test
cd apps/desktop && rm -rf build dist && pyinstaller EyeHealthAssistant.spec --noconfirm --clean && open "dist/Eye Health Assistant.app"
```

### 4. Update the version

If this is a new version, update all version references:

```bash
./scripts/build/bump_version.sh X.Y.Z
```

This updates:

- `apps/desktop/pyproject.toml`
- `apps/desktop/src/eye_health_assistant/core/constants.py`
- `apps/desktop/src/eye_health_assistant/__init__.py`
- `apps/web/package.json`

### 5. Update CHANGELOG.md

Add a new section to `docs/CHANGELOG.md`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- New features

### Changed

- Changes to existing features

### Fixed

- Bug fixes

### Security

- Security improvements
```

### 6. Commit your changes

```bash
git add -A
git commit -m "chore: prepare release vX.Y.Z"
git push origin main
```

## Creating the Release

### Step 1: Create a Git tag

```bash
git tag vX.Y.Z
```

For example:

```bash
git tag v1.0.0
```

### Step 2: Push the tag

```bash
git push origin vX.Y.Z
```

Or push all tags:

```bash
git push origin --tags
```

### Step 3: What happens next

Once the tag is pushed, GitHub Actions automatically:

1. **Validates** the release
   - Verifies version consistency
   - Runs all tests
   - Runs linting
   - Runs type checking

2. **Builds macOS artifact**
   - Creates application bundle (`.app`)
   - Creates disk image (`.dmg`)

3. **Builds Windows artifact**
   - Creates application folder
   - Creates ZIP archive

4. **Creates GitHub Release**
   - Generates release notes from commits
   - Attaches macOS `.dmg` and Windows `.zip`
   - Publishes the release

### Step 4: Monitor the workflow

Go to: https://github.com/CoderSwarup/eye-health-assistant/actions

You should see the "Release" workflow running. Click on it to monitor progress.

### Step 5: Verify the release

After the workflow completes:

1. Go to: https://github.com/CoderSwarup/eye-health-assistant/releases
2. Verify the release exists
3. Verify the version number is correct
4. Verify the artifacts are attached:
   - `Eye-Health-Assistant-macOS-vX.Y.Z.dmg`
   - `Eye-Health-Assistant-Windows-vX.Y.Z.zip`
5. Download and test each artifact

## Monitoring

### Workflow Status

Check the workflow status at:

```
https://github.com/CoderSwarup/eye-health-assistant/actions
```

### Release Page

Check the release at:

```
https://github.com/CoderSwarup/eye-health-assistant/releases
```

## What to Do If It Fails

### Tests failed

1. Check the workflow logs
2. Fix the failing tests locally
3. Push the fix
4. Delete the tag: `git tag -d vX.Y.Z`
5. Re-tag and re-push

### Build failed

1. Check the workflow logs for the specific step
2. Common issues:
   - Missing dependency
   - Import error
   - Resource not found
3. Fix the issue locally
4. Delete the tag and re-release

### Version mismatch

If the release workflow fails with a version mismatch:

1. Check your local version:
   ```bash
   python -c "from eye_health_assistant.core.constants import VERSION; print(VERSION)"
   ```

2. Check the tag version:
   ```bash
   git tag -l
   ```

3. If they don't match, update the version:
   ```bash
   ./scripts/build/bump_version.sh X.Y.Z
   git add -A
   git commit -m "chore: fix version to X.Y.Z"
   git push origin main
   ```

4. Delete the old tag and re-create it:
   ```bash
   git tag -d vX.Y.Z
   git push origin :refs/tags/vX.Y.Z
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

### Artifacts not attached

1. Check the "Create GitHub Release" step in the workflow
2. Verify the artifacts were uploaded in previous steps
3. Check GitHub Release permissions

### Complete Rollback — Delete Tag and Re-Release

If the release failed for any reason and you need to fix and re-release the same version:

```bash
# Step 1: Delete the tag locally
git tag -d vX.Y.Z

# Step 2: Delete the tag from remote
git push origin :refs/tags/vX.Y.Z

# Step 3: Fix your code
# (make changes, fix bugs, etc.)

# Step 4: Commit the fix
git add -A
git commit -m "fix: description of what you fixed"

# Step 5: Push the fix
git push origin development

# Step 6: Re-create the tag
git tag vX.Y.Z

# Step 7: Push the tag again
git push origin vX.Y.Z
```

**Important:** You cannot push the same tag twice. You must delete it first, then re-create it.

| Action | Result |
|--------|--------|
| Push same tag twice | ❌ Fails - tag already exists |
| Delete tag + re-push | ✅ Works |
| Push new version tag | ✅ Works |

### Alternative: Use a New Version Number

Instead of deleting and re-creating the tag, you can use a new version:

```bash
# If v1.0.0 failed, use v1.0.1 instead
git tag v1.0.1
git push origin v1.0.1
```

This is often simpler and creates a clear version history.

## Local Release Verification

### Full Local Build & Test Checklist

Before pushing a release tag, run through this complete checklist:

#### Prerequisites

```bash
# Ensure dependencies are installed
cd apps/desktop
pip install -e ".[dev]"

# Ensure tests pass
python -m pytest tests/unit/ -v

# Ensure linting passes
ruff check src/
mypy src/
```

#### macOS Build & Test

```bash
# Build
cd apps/desktop
rm -rf build dist
pyinstaller EyeHealthAssistant.spec --noconfirm --clean

# Verify bundle structure
ls -la "dist/Eye Health Assistant.app/Contents/MacOS/"
ls -la "dist/Eye Health Assistant.app/Contents/Resources/eye_health_assistant/content/"

# Launch and test
open "dist/Eye Health Assistant.app"
# Test all pages, settings, theme toggle, exercises, eye care
```

#### Windows Build & Test

```cmd
:: Build
cd apps\desktop
rmdir /s /q build
rmdir /s /q dist
pyinstaller EyeHealthAssistant.spec --noconfirm --clean

:: Verify
dir "dist\EyeHealthAssistant\EyeHealthAssistant.exe"
dir "dist\EyeHealthAssistant\eye_health_assistant\content\"

:: Launch and test
"dist\EyeHealthAssistant\EyeHealthAssistant.exe"
:: Test all pages, settings, theme toggle, exercises, eye care
```

#### Test Checklist

- [ ] App launches without crash
- [ ] Dashboard loads with all metric cards
- [ ] All 7 sidebar pages are accessible
- [ ] Theme toggle works (light/dark)
- [ ] Settings page loads all sections
- [ ] Exercises page shows exercise cards
- [ ] Eye Care page shows article cards
- [ ] Statistics page loads
- [ ] History page loads
- [ ] No error dialogs appear
- [ ] App closes cleanly

## Rollback

If a release has critical issues:

1. Go to GitHub Releases
2. Edit the release
3. Mark it as a pre-release or delete it
4. Fix the issue
5. Create a new patch release

Do not delete tags that have been published to GitHub Releases.
