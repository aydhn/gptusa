from typing import Any
import json
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    ServiceGraphIngestionResult,
    StartupCheckItem,
    StartupCheckReport,
    ServiceReadinessItem,
    ServiceReadinessMatrix,
    ReadinessGate,
    LifecycleTransition,
    RuntimeLifecycleContext,
    RuntimeLifecycleFullReview
)

def service_graph_ingestion_result_to_text(item: ServiceGraphIngestionResult) -> str:
    return f"ServiceGraphIngestionResult: valid={item.service_graph_valid}, dry_run={item.dry_run_passed}, execution={item.execution_performed}"

def startup_check_item_to_text(item: StartupCheckItem) -> str:
    return f"StartupCheck [{item.check_type.value}]: {item.status.value} - {item.message}"

def startup_check_report_to_text(item: StartupCheckReport, limit: int = 200) -> str:
    text = f"StartupCheckReport [{item.status.value}]: Passed {item.passed_checks}/{item.total_checks}"
    return text[:limit]

def service_readiness_item_to_text(item: ServiceReadinessItem) -> str:
    return f"ServiceReadiness [{item.service_name}]: {item.readiness_status.value}"

def service_readiness_matrix_to_text(item: ServiceReadinessMatrix, limit: int = 300) -> str:
    text = f"ServiceReadinessMatrix: Ready {item.ready_services}/{item.total_services}, NoExecutionReady={item.no_execution_ready}"
    return text[:limit]

def readiness_gate_to_text(item: ReadinessGate, limit: int = 200) -> str:
    text = f"ReadinessGate [{item.status.value}]: Decision={item.decision.value}, Passed={item.gate_passed}, Phase105Ready={item.ready_for_phase105}"
    return text[:limit]

def lifecycle_transition_to_text(item: LifecycleTransition) -> str:
    return f"Transition [{item.from_status.value} -> {item.to_status.value}]: {item.transition_status.value} ({item.reason})"

def runtime_lifecycle_context_to_text(item: RuntimeLifecycleContext, limit: int = 300) -> str:
    text = f"RuntimeLifecycleContext [{item.status.value}]: Decision={item.decision.value}, Phase105Ready={item.ready_for_phase105}"
    return text[:limit]

def runtime_lifecycle_full_review_to_text(item: RuntimeLifecycleFullReview, limit: int = 300) -> str:
    text = f"FullReview [{item.report_type.value}]: Gate={item.readiness_gate.decision.value if item.readiness_gate else 'None'}, Issues={len(item.errors)}"
    return text[:limit]

def lifecycle_store_summary_to_text(summary: dict) -> str:
    return json.dumps(summary, indent=2)

def runtime_lifecycle_limitations_text() -> str:
    return (
        "LIMITATION: Phase 104 is STRICTLY a local metadata readiness evaluation phase.\n"
        "It does NOT perform broker API calls, network fetches, live trades, or actual active paper runs.\n"
        "Any 'READY' status is strictly a local metadata state and is NOT a financial investment advice or live execution approval."
    )
