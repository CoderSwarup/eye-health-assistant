@echo off
REM build_windows.bat — Build Eye Health Assistant for Windows
REM
REM Usage:
REM   scripts\build\build_windows.bat
REM
REM Prerequisites:
REM   - Python 3.12+
REM   - pip install -e ".[dev]"

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..
set DESKTOP_DIR=%PROJECT_ROOT%\apps\desktop
set DIST_DIR=%DESKTOP_DIR%\dist

echo === Eye Health Assistant — Windows Build ===
echo.

REM Step 1: Clean previous builds
echo [1/6] Cleaning previous builds...
cd /d "%DESKTOP_DIR%"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Step 2: Run tests
echo [2/6] Running tests...
python -m pytest tests\unit\ -q --tb=short
if errorlevel 1 (
    echo ERROR: Tests failed. Aborting build.
    exit /b 1
)

REM Step 3: Run linting
echo [3/6] Running linting...
ruff check src\
if errorlevel 1 (
    echo ERROR: Linting failed. Aborting build.
    exit /b 1
)

REM Step 4: Run type checking
echo [4/6] Running type checking...
mypy src\
if errorlevel 1 (
    echo ERROR: Type checking failed. Aborting build.
    exit /b 1
)

REM Step 5: Build with PyInstaller
echo [5/6] Building with PyInstaller...
pyinstaller EyeHealthAssistant.spec --noconfirm --clean
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    exit /b 1
)

REM Step 6: Verify build
echo [6/6] Verifying build...
set EXECUTABLE=%DIST_DIR%\EyeHealthAssistant\EyeHealthAssistant.exe
if not exist "%EXECUTABLE%" (
    echo ERROR: Executable not found at %EXECUTABLE%
    exit /b 1
)

REM Check content files
set CONTENT_CHECK=%DIST_DIR%\EyeHealthAssistant\eye_health_assistant\content\exercises\exercises.json
if not exist "%CONTENT_CHECK%" (
    echo ERROR: Exercise content not bundled
    exit /b 1
)

set CONTENT_CHECK=%DIST_DIR%\EyeHealthAssistant\eye_health_assistant\content\eye_care\eye_care.json
if not exist "%CONTENT_CHECK%" (
    echo ERROR: Eye care content not bundled
    exit /b 1
)

echo   Application built successfully: %EXECUTABLE%

REM Get version
for /f "tokens=2 delims==" %%a in ('python -c "from eye_health_assistant.core.constants import VERSION; print(VERSION)"') do set VERSION=%%a

echo.
echo === Build Complete ===
echo Application: %EXECUTABLE%
echo Version: %VERSION%
echo.
echo To test: "%EXECUTABLE%"
echo.
echo To create installer, use Inno Setup with the provided .iss script.
