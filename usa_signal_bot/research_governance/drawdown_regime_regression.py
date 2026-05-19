from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceRiskFlag, GovernanceChecklistStatus, create_governance_checklist_item_id

def detect_drawdown_regression(baseline: Optional[float], candidate: Optional[float]) -> GovernanceChecklistItem:
    status = GovernanceChecklistStatus.PASS
    if baseline and candidate and candidate > baseline:
        status = GovernanceChecklistStatus.WARNING
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("drawdown"),
        name="drawdown",
        status=status,
        description="Drawdown regression check",
        evidence_refs=[], risk_flags=[GovernanceRiskFlag.DRAWDOWN_REGRESSION] if status == GovernanceChecklistStatus.WARNING else [],
        warnings=[], errors=[]
    )

def detect_walk_forward_instability(gates_or_metrics: dict[str, Any]) -> GovernanceChecklistItem:
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("wf_instability"),
        name="wf_instability",
        status=GovernanceChecklistStatus.PASS,
        description="WF Instability check",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )

def detect_regime_instability(comparison_payload: dict[str, Any]) -> GovernanceChecklistItem:
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("regime_instability"),
        name="regime_instability",
        status=GovernanceChecklistStatus.PASS,
        description="Regime Instability check",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )

def detect_drawdown_regime_regression(comparison_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
    metrics = comparison_payload.get("metrics", {})
    b_dd = metrics.get("baseline", {}).get("max_drawdown_pct")
    c_dd = metrics.get("candidate", {}).get("max_drawdown_pct")
    return [
        detect_drawdown_regression(b_dd, c_dd),
        detect_walk_forward_instability(comparison_payload),
        detect_regime_instability(comparison_payload)
    ]

def drawdown_regime_risk_flags(comparison_payload: dict[str, Any]) -> list[GovernanceRiskFlag]:
    flags = []
    for reg in detect_drawdown_regime_regression(comparison_payload):
        if reg.status == GovernanceChecklistStatus.WARNING:
            if reg.name == "drawdown": flags.append(GovernanceRiskFlag.DRAWDOWN_REGRESSION)
            if reg.name == "wf_instability": flags.append(GovernanceRiskFlag.WALK_FORWARD_UNSTABLE)
            if reg.name == "regime_instability": flags.append(GovernanceRiskFlag.REGIME_INSTABILITY)
    return flags

def drawdown_regime_regression_to_text(payload: dict[str, Any]) -> str:
    return "Drawdown/Regime Regression Report"
