import pytest
from usa_signal_bot.regime_classification.validation.regime_alignment_ingestion import (
    ingest_regime_alignment_review_payload
)

def test_ingest_regime_alignment_valid():
    payload = {
        "review_id": "rev_1",
        "context": {
            "context_id": "ctx_1",
            "market_behavior_ingested": True,
            "frozen_factors_loaded": True,
            "behavior_artifacts_loaded": True,
            "alignment_specs_ready": True,
            "overlays_built": True,
            "compatibility_computed": True,
            "diagnostics_built": True,
            "readiness_gate_ready": True,
            "ready_for_phase132": True,
            "metadata_only": True,
            "research_data_only": True
        }
    }
    res = ingest_regime_alignment_review_payload(payload)
    assert res.valid_for_phase132 is True
    assert res.errors == []

def test_ingest_regime_alignment_invalid():
    payload = {
        "review_id": "rev_2",
        "context": {
            "context_id": "ctx_2",
            "market_behavior_ingested": False,
            "ready_for_phase132": False
        }
    }
    res = ingest_regime_alignment_review_payload(payload)
    assert res.valid_for_phase132 is False
    assert len(res.errors) > 0
