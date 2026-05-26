
import pytest
from usa_signal_bot.provider_final_acceptance.provider_freeze_ingestion import ingest_provider_freeze_review_payload

def test_ingest_provider_freeze_review_payload():
    payload = {
        "review_id": "test_1",
        "context": {
            "provider_expansion_frozen": True,
            "multi_provider_review_passed": True,
            "data_layer_rehearsal_passed": True,
            "output_contracts_passed": True,
            "ready_for_phase115": True,
            "metadata_only": True,
            "research_data_only": True,
            "activation_allowed": False
        }
    }
    res = ingest_provider_freeze_review_payload(payload)
    assert res.valid_for_phase115 == True

def test_invalid_ingest_provider_freeze_review_payload():
    payload = {
        "context": {
            "provider_expansion_frozen": True,
            "ready_for_phase115": True,
            "activation_allowed": True # This should invalidate it
        }
    }
    res = ingest_provider_freeze_review_payload(payload)
    assert res.valid_for_phase115 == False
