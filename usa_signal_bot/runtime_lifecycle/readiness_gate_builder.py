from typing import Dict, Any, Optional
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    StartupCheckReport,
    ServiceReadinessMatrix,
    ReadinessGate,
    create_readiness_gate_id,
    _now_str
)
from usa_signal_bot.core.enums import ReadinessGateStatus, ReadinessGateDecision

def build_readiness_gate(
    startup_report: StartupCheckReport,
    readiness_matrix: ServiceReadinessMatrix,
    source_service_graph_review_id: Optional[str] = None
) -> ReadinessGate:
    passed = startup_report.startup_checks_passed and readiness_matrix.all_required_services_ready

    return ReadinessGate(
        gate_id=create_readiness_gate_id(),
        created_at_utc=_now_str(),
        status=ReadinessGateStatus.CREATED,
        decision=ReadinessGateDecision.UNKNOWN,
        source_service_graph_review_id=source_service_graph_review_id,
        source_startup_report_id=startup_report.report_id,
        source_readiness_matrix_id=readiness_matrix.matrix_id,
        startup_report=startup_report,
        readiness_matrix=readiness_matrix,
        gate_passed=passed,
        metadata_only=True,
        read_only=True,
        ready_for_phase105=passed,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        execution_performed=False,
        network_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        scraping_used=False,
        dashboard_started=False,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def build_default_readiness_gate() -> ReadinessGate:
    return ReadinessGate(
        gate_id=create_readiness_gate_id(),
        created_at_utc=_now_str(),
        status=ReadinessGateStatus.DRAFT,
        decision=ReadinessGateDecision.UNKNOWN,
        source_service_graph_review_id=None,
        source_startup_report_id=None,
        source_readiness_matrix_id=None,
        startup_report=None,
        readiness_matrix=None,
        gate_passed=False,
        metadata_only=True,
        read_only=True,
        ready_for_phase105=False,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        dashboard_enabled=False,
        execution_performed=False,
        network_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        scraping_used=False,
        dashboard_started=False,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def readiness_gate_summary(gate: ReadinessGate) -> Dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "decision": gate.decision.value,
        "passed": gate.gate_passed
    }

def readiness_gate_to_text(gate: ReadinessGate, limit: int = 200) -> str:
    from usa_signal_bot.runtime_lifecycle.lifecycle_reporting import readiness_gate_to_text as _to_text
    return _to_text(gate, limit)
