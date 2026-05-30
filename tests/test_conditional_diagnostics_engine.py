import pytest
from usa_signal_bot.regime_classification.validation.conditional_diagnostics_engine import build_conditional_diagnostics
from usa_signal_bot.core.enums import ConditionalDiagnosticKind

def test_build_conditional_diagnostics():
    comp_res = [
        {"compatibility_id": "1", "score": 30, "classification": "low_compatibility"},
        {"compatibility_id": "2", "score": 90, "classification": "high_compatibility"}
    ]
    diags = build_conditional_diagnostics(comp_res, [], [])
    assert len(diags) > 0
    assert any(d.diagnostic_kind == ConditionalDiagnosticKind.LOW_COMPATIBILITY_DIAGNOSTIC for d in diags)
