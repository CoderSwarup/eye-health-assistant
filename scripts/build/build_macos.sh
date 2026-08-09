#!/bin/bash
# build_macos.sh — Build Eye Health Assistant for macOS
#
# Usage:
#   ./scripts/build/build_macos.sh [--sign IDENTITY] [--notarize]
#
# Prerequisites:
#   - Python 3.12+
#   - pip install -e ".[dev]"
#   - brew install create-dmg (for DMG creation)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DESKTOP_DIR="$PROJECT_ROOT/apps/desktop"
DIST_DIR="$DESKTOP_DIR/dist"
BUILD_DIR="$DESKTOP_DIR/build"
APP_NAME="Eye Health Assistant"
BUNDLE_NAME="EyeHealthAssistant"

# Parse arguments
SIGN_IDENTITY=""
NOTARIZE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --sign)
            SIGN_IDENTITY="$2"
            shift 2
            ;;
        --notarize)
            NOTARIZE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=== Eye Health Assistant — macOS Build ==="
echo ""

# Step 1: Clean previous builds
echo "[1/7] Cleaning previous builds..."
cd "$DESKTOP_DIR"
rm -rf build dist *.spec.bak

# Step 2: Run tests
echo "[2/7] Running tests..."
python -m pytest tests/unit/ -q --tb=short || {
    echo "ERROR: Tests failed. Aborting build."
    exit 1
}

# Step 3: Run linting
echo "[3/7] Running linting..."
ruff check src/ || {
    echo "ERROR: Linting failed. Aborting build."
    exit 1
}

# Step 4: Run type checking
echo "[4/7] Running type checking..."
mypy src/ || {
    echo "ERROR: Type checking failed. Aborting build."
    exit 1
}

# Step 5: Build with PyInstaller
echo "[5/7] Building with PyInstaller..."
pyinstaller EyeHealthAssistant.spec --noconfirm --clean

# Step 6: Verify build
echo "[6/7] Verifying build..."
APP_PATH="$DIST_DIR/$APP_NAME.app"
if [ ! -d "$APP_PATH" ]; then
    echo "ERROR: Application bundle not found at $APP_PATH"
    exit 1
fi

# Check bundle structure
EXECUTABLE="$APP_PATH/Contents/MacOS/$BUNDLE_NAME"
if [ ! -f "$EXECUTABLE" ]; then
    echo "ERROR: Executable not found at $EXECUTABLE"
    exit 1
fi

# Check content files are bundled
CONTENT_CHECK="$APP_PATH/Contents/Resources/eye_health_assistant/content/exercises/exercises.json"
if [ ! -f "$CONTENT_CHECK" ]; then
    echo "ERROR: Exercise content not bundled"
    exit 1
fi

CONTENT_CHECK="$APP_PATH/Contents/Resources/eye_health_assistant/content/eye_care/eye_care.json"
if [ ! -f "$CONTENT_CHECK" ]; then
    echo "ERROR: Eye care content not bundled"
    exit 1
fi

echo "  Application bundle verified: $APP_PATH"

# Step 7: Code signing (optional)
if [ -n "$SIGN_IDENTITY" ]; then
    echo "[7/7] Signing application..."
    codesign --force --deep --sign "$SIGN_IDENTITY" \
        --options runtime \
        --timestamp \
        "$APP_PATH"
    echo "  Signed with identity: $SIGN_IDENTITY"
else
    echo "[7/7] Skipping code signing (no identity provided)"
    echo "  To sign: ./scripts/build/build_macos.sh --sign \"Developer ID Application: Your Name (TEAMID)\""
fi

# Create DMG
echo ""
echo "Creating DMG..."
DMG_NAME="Eye-Health-Assistant-macOS-v$(python -c "from eye_health_assistant.core.constants import VERSION; print(VERSION)").dmg"
DMG_PATH="$DIST_DIR/$DMG_NAME"

if command -v create-dmg &> /dev/null; then
    create-dmg \
        --volname "Eye Health Assistant" \
        --volicon "$APP_PATH/Contents/Resources/AppIcon.icns" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "$APP_NAME.app" 150 190 \
        --hide-extension "$APP_NAME.app" \
        --app-drop-link 450 190 \
        "$DMG_PATH" \
        "$APP_PATH" 2>/dev/null || {
        echo "  create-dmg failed, using hdiutil fallback..."
        hdiutil create -volname "Eye Health Assistant" \
            -srcfolder "$APP_PATH" \
            -ov -format UDZO \
            "$DMG_PATH"
    }
    echo "  DMG created: $DMG_PATH"
else
    echo "  create-dmg not installed. Installing via Homebrew..."
    brew install create-dmg 2>/dev/null || true
    echo "  Please re-run this script after installing create-dmg"
    echo "  Or create DMG manually: hdiutil create -volname \"Eye Health Assistant\" -srcfolder \"$APP_PATH\" -ov -format UDZO \"$DMG_PATH\""
fi

# Notarization (optional)
if [ "$NOTARIZE" = true ]; then
    echo ""
    echo "Notarizing application..."
    if [ -z "${APPLE_ID:-}" ] || [ -z "${APPLE_TEAM_ID:-}" ] || [ -z "${APPLE_APP_PASSWORD:-}" ]; then
        echo "  ERROR: Notarization requires APPLE_ID, APPLE_TEAM_ID, and APPLE_APP_PASSWORD"
        echo "  Set these environment variables and re-run with --notarize"
    else
        xcrun notarytool submit "$DMG_PATH" \
            --apple-id "$APPLE_ID" \
            --team-id "$APPLE_TEAM_ID" \
            --password "$APPLE_APP_PASSWORD" \
            --wait
        echo "  Notarization complete"
    fi
fi

echo ""
echo "=== Build Complete ==="
echo "Application: $APP_PATH"
if [ -f "$DMG_PATH" ]; then
    echo "DMG: $DMG_PATH"
fi
echo ""
echo "To test: open \"$APP_PATH\""
