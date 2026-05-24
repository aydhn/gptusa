import pytest
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    ServiceGraphIngestionResult,
    StartupCheckReport,
    ServiceReadinessMatrix,
    ReadinessGate,
    RuntimeLifecycleContext,
    validate_service_graph_ingestion_result,
    validate_startup_check_report,
    validate_service_readiness_matrix,
    validate_readiness_gate,
    validate_runtime_lifecycle_context
)
from usa_signal_bot.core.enums import RuntimeLifecycleStatus, ReadinessGateStatus, ReadinessGateDecision
from usa_signal_bot.core.exceptions import LifecycleValidationError

def test_service_graph_ingestion_validation():
    # Valid model
    sgi = ServiceGraphIngestionResult(
        ingestion_id="SGI-test", created_at_utc="2025-01-01T00:00:00Z",
        source_path=None, source_review_id=None, source_graph_id=None,
        available=True, service_graph_valid=True, dry_run_passed=True,
        graph_has_cycles=False, missing_dependency_count=0, invalid_contract_count=0, blocked_route_count=0,
        execution_performed=False, network_used=False, broker_used=False, order_created=False,
        paper_state_mutated=False, telegram_real_sent=False, scraping_used=False, dashboard_started=False,
        valid_for_phase104=True, risk_flags=[], warnings=[], errors=[], metadata={}
    )
    validate_service_graph_ingestion_result(sgi) # Should not raise

    # Invalid model
    sgi.execution_performed = True
    with pytest.raises(LifecycleValidationError):
        validate_service_graph_ingestion_result(sgi)

def test_startup_check_report_validation():
    scr = StartupCheckReport(
        report_id="SCR-test", created_at_utc="2025-01-01T00:00:00Z",
        status=RuntimeLifecycleStatus.CREATED, total_checks=10, passed_checks=10, warning_checks=0, failed_checks=0, blocked_checks=0, skipped_checks=0, items=[],
        startup_checks_passed=True, startup_checks_metadata_only=True,
        execution_performed=False, network_used=False, broker_used=False, order_created=False,
        paper_state_mutated=False, telegram_real_sent=False, scraping_used=False, dashboard_started=False,
        risk_flags=[], warnings=[], errors=[], metadata={}
    )
    validate_startup_check_report(scr)

    scr.network_used = True
    with pytest.raises(LifecycleValidationError):
        validate_startup_check_report(scr)

    scr.network_used = False
    scr.startup_checks_metadata_only = False
    with pytest.raises(LifecycleValidationError):
        validate_startup_check_report(scr)

def test_readiness_gate_validation():
    gate = ReadinessGate(
        gate_id="RG-test", created_at_utc="2025-01-01T00:00:00Z",
        status=ReadinessGateStatus.CREATED, decision=ReadinessGateDecision.PASS_TO_PHASE105_CORE_ACCEPTANCE,
        source_service_graph_review_id=None, source_startup_report_id=None, source_readiness_matrix_id=None,
        startup_report=None, readiness_matrix=None,
        gate_passed=True, metadata_only=True, read_only=True, ready_for_phase105=True,
        activation_allowed=False, active_paper_enabled=False, broker_execution_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False, dashboard_enabled=False,
        execution_performed=False, network_used=False, broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False, scraping_used=False, dashboard_started=False,
        risk_flags=[], required_followups=[], warnings=[], errors=[], metadata={}
    )
    validate_readiness_gate(gate)

    gate.activation_allowed = True
    with pytest.raises(LifecycleValidationError):
        validate_readiness_gate(gate)
