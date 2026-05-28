import pytest
from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_freeze_preparation_review_payload
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
from usa_signal_bot.feature_engine.final_closure.final_closure_checks import run_final_closure_checks

def test_final_closure_checks_fail():
    payload = {"context": {"ready_for_phase125": False}}
    ingestion = ingest_freeze_preparation_review_payload(payload)
    artifacts = build_final_artifact_references()
    res = run_final_closure_checks(ingestion, artifacts)
    assert res.closure_passed is False

def test_final_closure_checks_pass():
    payload = {"context": {
        "artifact_chain_ready": True, "integration_rehearsal_ready": True, "report_qa_accepted": True,
        "freeze_candidate_ready": True, "freeze_readiness_gate_ready": True, "ready_for_phase125": True,
        "research_data_only": True
    }}
    ingestion = ingest_freeze_preparation_review_payload(payload)
    artifacts = build_final_artifact_references()
    for a in artifacts:
        a.available = True
    res = run_final_closure_checks(ingestion, artifacts)
    assert res.closure_passed is True
