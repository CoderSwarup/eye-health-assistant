#!/bin/bash
# bump_version.sh — Bump application version across all files
#
# Usage:
#   ./scripts/build/bump_version.sh <new_version>
#
# Example:
#   ./scripts/build/bump_version.sh 1.0.0

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <new_version>"
    echo "Example: $0 1.0.0"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "ERROR: Version must be in MAJOR.MINOR.PATCH format (e.g., 1.0.0)"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Bumping version to $NEW_VERSION ==="
echo ""

# Files to update
FILES=(
    "apps/desktop/pyproject.toml"
    "apps/desktop/src/eye_health_assistant/core/constants.py"
    "apps/desktop/src/eye_health_assistant/__init__.py"
    "apps/web/package.json"
)

for FILE in "${FILES[@]}"; do
    FULL_PATH="$PROJECT_ROOT/$FILE"
    if [ -f "$FULL_PATH" ]; then
        echo "Updating: $FILE"
        # Use sed to replace version strings
        if [[ "$FILE" == *.py ]]; then
            sed -i.bak "s/VERSION: str = \"[^\"]*\"/VERSION: str = \"$NEW_VERSION\"/" "$FULL_PATH"
        elif [[ "$FILE" == *.toml ]]; then
            sed -i.bak "s/^version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" "$FULL_PATH"
        elif [[ "$FILE" == *.json ]]; then
            sed -i.bak "s/\"version\": \"[^\"]*\"/\"version\": \"$NEW_VERSION\"/" "$FULL_PATH"
        fi
        rm -f "$FULL_PATH.bak"
    else
        echo "  WARNING: File not found: $FILE"
    fi
done

echo ""
echo "=== Version bumped to $NEXT_VERSION ==="
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit: git add -A && git commit -m \"chore: bump version to $NEW_VERSION\""
echo "  3. Tag: git tag v$NEW_VERSION"
echo "  4. Push: git push origin main --tags"
