import pytest
from usa_signal_bot.advanced_runtime.transition_review_ingestion import (
    ingest_advanced_transition_review_payload,
    transition_review_supports_phase102
)
from usa_signal_bot.core.enums import RuntimeRegistryRiskFlag

def test_ingest_valid_payload():
    payload = {
        "review_id": "rev1",
        "context": {
            "status": "VALIDATED",
            "activation_allowed": False
        }
    }
    res = ingest_advanced_transition_review_payload(payload)
    assert res.valid_for_phase102 is True
    assert res.advanced_transition_ready is True
    assert res.current_phase == 102

def test_ingest_invalid_payload():
    payload = {
        "review_id": "rev1",
        "context": {
            "status": "VALIDATED",
            "activation_allowed": True # Not allowed in 102
        }
    }
    res = ingest_advanced_transition_review_payload(payload)
    assert res.valid_for_phase102 is False
    assert RuntimeRegistryRiskFlag.TRANSITION_REVIEW_INVALID in res.risk_flags
