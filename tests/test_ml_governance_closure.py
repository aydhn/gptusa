import pytest
import pandas as pd
from usa_signal_bot.ml_research.ml_governance_closure.drift_monitoring_ingestion import ingest_drift_monitoring_review_payload
from usa_signal_bot.ml_research.ml_governance_closure.feature_attribution_proxy import build_feature_attribution_proxies
from usa_signal_bot.ml_research.ml_governance_closure.factor_contribution_summary import build_factor_contribution_summaries
from usa_signal_bot.ml_research.ml_governance_closure.ml_closure_safety_validator import validate_ml_closure_dataframe_output_safety, ml_closure_text_has_trade_or_execution_language

def test_ingest_drift_monitoring_review():
    payload = {
        "review_id": "rev-123",
        "context": {
            "context_id": "ctx-123",
            "ensemble_prototype_ingested": True,
            "drift_inputs_resolved": True,
            "monitoring_metadata_package_built": True,
            "post_ensemble_governance_built": True,
            "non_activation_boundary_validated": True,
            "model_cards_updated": True,
            "readiness_gate_built": True
        },
        "monitoring_metadata_package": {"mock": True},
        "post_ensemble_governance": {"mock": True},
        "non_activation_drift_boundary": {
            "research_data_only": True,
            "live_monitoring_enabled": False,
            "produces_trade_signal": False
        },
        "drift_readiness_gate": {
            "gate_passed": True,
            "ready_for_phase145": True
        }
    }
    result = ingest_drift_monitoring_review_payload(payload)
    assert result.valid_for_phase145 is True
    assert result.research_data_only is True
    assert result.produces_trade_signal is False

def test_feature_attribution_proxy_builder():
    df = pd.DataFrame({
        "feature_1": [1.0, 2.0, 3.0],
        "feature_2": [-1.0, -0.5, 0.5]
    })
    proxies = build_feature_attribution_proxies(df)
    assert len(proxies) == 2
    assert proxies[0].not_trade_signal is True
    assert proxies[0].produces_trade_signal is False

def test_factor_contribution_summary_builder():
    df = pd.DataFrame({
        "momentum_1": [10.0, 12.0],
        "volatility_1": [1.5, 2.0]
    })
    summaries = build_factor_contribution_summaries(df)
    assert len(summaries) == 2
    assert summaries[0].not_portfolio_weight is True
    assert summaries[0].produces_portfolio_weights is False

def test_ml_closure_safety_validator():
    df = pd.DataFrame({"good_col": [1], "buy_signal": [1]})
    errors = validate_ml_closure_dataframe_output_safety(df)
    assert len(errors) > 0
    assert any("Forbidden fragment" in e for e in errors)

    assert ml_closure_text_has_trade_or_execution_language("guaranteed profit") is True
    assert ml_closure_text_has_trade_or_execution_language("This is a research proxy") is False
