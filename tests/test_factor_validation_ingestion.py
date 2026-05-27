import pytest
from usa_signal_bot.feature_engine.factor_explainability.factor_validation_ingestion import ingest_factor_validation_review_payload

def test_ingest_factor_validation_review_payload():
    payload = {
        "review_id": "r1",
        "validation_ready": True,
        "drift_ready": True,
        "versioning_ready": True,
        "store_hardened": True,
        "activation_allowed": False
    }
    res = ingest_factor_validation_review_payload(payload)
    assert res.valid_for_phase123 is True
    assert res.ready_for_phase123 is True

def test_ingest_factor_validation_review_payload_invalid():
    payload = {
        "validation_ready": True
    }
    res = ingest_factor_validation_review_payload(payload)
    assert res.valid_for_phase123 is False
    assert "Missing review_id in payload" in res.warnings
