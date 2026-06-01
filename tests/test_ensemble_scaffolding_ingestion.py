from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_scaffolding_ingestion import ingest_ensemble_scaffolding_review_payload

def test_ingest_valid_payload():
    payload = {
        "review_id": "esfr_123",
        "report_type": "ENSEMBLE_SCAFFOLDING_FULL_REVIEW",
        "context": {
            "ready_for_phase143": True,
            "research_data_only": True,
            "offline_ml_research_only": True,
            "activation_allowed": False
        }
    }
    result = ingest_ensemble_scaffolding_review_payload(payload)
    assert result.valid_for_phase143 is True
    assert result.research_data_only is True

def test_ingest_invalid_payload_with_live_inference():
    payload = {
        "review_id": "esfr_123",
        "report_type": "ENSEMBLE_SCAFFOLDING_FULL_REVIEW",
        "context": {
            "ready_for_phase143": True,
            "research_data_only": True,
            "offline_ml_research_only": True,
            "live_inference_enabled": True
        }
    }
    result = ingest_ensemble_scaffolding_review_payload(payload)
    assert result.valid_for_phase143 is False
    assert "Unsafe flag detected: live_inference_enabled=True" in result.errors
