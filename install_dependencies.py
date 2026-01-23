"""
Utility script to help install and verify all dependencies.
Run this if you encounter any issues with imports or installations.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a shell command and report status."""
    if description:
        print(f"\n➜ {description}")
    print(f"  Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ Success")
            return True
        else:
            print(f"  ✗ Failed")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False


def main():
    print("=" * 70)
    print("YouTube Automation System - Dependency Installer")
    print("=" * 70)
    
    project_root = Path(__file__).parent
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"\n✗ requirements.txt not found at {requirements_file}")
        print("  Make sure you're in the youtube_automation directory")
        return
    
    print("\nSTEP 1: Upgrade pip, setuptools, and wheel")
    print("-" * 70)
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
        "Upgrading package tools..."
    )
    
    print("\nSTEP 2: Install Python dependencies from requirements.txt")
    print("-" * 70)
    success = run_command(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
        "Installing dependencies from requirements.txt..."
    )
    
    if not success:
        print("\n⚠ Installation had issues. Trying alternative approach...")
        print("Installing packages individually...\n")
        
        packages = [
            "google-auth-oauthlib",
            "google-auth-httplib2",
            "google-api-python-client",
            "yt-dlp",
            "youtube-transcript-api",
            "pandas",
            "numpy",
            "spacy",
            "vaderSentiment",
            "plotly",
            "python-pptx",
            "requests",
            "beautifulsoup4",
            "sqlalchemy",
        ]
        
        for package in packages:
            run_command(
                [sys.executable, "-m", "pip", "install", package],
                f"Installing {package}..."
            )
    
    print("\nSTEP 3: Download spaCy language model")
    print("-" * 70)
    run_command(
        [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
        "Downloading spaCy English model..."
    )
    
    print("\nSTEP 4: Install Plotly image rendering backend (optional but recommended)")
    print("-" * 70)
    run_command(
        [sys.executable, "-m", "pip", "install", "kaleido"],
        "Installing kaleido for image rendering..."
    )
    
    print("\n" + "=" * 70)
    print("INSTALLATION COMPLETE")
    print("=" * 70)
    
    print("\nNEXT STEPS:")
    print("1. Create .env file from .env.example:")
    print(f"   cp .env.example .env")
    print("\n2. Edit .env with your API credentials:")
    print("   - YouTube API key")
    print("   - Gmail credentials (optional)")
    print("\n3. Verify setup:")
    print(f"   python setup.py")
    print("\n4. Run the pipeline:")
    print(f"   python main.py --skip-email  # Test mode")
    print(f"   python main.py                # Full pipeline")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
