import pytest
from usa_signal_bot.regime_classification.validation.compatibility_validation_runner import run_compatibility_validation
from usa_signal_bot.regime_classification.validation.regime_alignment_ingestion import ingest_regime_alignment_review_payload

def test_run_compatibility_validation_pass():
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
    ingestion = ingest_regime_alignment_review_payload(payload)
    comp_res = [{"compatibility_id": "1", "score": 90, "normalized_score": 0.9, "classification": "high"}]
    over_res = [{"score": 90, "normalized_score": 0.9}]
    diag_prof = [{"profile_id": "p1"}]

    res = run_compatibility_validation(ingestion, comp_res, over_res, diag_prof)
    assert res.validation_passed is True

def test_run_compatibility_validation_fail_score():
    payload = {
        "review_id": "rev_1",
        "context": {
            "context_id": "ctx_1",
            "ready_for_phase132": True,
        }
    }
    ingestion = ingest_regime_alignment_review_payload(payload)
    comp_res = [{"compatibility_id": "1", "score": 150, "normalized_score": 1.5, "classification": "high"}]
    over_res = [{"score": 90, "normalized_score": 0.9}]
    diag_prof = [{"profile_id": "p1"}]

    res = run_compatibility_validation(ingestion, comp_res, over_res, diag_prof)
    assert res.validation_passed is False
