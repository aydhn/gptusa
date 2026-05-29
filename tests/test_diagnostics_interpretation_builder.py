from usa_signal_bot.regime_classification.behavior_reporting.diagnostics_interpretation_builder import (
    build_diagnostics_interpretations, validate_diagnostics_interpretations
)

def test_build_diagnostics_interpretations():
    payloads = {
        "transition_matrices": [{"symbol": "AAPL"}],
        "persistence_profiles": [{"symbol": "MSFT"}],
    }
    ints = build_diagnostics_interpretations(payloads)
    assert len(ints) == 2
    assert ints[0].symbol == "AAPL"
    assert ints[1].symbol == "MSFT"

def test_validate_diagnostics_interpretations():
    payloads = {
        "transition_matrices": [{"symbol": "AAPL"}],
    }
    ints = build_diagnostics_interpretations(payloads)
    errs = validate_diagnostics_interpretations(ints)
    assert not errs
