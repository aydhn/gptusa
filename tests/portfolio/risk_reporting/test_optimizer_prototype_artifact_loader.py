import pytest
from pathlib import Path
from typing import Dict, Any

from usa_signal_bot.portfolio.risk_reporting.optimizer_prototype_artifact_loader import (
    load_optimizer_prototype_artifacts,
)


def test_load_optimizer_prototype_artifacts_returns_dict():
    """Verify load_optimizer_prototype_artifacts returns a dictionary."""
    data_root = Path("/tmp/mock_data_root")
    result = load_optimizer_prototype_artifacts(data_root)
    assert isinstance(result, dict)
    assert result == {}


def test_load_optimizer_prototype_artifacts_accepts_none():
    """Verify load_optimizer_prototype_artifacts accepts None for data_root."""
    result = load_optimizer_prototype_artifacts(None)
    assert isinstance(result, dict)
    assert result == {}
