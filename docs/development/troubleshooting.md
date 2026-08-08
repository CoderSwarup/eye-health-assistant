# Troubleshooting Guide

## Application Won't Start

### Python Not Found

**Symptom**: `python: command not found`

**Solution**:
- Ensure Python 3.12+ is installed
- Use `python3` instead of `python` if needed
- Activate the virtual environment: `source .venv/bin/activate`

### Missing Dependencies

**Symptom**: `ModuleNotFoundError: No module named 'PySide6'`

**Solution**:
```bash
cd apps/desktop
pip install -e ".[dev]"
```

### Permission Error

**Symptom**: `PermissionError` when creating application directories

**Solution**:
- Check that your user has write access to the application data directory
- On macOS: `~/Library/Application Support/EyeHealthAssistant/`
- On Windows: `AppData/Local/EyeHealthAssistant/`

## Camera Issues

### Camera Permission Denied

**macOS**:
1. Open System Preferences
2. Go to Security & Privacy → Privacy → Camera
3. Find Eye Health Assistant and enable it
4. Restart the application

**Windows**:
1. Open Settings
2. Go to Privacy → Camera
3. Ensure camera access is enabled
4. Ensure Eye Health Assistant has permission

### Camera Not Detected

- Ensure a camera is connected
- Check if another application is using the camera
- Try selecting a different camera in Settings → Camera

### Black Camera Preview

- Check camera lens for obstructions
- Ensure adequate lighting
- Try a different camera if available
- Check camera drivers are up to date

## Notification Issues

### Notifications Not Appearing

**macOS**:
1. System Preferences → Notifications
2. Find Eye Health Assistant
3. Ensure notifications are enabled

**Windows**:
1. Settings → System → Notifications
2. Ensure notifications are enabled for Eye Health Assistant

### Too Many Notifications

Adjust notification settings:
- Settings → Notifications → Reminder Frequency
- Settings → Notifications → Quiet Hours
- Settings → Notifications → Minimum Interval

## Database Issues

### Corrupted Database

If the application behaves strangely:
1. Go to Settings → Privacy → Delete All Data
2. Or manually delete the database file from the application data directory

### Database Location

Find your database:
- **macOS**: `~/Library/Application Support/EyeHealthAssistant/database/app.sqlite`
- **Windows**: `AppData/Local/EyeHealthAssistant/database/app.sqlite`
- **Linux**: `~/.local/share/EyeHealthAssistant/database/app.sqlite`

## Performance Issues

### High CPU Usage

- Ensure camera processing is not running when not needed
- Check if Smart Mode is active unnecessarily
- Reduce monitoring frequency in Settings → Monitoring

### Application Freezing

- Check available system memory
- Close other resource-intensive applications
- Restart the application

## Getting Help

If your issue isn't resolved:
1. Check the application logs in the logs directory
2. Open an issue on the project repository
3. Include your OS version and application version
