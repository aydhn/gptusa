import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.prediction_correlation_diagnostics import build_prediction_correlation_diagnostics
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_candidate_resolver import build_ensemble_candidate_references

def test_build_pred_corr():
    reports = [{"candidate_id": f"cand_{i}", "rank": i, "warning_count": 0} for i in range(2)]
    validations = [{"candidate_id": f"cand_{i}", "passed": True} for i in range(2)]
    cands = build_ensemble_candidate_references(reports, validations)

    diags = build_prediction_correlation_diagnostics(cands)
    assert len(diags) > 0
    for d in diags:
        assert d.investment_advice is False
        assert d.produces_trade_signal is False
