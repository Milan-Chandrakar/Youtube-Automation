"""
Configuration module for YouTube Automation System.
Stores API credentials, settings, and constants.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE")
YOUTUBE_API_QUOTA_LIMIT = 10000  # Daily quota from Google

# Search Parameters
SEARCH_QUERY = "Shivji trending videos"
MAX_VIDEOS_PER_SEARCH = 50
DAYS_BACK = 30
REGIONS = ["US"]  # Add more region codes as needed

# Analysis Parameters
SENTIMENT_THRESHOLD_POSITIVE = 0.05
SENTIMENT_THRESHOLD_NEGATIVE = -0.05
MIN_ENGAGEMENT_THRESHOLD = 100  # Minimum comments/likes to consider

# Database Configuration
DB_PATH = PROJECT_ROOT / "data" / "youtube_data.db"
CSV_EXPORT_PATH = PROJECT_ROOT / "data" / "videos.csv"
TRANSCRIPTS_PATH = PROJECT_ROOT / "data" / "transcripts"

# Gmail Configuration
GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL", "your-email@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "YOUR_APP_PASSWORD_HERE")
GMAIL_RECIPIENT = os.getenv("GMAIL_RECIPIENT", "recipient@example.com")

# Report Configuration
REPORT_TITLE = "Shivji Trending Videos Analysis Report"
REPORT_OUTPUT_PATH = PROJECT_ROOT / "reports"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "logs" / "youtube_automation.log"

# Ensure directories exist
for directory in [DB_PATH.parent, TRANSCRIPTS_PATH, REPORT_OUTPUT_PATH, LOG_FILE.parent]:
    directory.mkdir(parents=True, exist_ok=True)
