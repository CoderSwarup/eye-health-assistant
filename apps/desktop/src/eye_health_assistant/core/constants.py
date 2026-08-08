"""Application constants."""

APP_NAME: str = "Eye Health Assistant"
VERSION: str = "0.1.0"
APP_AUTHOR: str = "Eye Health Assistant Contributors"

# Database
DATABASE_FILENAME: str = "app.sqlite"

# Algorithm versions
SCORE_ALGORITHM_VERSION: str = "1.0"
BLINK_ALGORITHM_VERSION: str = "1.0"

# Default timer settings (seconds)
DEFAULT_FOCUS_DURATION: int = 20 * 60  # 20 minutes
DEFAULT_BREAK_DURATION: int = 20  # 20 seconds
DEFAULT_LONG_BREAK_DURATION: int = 5 * 60  # 5 minutes

# Blink detection defaults
DEFAULT_BLINK_RATE_THRESHOLD: float = 15.0  # blinks per minute
DEFAULT_ROLLING_WINDOW_MINUTES: int = 3
MINIMUM_OBSERVATION_SECONDS: int = 60

# Notification defaults
DEFAULT_MIN_NOTIFICATION_INTERVAL: int = 300  # 5 minutes in seconds
