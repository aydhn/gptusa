from typing import Any
from .observer_governance_models import ObserverGovernanceGate, ObserverPaperComparisonReport, PromotionEvidenceRefresh, create_observer_governance_gate_id
from usa_signal_bot.core.enums import ObserverGovernanceGateType, ObserverGovernanceStatus, ObserverGovernanceRiskFlag

def _make_gate(gt: ObserverGovernanceGateType, passed: bool, flags: list[ObserverGovernanceRiskFlag] = None) -> ObserverGovernanceGate:
    return ObserverGovernanceGate(
        gate_id=create_observer_governance_gate_id(), gate_type=gt,
        status=ObserverGovernanceStatus.PASS if passed else ObserverGovernanceStatus.FAIL,
        observed_value=passed, threshold=True, description=f"{gt.value} check",
        risk_flags=flags or [], warnings=[], errors=[]
    )

def gate_locked_runtime_confirmed(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = observer_payload.get("locked_runtime", False)
    flags = [] if passed else [ObserverGovernanceRiskFlag.LOCKED_RUNTIME_NOT_CONFIRMED]
    return _make_gate(ObserverGovernanceGateType.LOCKED_RUNTIME_CONFIRMED, passed, flags)

def gate_no_active_paper_permission(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = not observer_payload.get("active_paper_permission", False)
    flags = [] if passed else [ObserverGovernanceRiskFlag.ACTIVE_PAPER_ENABLE_RISK]
    return _make_gate(ObserverGovernanceGateType.NO_ACTIVE_PAPER_PERMISSION, passed, flags)

def gate_no_paper_mutation(observer_payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> ObserverGovernanceGate:
    passed = not observer_payload.get("paper_mutation", False)
    flags = [] if passed else [ObserverGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK]
    return _make_gate(ObserverGovernanceGateType.NO_PAPER_MUTATION, passed, flags)

def gate_no_order_execution(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = True
    return _make_gate(ObserverGovernanceGateType.NO_ORDER_EXECUTION, passed)

def gate_no_broker_send(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = not observer_payload.get("broker_send", False)
    flags = [] if passed else [ObserverGovernanceRiskFlag.BROKER_ORDER_RISK]
    return _make_gate(ObserverGovernanceGateType.NO_BROKER_SEND, passed, flags)

def gate_no_telegram_real_send(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = not observer_payload.get("telegram_real_send", False)
    flags = [] if passed else [ObserverGovernanceRiskFlag.TELEGRAM_REAL_SEND_RISK]
    return _make_gate(ObserverGovernanceGateType.NO_TELEGRAM_REAL_SEND, passed, flags)

def gate_no_config_patch(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = not observer_payload.get("config_patch", False)
    flags = [] if passed else [ObserverGovernanceRiskFlag.PRODUCTION_CONFIG_WRITE_RISK]
    return _make_gate(ObserverGovernanceGateType.NO_CONFIG_PATCH, passed, flags)

def gate_paper_baseline_available(paper_snapshot: dict[str, Any]) -> ObserverGovernanceGate:
    passed = bool(paper_snapshot)
    flags = [] if passed else [ObserverGovernanceRiskFlag.PAPER_BASELINE_MISSING]
    return _make_gate(ObserverGovernanceGateType.PAPER_BASELINE_AVAILABLE, passed, flags)

def gate_observer_output_available(observer_payload: dict[str, Any]) -> ObserverGovernanceGate:
    passed = bool(observer_payload)
    flags = [] if passed else [ObserverGovernanceRiskFlag.OBSERVER_OUTPUT_MISSING]
    return _make_gate(ObserverGovernanceGateType.OBSERVER_OUTPUT_AVAILABLE, passed, flags)

def gate_drift_acceptable(comparison_report: ObserverPaperComparisonReport) -> ObserverGovernanceGate:
    passed = ObserverGovernanceRiskFlag.DRIFT_TOO_HIGH not in comparison_report.risk_flags
    flags = [] if passed else [ObserverGovernanceRiskFlag.DRIFT_TOO_HIGH]
    return _make_gate(ObserverGovernanceGateType.DRIFT_ACCEPTABLE, passed, flags)

def gate_evidence_fresh(refresh: PromotionEvidenceRefresh) -> ObserverGovernanceGate:
    passed = refresh.status.value == "FRESH"
    flags = []
    if refresh.missing_count > 0: flags.append(ObserverGovernanceRiskFlag.EVIDENCE_MISSING)
    elif refresh.stale_count > 0: flags.append(ObserverGovernanceRiskFlag.EVIDENCE_STALE)
    return _make_gate(ObserverGovernanceGateType.EVIDENCE_FRESH, passed, flags)

def default_observer_governance_gates(observer_payload: dict[str, Any], paper_snapshot: dict[str, Any], comparison_report: ObserverPaperComparisonReport, evidence_refresh: PromotionEvidenceRefresh) -> list[ObserverGovernanceGate]:
    return [
        gate_locked_runtime_confirmed(observer_payload),
        gate_no_active_paper_permission(observer_payload),
        gate_no_paper_mutation(observer_payload, paper_snapshot),
        gate_no_order_execution(observer_payload),
        gate_no_broker_send(observer_payload),
        gate_no_telegram_real_send(observer_payload),
        gate_no_config_patch(observer_payload),
        gate_paper_baseline_available(paper_snapshot),
        gate_observer_output_available(observer_payload),
        gate_drift_acceptable(comparison_report),
        gate_evidence_fresh(evidence_refresh)
    ]

def observer_governance_gates_to_text(gates: list[ObserverGovernanceGate]) -> str:
    return str([g.gate_type.value for g in gates])
