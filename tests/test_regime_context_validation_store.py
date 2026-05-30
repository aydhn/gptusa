import pytest
from pathlib import Path
from usa_signal_bot.regime_classification.validation.regime_context_validation_store import regime_context_validation_store_summary

def test_store_summary():
    s = regime_context_validation_store_summary(Path("/tmp/mock_data_root"))
    assert s["reviews"] == 0
