import json
from pathlib import Path
from usa_signal_bot.portfolio.foundation.backtest_closure_ingestion import (
    ingest_backtest_closure_review_payload, backtest_closure_supports_phase153
)

def test_ingest_backtest_closure_review_payload(tmp_path):
    payload = {
        "ready_for_phase153": True,
        "research_data_only": True,
        "review_id": "test-id",
        "phase153_readiness_gate": {"ready_for_phase153": True},
        "handoff_safety_boundary": {"boundary_passed": True},
        "phase153_handoff_contract_built": True,
        "phase153_handoff_package_built": True
    }

    res = ingest_backtest_closure_review_payload(payload)
    assert res.valid_for_phase153 is True
    assert len(res.errors) == 0

def test_ingest_unsafe_closure():
    payload = {
        "ready_for_phase153": True,
        "research_data_only": True,
        "review_id": "test-id",
        "phase153_readiness_gate": {"ready_for_phase153": True},
        "handoff_safety_boundary": {"boundary_passed": True},
        "live_trading_enabled": True
    }

    res = ingest_backtest_closure_review_payload(payload)
    assert res.valid_for_phase153 is False
    assert len(res.errors) > 0
