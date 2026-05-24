from typing import Dict, Any, List
from usa_signal_bot.runtime_lifecycle.phase104_models import ReadinessGate
from usa_signal_bot.core.enums import ReadinessGateDecision, ReadinessGateStatus

def evaluate_readiness_gate(gate: ReadinessGate) -> ReadinessGateDecision:
    if not gate.metadata_only or not gate.read_only:
        gate.status = ReadinessGateStatus.BLOCKED
        return ReadinessGateDecision.BLOCK

    if gate.startup_report and not gate.startup_report.startup_checks_passed:
        gate.status = ReadinessGateStatus.WARNING
        return ReadinessGateDecision.REQUEST_STARTUP_CHECK_FIX

    if gate.readiness_matrix and not gate.readiness_matrix.all_required_services_ready:
        gate.status = ReadinessGateStatus.WARNING
        return ReadinessGateDecision.REQUEST_DEPENDENCY_FIX

    if gate.gate_passed:
        gate.status = ReadinessGateStatus.PASSED_METADATA_ONLY
        return ReadinessGateDecision.PASS_TO_PHASE105_CORE_ACCEPTANCE

    gate.status = ReadinessGateStatus.WARNING
    return ReadinessGateDecision.REQUEST_MANUAL_REVIEW

def readiness_gate_requires_followup(gate: ReadinessGate) -> bool:
    return gate.decision in [
        ReadinessGateDecision.REQUEST_STARTUP_CHECK_FIX,
        ReadinessGateDecision.REQUEST_SERVICE_GRAPH_REFRESH,
        ReadinessGateDecision.REQUEST_DEPENDENCY_FIX,
        ReadinessGateDecision.REQUEST_CONFIG_FIX,
        ReadinessGateDecision.REQUEST_MANUAL_REVIEW,
        ReadinessGateDecision.BLOCK
    ]

def readiness_gate_followups(gate: ReadinessGate) -> List[str]:
    if not readiness_gate_requires_followup(gate):
        return []
    return [f"Address decision: {gate.decision.value}"]

def readiness_gate_blocks_phase105(gate: ReadinessGate) -> bool:
    return gate.decision == ReadinessGateDecision.BLOCK or not gate.gate_passed

def readiness_gate_evaluator_summary(gate: ReadinessGate) -> Dict[str, Any]:
    return {"decision": gate.decision.value}

def readiness_gate_evaluator_to_text(gate: ReadinessGate) -> str:
    return f"Evaluated Decision: {gate.decision.value}"
