import pytest
from usa_signal_bot.backtesting.benchmark_comparison.backtest_analytics_artifact_loader import (
    validate_backtest_analytics_artifacts
)

def test_validate_artifacts():
    payloads = {
        "safe": {"test": True},
        "unsafe": {"broker_order": True}
    }
    errors = validate_backtest_analytics_artifacts(payloads)
    assert len(errors) == 1
    assert "broker_order" in errors[0]
