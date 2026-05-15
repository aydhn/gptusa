import pytest
from usa_signal_bot.regime_map.strategy_adapter import attach_regime_confirmation_to_signal, suppress_candidate_if_regime_conflicted

def test_attach_regime_confirmation_to_signal():
    signal = {"symbol": "SPY", "direction": "LONG"}
    enriched = attach_regime_confirmation_to_signal(signal, None)
    assert enriched["direction"] == "LONG"
    assert "metadata" in enriched

def test_suppress_candidate_if_regime_conflicted():
    candidate = {"symbol": "SPY"}
    enriched = suppress_candidate_if_regime_conflicted(candidate, None)
    assert "regime_map_suppression" not in enriched.get("metadata", {})
