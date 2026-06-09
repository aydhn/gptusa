import os
from pathlib import Path

def create_dirs():
    dirs = [
        "usa_signal_bot/integration",
        "usa_signal_bot/portfolio/risk_reporting",
        "usa_signal_bot/core",
        "usa_signal_bot/app",
        "usa_signal_bot/quality",
        "usa_signal_bot/observability",
        "usa_signal_bot/notifications",
        "tests/fixtures/full_system_integration",
        "docs",
        "config"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

create_dirs()
