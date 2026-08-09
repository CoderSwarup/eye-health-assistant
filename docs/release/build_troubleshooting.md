# Build Troubleshooting

This document covers common build problems and their solutions.

## Common Issues

### 1. Missing Module Error

**Error:**
```
ModuleNotFoundError: No module named 'eye_health_assistant'
```

**Solution:**
```bash
cd apps/desktop
pip install -e ".[dev]"
```

### 2. PyInstaller Missing Import

**Error:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solution:**
Add the missing module to `hiddenimports` in `EyeHealthAssistant.spec`:

```python
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    # Add missing module here
]
```

### 3. Content Files Not Bundled

**Error:**
Application launches but exercises/eye care content is missing.

**Solution:**
1. Check `EyeHealthAssistant.spec` has the correct `datas` configuration
2. Ensure content files exist at the expected paths
3. Rebuild: `pyinstaller EyeHealthAssistant.spec --noconfirm --clean`

### 4. macOS App Won't Launch

**Error:**
Application crashes immediately on launch.

**Solutions:**
1. Check Console.app for crash logs
2. Verify the app has correct permissions:
   ```bash
   xattr -cr "dist/Eye Health Assistant.app"
   ```
3. Check for missing frameworks:
   ```bash
   otool -L "dist/Eye Health Assistant.app/Contents/MacOS/EyeHealthAssistant"
   ```

### 5. Windows Antivirus Blocking

**Error:**
Windows Defender or antivirus blocks the application.

**Solution:**
1. This is common with unsigned executables
2. Click "More info" → "Run anyway"
3. For production, use code signing (see below)

### 6. Build Fails with Permission Error

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Clean build artifacts
rm -rf build dist

# Or on Windows
rmdir /s /q build
rmdir /s /q dist
```

### 7. Version Mismatch Error

**Error:**
Release workflow fails with version mismatch.

**Solution:**
```bash
# Check current version
python -c "from eye_health_assistant.core.constants import VERSION; print(VERSION)"

# Update version
./scripts/build/bump_version.sh X.Y.Z

# Commit and push
git add -A
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

### 8. Missing PySide6 Qt Libraries

**Error:**
```
qt.qpa.plugin: Could not load the Qt platform plugin "cocoa"
```

**Solution:**
```bash
# Reinstall PySide6
pip install --force-reinstall PySide6

# Set environment variable (if needed)
export QT_QPA_PLATFORM=offscreen
```

### 9. macOS Code Signing Fails

**Error:**
```
code signing failed
```

**Solutions:**
1. Verify your certificate is installed:
   ```bash
   security find-identity -v -p codesigning
   ```
2. Use the correct identity:
   ```bash
   codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" "app.app"
   ```
3. For CI, ensure secrets are configured correctly

### 10. DMG Creation Fails

**Error:**
```
hdiutil: create failed - Resource busy
```

**Solution:**
```bash
# Unmount any existing DMAs
hdiutil detach /Volumes/Eye\ Health\ Assistant 2>/dev/null || true

# Retry creation
```

## Platform-Specific Issues

### macOS

#### Apple Silicon vs Intel

The build produces an Intel-compatible binary by default. For Apple Silicon:

```bash
# Build with architecture target
pyinstaller EyeHealthAssistant.spec --target-arch arm64
```

For universal binary:

```bash
# Build both architectures and combine
pyinstaller EyeHealthAssistant.spec --target-arch x86_64
pyinstaller EyeHealthAssistant.spec --target-arch arm64
# Then use lipo to combine
```

#### Notarization

For macOS notarization, you need:

1. Apple Developer account
2. App-specific password
3. Team ID

Set environment variables:

```bash
export APPLE_ID="your@email.com"
export APPLE_TEAM_ID="YOUR_TEAM_ID"
export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```

Then run:

```bash
xcrun notarytool submit "Eye Health Assistant.dmg" \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_PASSWORD" \
  --wait
```

### Windows

#### Antivirus False Positives

Unsigned executables often trigger antivirus. Solutions:

1. **Code signing** (recommended for production)
2. **Submit to antivirus vendors** for whitelisting
3. **User education** about unsigned software

#### Missing Visual C++ Redistributable

If the app crashes on Windows without Python:

1. Install Visual C++ Redistributable
2. Or bundle it with the installer using Inno Setup

## CI/CD Issues

### GitHub Actions Failing

1. Check workflow logs at:
   ```
   https://github.com/CoderSwarup/eye-health-assistant/actions
   ```

2. Common CI issues:
   - Dependency installation fails
   - Tests fail
   - Build fails
   - Artifact upload fails

### Release Workflow Not Triggering

1. Verify the tag format: `vX.Y.Z`
2. Check the tag was pushed:
   ```bash
   git tag -l
   git push origin --tags
   ```

### Artifacts Not Uploading

1. Check the `actions/upload-artifact` step
2. Verify the file path is correct
3. Check GitHub permissions

## Getting Help

If you encounter an issue not covered here:

1. Check the GitHub Issues: https://github.com/CoderSwarup/eye-health-assistant/issues
2. Search for similar issues
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Operating system
   - Python version
   - PyInstaller version
