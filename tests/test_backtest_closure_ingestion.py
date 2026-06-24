import json
from pathlib import Path
from usa_signal_bot.portfolio.foundation.backtest_closure_ingestion import (
    ingest_backtest_closure_review_payload,
    backtest_closure_supports_phase153,
    ingest_latest_backtest_closure_review_from_store,
)


def test_ingest_backtest_closure_review_payload(tmp_path):
    payload = {
        "ready_for_phase153": True,
        "research_data_only": True,
        "review_id": "test-id",
        "phase153_readiness_gate": {"ready_for_phase153": True},
        "handoff_safety_boundary": {"boundary_passed": True},
        "phase153_handoff_contract_built": True,
        "phase153_handoff_package_built": True,
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
        "live_trading_enabled": True,
    }

    res = ingest_backtest_closure_review_payload(payload)
    assert res.valid_for_phase153 is False
    assert len(res.errors) > 0


def test_ingest_latest_review_from_store_success(tmp_path):
    reviews_dir = tmp_path / "backtesting" / "closure" / "reviews"
    reviews_dir.mkdir(parents=True)

    payload = {
        "ready_for_phase153": True,
        "research_data_only": True,
        "review_id": "test-id",
        "phase153_readiness_gate": {"ready_for_phase153": True},
        "handoff_safety_boundary": {"boundary_passed": True},
        "phase153_handoff_contract_built": True,
        "phase153_handoff_package_built": True,
    }

    file_path = reviews_dir / "review_1.json"
    with open(file_path, "w") as f:
        json.dump(payload, f)

    res = ingest_latest_backtest_closure_review_from_store(tmp_path)
    assert res.valid_for_phase153 is True
    assert len(res.errors) == 0
    assert res.source_path == str(file_path)


def test_ingest_latest_review_from_store_missing_dir(tmp_path):
    res = ingest_latest_backtest_closure_review_from_store(tmp_path)
    assert res.valid_for_phase153 is False
    assert len(res.errors) == 1
    assert "does not exist" in res.errors[0]


def test_ingest_latest_review_from_store_no_files(tmp_path):
    reviews_dir = tmp_path / "backtesting" / "closure" / "reviews"
    reviews_dir.mkdir(parents=True)

    res = ingest_latest_backtest_closure_review_from_store(tmp_path)
    assert res.valid_for_phase153 is False
    assert len(res.errors) == 1
    assert "No review files found" in res.errors[0]


def test_ingest_latest_review_from_store_invalid_json(tmp_path):
    reviews_dir = tmp_path / "backtesting" / "closure" / "reviews"
    reviews_dir.mkdir(parents=True)

    file_path = reviews_dir / "review_bad.json"
    with open(file_path, "w") as f:
        f.write("{invalid json format]")

    res = ingest_latest_backtest_closure_review_from_store(tmp_path)
    assert res.valid_for_phase153 is False
    assert len(res.errors) == 1
    assert (
        "Expecting property name enclosed in double quotes" in res.errors[0]
        or "Invalid control character" in res.errors[0]
        or "Expecting value" in res.errors[0]
    )
