# Prerequisites

## Desktop Application (Python + PySide6)

### Required
- Python 3.12+ (tested with 3.14)
- pip (Python package manager)

### Optional (for Smart Mode / Camera Features)
- Webcam (USB or built-in)
- OpenCV: `pip install opencv-python`
- MediaPipe: `pip install mediapipe` (not available on Python 3.14)

### System Requirements
- **macOS**: 10.15+ (Catalina or later)
- **Windows**: 10+ with Visual C++ Redistributable
- **Linux**: GTK 3+ with desktop notifications

## Web Landing Site (Next.js)

### Required
- Node.js 20+ (LTS recommended)
- npm 10+

### Development
- VS Code with TypeScript extension (recommended)
- Git 2.30+

## Development Tools (Optional)

### Code Quality
- Ruff: `pip install ruff` (Python linter/formatter)
- mypy: `pip install mypy` (Python type checker)
- ESLint: installed via npm (TypeScript linter)

### Building
- PyInstaller: `pip install pyinstaller` (desktop distribution)
- Node.js 20+ with npm (web builds)
