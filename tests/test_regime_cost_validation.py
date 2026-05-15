import pytest
from usa_signal_bot.regime_costs.regime_cost_validation import (
    validate_cost_regime_snapshot_report, validate_no_live_execution_language_in_regime_cost,
    validate_no_sensitive_data_in_regime_cost_payload
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot

def test_validation():
    s = build_cost_regime_snapshot("SPY")
    s.symbol = ""
    res = validate_cost_regime_snapshot_report(s)
    assert res.valid is False
    assert res.error_count == 1

    res2 = validate_no_live_execution_language_in_regime_cost("This is guaranteed fill")
    assert res2.valid is False

    res3 = validate_no_sensitive_data_in_regime_cost_payload({"token": "123"})
    assert res3.valid is False
