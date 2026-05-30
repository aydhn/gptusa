import os
import re
from pathlib import Path

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

ensure_dir("usa_signal_bot/regime_classification/monitoring")
ensure_dir("tests/fixtures/regime_monitoring")
ensure_dir("docs")
