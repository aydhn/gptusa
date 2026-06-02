import pytest
from usa_signal_bot.backtesting.advanced_ml_closure_ingestion import ingest_advanced_ml_closure_review_payload

def test_ingest_advanced_ml_closure_review_payload_valid():
    payload = {
        "ready_for_phase146": True,
        "phase136_to_145_closed": True,
        "acceptance_gate_passed": True,
        "research_data_only": True,
        "offline_ml_research_only": True
    }
    res = ingest_advanced_ml_closure_review_payload(payload)
    assert res.valid_for_phase146 is True
    assert res.ready_for_phase146 is True

def test_ingest_advanced_ml_closure_review_payload_invalid():
    payload = {
        "ready_for_phase146": True,
        "phase136_to_145_closed": True,
        "acceptance_gate_passed": True,
        "research_data_only": True,
        "offline_ml_research_only": True,
        "live_trading_enabled": True
    }
    res = ingest_advanced_ml_closure_review_payload(payload)
    assert res.valid_for_phase146 is False
