import pytest
from usa_signal_bot.regime_classification.freeze_preparation.regime_monitoring_ingestion import (
    ingest_regime_monitoring_review_payload,
    regime_monitoring_supports_phase134,
    regime_monitoring_ingestion_to_text
)
from usa_signal_bot.core.enums import ResearchFreezeRiskFlag

def test_ingest_regime_monitoring_review_payload_valid():
    payload = {
        "review_id": "rev1",
        "context_id": "ctx1",
        "ready_for_phase134": True,
        "baseline_built": True,
        "snapshot_built": True,
        "drift_tracked": True,
        "degradation_diagnostics_built": True,
        "readiness_gate_built": True,
        "readiness_gate_passed": True,
        "activation_allowed": False,
        "deployment_allowed": False,
        "produces_trade_signal": False,
        "investment_advice": False
    }

    res = ingest_regime_monitoring_review_payload(payload)

    assert res.source_review_id == "rev1"
    assert res.source_context_id == "ctx1"
    assert res.ready_for_phase134 is True
    assert res.valid_for_phase134 is True
    assert res.metadata_only is True
    assert res.research_data_only is True
    assert res.activation_allowed is False
    assert len(res.errors) == 0

def test_ingest_regime_monitoring_review_payload_invalid():
    payload = {
        "review_id": "rev2",
        "ready_for_phase134": False,
        "activation_allowed": True,
        "produces_trade_signal": True
    }

    res = ingest_regime_monitoring_review_payload(payload)

    assert res.ready_for_phase134 is False
    assert res.valid_for_phase134 is False
    assert len(res.errors) > 0
    assert ResearchFreezeRiskFlag.PHASE133_NOT_READY in res.risk_flags

def test_regime_monitoring_ingestion_to_text():
    payload = {"ready_for_phase134": True}
    res = ingest_regime_monitoring_review_payload(payload)
    text = regime_monitoring_ingestion_to_text(res)
    assert "Ready: True" in text
