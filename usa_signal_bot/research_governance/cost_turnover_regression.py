from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceRiskFlag, GovernanceChecklistStatus, create_governance_checklist_item_id

def detect_cost_drag_regression(baseline: Optional[float], candidate: Optional[float]) -> GovernanceChecklistItem:
    status = GovernanceChecklistStatus.PASS
    if baseline and candidate and candidate > baseline:
        status = GovernanceChecklistStatus.WARNING
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("cost_drag"),
        name="cost_drag",
        status=status,
        description="Check cost drag regression",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )

def detect_turnover_regression(baseline: Optional[float], candidate: Optional[float]) -> GovernanceChecklistItem:
    status = GovernanceChecklistStatus.PASS
    if baseline and candidate and candidate > baseline:
        status = GovernanceChecklistStatus.WARNING
    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id("turnover"),
        name="turnover",
        status=status,
        description="Check turnover regression",
        evidence_refs=[], risk_flags=[], warnings=[], errors=[]
    )

def detect_cost_turnover_regression(comparison_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
    metrics = comparison_payload.get("metrics", {})
    b_cost = metrics.get("baseline", {}).get("cost_drag")
    c_cost = metrics.get("candidate", {}).get("cost_drag")
    b_turn = metrics.get("baseline", {}).get("turnover")
    c_turn = metrics.get("candidate", {}).get("turnover")

    return [
        detect_cost_drag_regression(b_cost, c_cost),
        detect_turnover_regression(b_turn, c_turn)
    ]

def cost_turnover_risk_flags(comparison_payload: dict[str, Any]) -> list[GovernanceRiskFlag]:
    flags = []
    for reg in detect_cost_turnover_regression(comparison_payload):
        if reg.status == GovernanceChecklistStatus.WARNING:
            if reg.name == "cost_drag": flags.append(GovernanceRiskFlag.COST_REGRESSION)
            if reg.name == "turnover": flags.append(GovernanceRiskFlag.TURNOVER_REGRESSION)
    return flags

def cost_turnover_regression_summary(comparison_payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def cost_turnover_regression_to_text(payload: dict[str, Any]) -> str:
    return "Cost Turnover Report"
