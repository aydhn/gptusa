from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import GovernanceChecklistItem, GovernanceRiskFlag, GovernanceChecklistStatus, create_governance_checklist_item_id

def detect_metric_regression(metric_name: str, baseline_value: Optional[float], candidate_value: Optional[float], higher_is_better: bool) -> GovernanceChecklistItem:
    status = GovernanceChecklistStatus.PASS
    if baseline_value is not None and candidate_value is not None:
        if higher_is_better and candidate_value < baseline_value:
            status = GovernanceChecklistStatus.WARNING
        elif not higher_is_better and candidate_value > baseline_value:
            status = GovernanceChecklistStatus.WARNING
    elif baseline_value is None or candidate_value is None:
        status = GovernanceChecklistStatus.INSUFFICIENT_DATA

    return GovernanceChecklistItem(
        checklist_id=create_governance_checklist_item_id(metric_name),
        name=metric_name,
        status=status,
        description=f"Regression check for {metric_name}",
        evidence_refs=[],
        risk_flags=[], warnings=[], errors=[]
    )

def detect_risk_regression(comparison_payload: dict[str, Any]) -> list[GovernanceChecklistItem]:
    metrics = comparison_payload.get("metrics", {})
    b_max = metrics.get("baseline", {}).get("max_drawdown_pct")
    c_max = metrics.get("candidate", {}).get("max_drawdown_pct")
    return [detect_metric_regression("max_drawdown_pct", b_max, c_max, False)]

def risk_regression_flags(comparison_payload: dict[str, Any]) -> list[GovernanceRiskFlag]:
    flags = []
    regressions = detect_risk_regression(comparison_payload)
    for reg in regressions:
        if reg.status == GovernanceChecklistStatus.WARNING:
            flags.append(GovernanceRiskFlag.DRAWDOWN_REGRESSION)
    return flags

def risk_regression_summary(comparison_payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "ok"}

def risk_regression_to_text(payload: dict[str, Any]) -> str:
    return "Risk Regression Report"
