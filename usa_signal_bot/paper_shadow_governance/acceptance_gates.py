from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus, ShadowGovernanceRiskFlag
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id
from usa_signal_bot.paper_shadow_governance.ledger_completeness import ledger_completeness_gate
from usa_signal_bot.paper_shadow_governance.notification_review import notification_safety_gate
from usa_signal_bot.paper_shadow_governance.pnl_cost_comparator import compare_shadow_cost_regression, compare_shadow_pnl_regression

def build_no_real_order_risk_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "REAL_ORDER_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.REAL_ORDER_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_REAL_ORDER_RISK),
        gate_type=ShadowAcceptanceGateType.NO_REAL_ORDER_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for real order risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_no_paper_mutation_risk_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "PAPER_MUTATION_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_PAPER_MUTATION_RISK),
        gate_type=ShadowAcceptanceGateType.NO_PAPER_MUTATION_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for paper state mutation risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_no_telegram_real_send_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "TELEGRAM_REAL_SEND_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.TELEGRAM_REAL_SEND_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_TELEGRAM_REAL_SEND_RISK),
        gate_type=ShadowAcceptanceGateType.NO_TELEGRAM_REAL_SEND_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for telegram real send risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_no_production_config_write_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    flags = candidate_payload.get("safety_flags", [])
    status = ShadowAcceptanceStatus.BLOCKED if "PRODUCTION_CONFIG_WRITE_RISK" in flags else ShadowAcceptanceStatus.PASS
    risk = [ShadowGovernanceRiskFlag.PRODUCTION_CONFIG_WRITE_RISK] if status == ShadowAcceptanceStatus.BLOCKED else []
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NO_PRODUCTION_CONFIG_WRITE_RISK),
        gate_type=ShadowAcceptanceGateType.NO_PRODUCTION_CONFIG_WRITE_RISK,
        status=status,
        threshold=0, observed_value=len(risk),
        description="Check for production config write risk",
        risk_flags=risk, warnings=[], errors=[]
    )

def build_ledger_complete_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return ledger_completeness_gate(candidate_payload)

def build_cost_not_worse_gate(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return compare_shadow_cost_regression(baseline_payload.get("metrics", {}), candidate_payload.get("metrics", {}))

def build_pnl_not_worse_gate(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return compare_shadow_pnl_regression(baseline_payload.get("metrics", {}), candidate_payload.get("metrics", {}))

def build_risk_not_worse_gate(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.RISK_NOT_WORSE),
        gate_type=ShadowAcceptanceGateType.RISK_NOT_WORSE,
        status=ShadowAcceptanceStatus.PASS,
        threshold=0, observed_value=0, description="Check risk metrics",
        risk_flags=[], warnings=[], errors=[]
    )

def build_notification_safe_gate(candidate_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    return notification_safety_gate(candidate_payload)

def default_shadow_acceptance_gates(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> List[ShadowAcceptanceGate]:
    return [
        build_no_real_order_risk_gate(candidate_payload),
        build_no_paper_mutation_risk_gate(candidate_payload),
        build_no_telegram_real_send_gate(candidate_payload),
        build_no_production_config_write_gate(candidate_payload),
        build_ledger_complete_gate(candidate_payload),
        build_cost_not_worse_gate(baseline_payload, candidate_payload),
        build_pnl_not_worse_gate(baseline_payload, candidate_payload),
        build_risk_not_worse_gate(baseline_payload, candidate_payload),
        build_notification_safe_gate(candidate_payload)
    ]

def shadow_acceptance_gates_to_text(gates: List[ShadowAcceptanceGate]) -> str:
    return f"Evaluated {len(gates)} gates."
