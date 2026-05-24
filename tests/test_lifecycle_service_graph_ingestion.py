import pytest
from usa_signal_bot.runtime_lifecycle.service_graph_ingestion import ingest_service_graph_review_payload
from usa_signal_bot.core.enums import LifecycleRiskFlag

def test_ingestion_valid_payload():
    payload = {
        "review_id": "REV-123",
        "runtime_service_graph": {
            "graph_id": "GRAPH-123",
            "is_valid": True,
            "has_cycles": False,
            "missing_dependency_count": 0,
            "invalid_contract_count": 0,
            "blocked_route_count": 0
        },
        "orchestration_dry_run_result": {
            "success": True
        },
        "execution_performed": False,
        "network_used": False,
        "broker_used": False,
        "order_created": False,
        "paper_state_mutated": False,
        "telegram_real_sent": False,
        "scraping_used": False,
        "dashboard_started": False
    }
    result = ingest_service_graph_review_payload(payload)
    assert result.service_graph_valid is True
    assert result.dry_run_passed is True
    assert result.execution_performed is False
    assert result.valid_for_phase104 is True
    assert len(result.errors) == 0

def test_ingestion_blocks_execution_flags():
    payload = {
        "review_id": "REV-123",
        "runtime_service_graph": {"is_valid": True, "has_cycles": False},
        "orchestration_dry_run_result": {"success": True},
        "execution_performed": True,  # This should block Phase 104 processing
        "network_used": False,
        "broker_used": False,
        "order_created": False,
        "paper_state_mutated": False,
        "telegram_real_sent": False,
        "scraping_used": False,
        "dashboard_started": False
    }
    result = ingest_service_graph_review_payload(payload)
    assert result.valid_for_phase104 is False
    assert LifecycleRiskFlag.EXECUTION_ROUTE_RISK in result.risk_flags

def test_ingestion_invalid_graph():
    payload = {
        "review_id": "REV-123",
        "runtime_service_graph": {"is_valid": False, "has_cycles": True},
        "orchestration_dry_run_result": {"success": True}
    }
    result = ingest_service_graph_review_payload(payload)
    assert result.valid_for_phase104 is False
    assert len(result.errors) > 0
    assert LifecycleRiskFlag.SERVICE_GRAPH_INVALID in result.risk_flags
