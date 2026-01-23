"""
Quick start setup guide for YouTube Automation System.
Run this script to verify and set up your environment.
"""

import sys
import os
from pathlib import Path
import subprocess

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
END = "\033[0m"


def print_status(message, status="info"):
    """Print colored status message."""
    if status == "success":
        print(f"{GREEN}✓{END} {message}")
    elif status == "error":
        print(f"{RED}✗{END} {message}")
    elif status == "warning":
        print(f"{YELLOW}⚠{END} {message}")
    elif status == "info":
        print(f"{BLUE}ℹ{END} {message}")


def check_python():
    """Check Python version."""
    print(f"\n{BLUE}=== Checking Python Installation ==={END}")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 8):
        print_status(f"Python {version} (compatible)", "success")
        return True
    else:
        print_status(f"Python {version} (requires 3.8+)", "error")
        return False


def check_dependencies():
    """Check if dependencies are installed."""
    print(f"\n{BLUE}=== Checking Dependencies ==={END}")
    
    required = [
        "google.auth",
        "youtube_transcript_api",
        "pandas",
        "spacy",
        "vaderSentiment",
        "plotly",
        "pptx",
        "requests",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print_status(f"{package}", "success")
        except ImportError:
            print_status(f"{package}", "error")
            missing.append(package)
    
    return len(missing) == 0, missing


def install_dependencies():
    """Install dependencies from requirements.txt."""
    print(f"\n{BLUE}=== Installing Dependencies ==={END}")
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=Path(__file__).parent
        )
        print_status("Dependencies installed successfully", "success")
        return True
    except subprocess.CalledProcessError:
        print_status("Failed to install dependencies", "error")
        return False


def check_spacy_model():
    """Check if spaCy model is installed."""
    print(f"\n{BLUE}=== Checking spaCy Model ==={END}")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print_status("spaCy model 'en_core_web_sm' found", "success")
        return True
    except OSError:
        print_status("spaCy model 'en_core_web_sm' not found", "warning")
        print(f"{YELLOW}Run: python -m spacy download en_core_web_sm{END}")
        return False


def check_config():
    """Check if configuration is set up."""
    print(f"\n{BLUE}=== Checking Configuration ==={END}")
    
    # Check for .env file or environment variables
    has_api_key = bool(os.getenv("YOUTUBE_API_KEY"))
    has_gmail_email = bool(os.getenv("GMAIL_SENDER_EMAIL"))
    has_gmail_pass = bool(os.getenv("GMAIL_APP_PASSWORD"))
    
    if has_api_key:
        print_status("YOUTUBE_API_KEY environment variable found", "success")
    else:
        print_status("YOUTUBE_API_KEY not set", "warning")
    
    if has_gmail_email:
        print_status("GMAIL_SENDER_EMAIL environment variable found", "success")
    else:
        print_status("GMAIL_SENDER_EMAIL not set", "warning")
    
    if has_gmail_pass:
        print_status("GMAIL_APP_PASSWORD environment variable found", "success")
    else:
        print_status("GMAIL_APP_PASSWORD not set", "warning")
    
    return has_api_key and has_gmail_email and has_gmail_pass


def check_directories():
    """Check if required directories exist."""
    print(f"\n{BLUE}=== Checking Directory Structure ==={END}")
    
    base_path = Path(__file__).parent
    dirs_to_create = [
        base_path / "data",
        base_path / "data" / "transcripts",
        base_path / "reports",
        base_path / "reports" / "charts",
        base_path / "logs",
    ]
    
    for directory in dirs_to_create:
        if directory.exists():
            print_status(f"{directory.relative_to(base_path)}", "success")
        else:
            print_status(f"{directory.relative_to(base_path)} (will be created)", "warning")
            directory.mkdir(parents=True, exist_ok=True)


def print_next_steps():
    """Print next steps for user."""
    print(f"\n{BLUE}=== Next Steps ==={END}")
    
    print("""
1. {YELLOW}Set up API Credentials:{END}
   
   YouTube API:
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable YouTube Data API v3
   - Create API key
   - Run: export YOUTUBE_API_KEY="your_key_here"
   
   Gmail (optional, for email delivery):
   - Enable 2-Factor Authentication on Google Account
   - Go to https://myaccount.google.com/apppasswords
   - Generate app password
   - Run commands:
     export GMAIL_SENDER_EMAIL="your-email@gmail.com"
     export GMAIL_APP_PASSWORD="your_app_password"
     export GMAIL_RECIPIENT="recipient@example.com"

2. {YELLOW}Verify Installation:{END}
   python setup.py  # Re-run this script

3. {YELLOW}Run Pipeline:{END}
   python main.py --skip-email  # Test without email
   python main.py                # Full pipeline with email

4. {YELLOW}View Results:{END}
   - Data: data/videos.csv
   - Transcripts: data/transcripts/
   - Reports: reports/YouTube_Trends_Report_*.pptx
   - Logs: logs/youtube_automation.log

5. {YELLOW}Documentation:{END}
   See README.md for detailed usage and configuration
    """.format(YELLOW=YELLOW, END=END))


def main():
    """Run setup checks."""
    print(f"\n{BLUE}{'='*60}")
    print(f"YouTube Automation System - Setup Verification")
    print(f"{'='*60}{END}\n")
    
    # Run checks
    python_ok = check_python()
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print_status("Installing missing dependencies...", "warning")
        if install_dependencies():
            deps_ok, missing = check_dependencies()
    
    spacy_ok = check_spacy_model()
    if not spacy_ok:
        response = input(f"\n{YELLOW}Install spaCy model now? (y/n): {END}").strip().lower()
        if response == 'y':
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
                )
                spacy_ok = check_spacy_model()
            except:
                print_status("Failed to install spaCy model", "error")
    
    config_ok = check_config()
    check_directories()
    
    # Print summary
    print(f"\n{BLUE}=== Setup Summary ==={END}")
    print_status("Python", "success" if python_ok else "error")
    print_status("Dependencies", "success" if deps_ok else "error")
    print_status("spaCy Model", "success" if spacy_ok else "warning")
    print_status("Configuration", "success" if config_ok else "warning")
    
    if not config_ok:
        print_next_steps()
    else:
        print(f"\n{GREEN}✓ Setup complete! Run: python main.py{END}\n")


if __name__ == "__main__":
    main()
