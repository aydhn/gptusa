import pytest
from usa_signal_bot.regime_map.backtest_adapter import attach_regime_map_to_backtest_result, backtest_regime_map_summary

def test_attach_regime_map_to_backtest_result():
    result = {"metrics": {}}
    enriched = attach_regime_map_to_backtest_result(result, None)
    assert "metadata" in enriched

def test_backtest_regime_map_summary():
    summary = backtest_regime_map_summary({"metadata": {"regime_warning_count": 5}})
    assert summary["regime_warning_count"] == 5
