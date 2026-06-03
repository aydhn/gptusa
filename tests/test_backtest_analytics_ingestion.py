import pytest
from usa_signal_bot.backtesting.benchmark_comparison.backtest_analytics_ingestion import (
    ingest_backtest_analytics_review_payload
)

def test_ingest_valid_payload():
    payload = {
        "context": {"context_id": "ctx-1"},
        "analytics_report": {"report_id": "r-1"},
        "run_validation": {"val_id": "v-1"},
        "safety_boundary": {"passed": True},
        "phase149_readiness_gate": {"ready_for_phase149": True, "passed": True},
        "research_data_only": True
    }
    result = ingest_backtest_analytics_review_payload(payload)
    assert result.available is True
    assert result.valid_for_phase149 is True

def test_ingest_blocked_payload():
    payload = {
        "context": {"context_id": "ctx-1"},
        "analytics_report": {"report_id": "r-1"},
        "run_validation": {"val_id": "v-1"},
        "safety_boundary": {"passed": True},
        "phase149_readiness_gate": {"ready_for_phase149": False},
        "research_data_only": True
    }
    result = ingest_backtest_analytics_review_payload(payload)
    assert result.valid_for_phase149 is False
