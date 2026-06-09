from usa_signal_bot.portfolio.risk_reporting.optimizer_prototype_ingestion import (
    ingest_optimizer_prototype_review_payload
)

def test_ingest_optimizer_prototype_review_payload_valid():
    payload = {
        "review_id": "test",
        "phase157_readiness_gate": {"ready_for_phase157": True},
        "safety_boundary": {"boundary_passed": True},
        "research_data_only": True
    }
    res = ingest_optimizer_prototype_review_payload(payload)
    assert res.valid_for_phase157 is True
    assert res.live_trading_enabled is False

def test_ingest_optimizer_prototype_review_payload_blocked():
    payload = {
        "review_id": "test",
        "actual_target_weights_produced": True,
        "phase157_readiness_gate": {"ready_for_phase157": True},
        "safety_boundary": {"boundary_passed": True}
    }
    res = ingest_optimizer_prototype_review_payload(payload)
    assert res.valid_for_phase157 is False
