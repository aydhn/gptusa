"""Path management and resolution utilities."""

import os
from pathlib import Path

# Assuming paths.py is at usa_signal_bot/core/paths.py
# The project root is two levels up from this file's directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"

LOGS_DIR = DATA_DIR / "logs"
REPORTS_DIR = DATA_DIR / "reports"
CACHE_DIR = DATA_DIR / "cache"
PAPER_DIR = DATA_DIR / "paper"
BACKTESTS_DIR = DATA_DIR / "backtests"

def ensure_directories() -> None:
    """Ensure all required core directories exist."""
    directories = [
        CONFIG_DIR,
        DATA_DIR,
        LOGS_DIR,
        REPORTS_DIR,
        CACHE_DIR,
        PAPER_DIR,
        BACKTESTS_DIR
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
