import pytest
from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_freeze_preparation_review_payload

def test_ingest_freeze_preparation_valid():
    payload = {
        "context": {
            "artifact_chain_ready": True,
            "integration_rehearsal_ready": True,
            "report_qa_accepted": True,
            "freeze_candidate_ready": True,
            "freeze_readiness_gate_ready": True,
            "ready_for_phase125": True,
            "research_data_only": True
        }
    }
    res = ingest_freeze_preparation_review_payload(payload)
    assert res.valid_for_phase125 is True

def test_ingest_freeze_preparation_invalid():
    payload = {
        "context": {
            "ready_for_phase125": False,
            "broker_execution_enabled": True
        }
    }
    res = ingest_freeze_preparation_review_payload(payload)
    assert res.valid_for_phase125 is False
