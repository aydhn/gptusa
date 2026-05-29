from usa_signal_bot.regime_classification.behavior_reporting.regime_transition_ingestion import (
    ingest_regime_transition_review_payload
)

def test_ingest_regime_transition_review_payload():
    payload = {
        "review_id": "rev-123",
        "context": {
            "labeling_ingested": True,
            "sequences_loaded": True,
            "transition_matrix_built": True,
            "persistence_analytics_built": True,
            "duration_analytics_built": True,
            "churn_diagnostics_built": True,
            "stability_diagnostics_built": True,
            "readiness_gate_ready": True,
            "ready_for_phase130": True,
            "research_data_only": True
        }
    }
    res = ingest_regime_transition_review_payload(payload)
    assert res.available is True
    assert res.valid_for_phase130 is True

def test_ingest_regime_transition_review_blocked():
    payload = {
        "review_id": "rev-123",
        "context": {
            "ready_for_phase130": False
        }
    }
    res = ingest_regime_transition_review_payload(payload)
    assert res.valid_for_phase130 is False
    assert len(res.errors) > 0
