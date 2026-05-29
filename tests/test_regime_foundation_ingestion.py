import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_foundation_ingestion import (
    ingest_regime_foundation_review_payload
)

def test_ingest_regime_foundation_review_payload():
    payload = {
        "review_id": "test",
        "context": {
            "final_closure_built": True,
            "frozen_artifacts_ready": True,
            "input_bundle_ready": True,
            "market_state_dataset_contract_ready": True,
            "taxonomy_ready": True,
            "non_activation_boundary_passed": True,
            "ready_for_phase127": True,
            "research_data_only": True
        }
    }

    res = ingest_regime_foundation_review_payload(payload)
    assert res.valid_for_phase127 is True
    assert res.activation_allowed is False

def test_ingest_regime_foundation_review_payload_invalid():
    payload = {
        "review_id": "test",
        "context": {
            "ready_for_phase127": False,
        }
    }

    res = ingest_regime_foundation_review_payload(payload)
    assert res.valid_for_phase127 is False
