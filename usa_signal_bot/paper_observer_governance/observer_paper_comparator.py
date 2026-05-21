from typing import Any
from .observer_governance_models import (
    ObserverMetricComparison, ObserverPaperComparisonReport, create_observer_metric_comparison_id,
    create_observer_paper_comparison_report_id
)
from usa_signal_bot.core.enums import ObserverMetricDirection, ObserverComparisonOutcome, ObserverGovernanceRiskFlag
from datetime import datetime, timezone

def compare_observer_metric(metric_name: str, paper_value: Any, observer_value: Any) -> ObserverMetricComparison:
    direction = ObserverMetricDirection.UNKNOWN
    if isinstance(paper_value, (int, float)) and isinstance(observer_value, (int, float)):
        direction = ObserverMetricDirection.UNCHANGED if paper_value == observer_value else (
            ObserverMetricDirection.IMPROVED if observer_value > paper_value else ObserverMetricDirection.WORSENED
        )
    return ObserverMetricComparison(
        comparison_id=create_observer_metric_comparison_id(metric_name),
        metric_name=metric_name, paper_value=paper_value, observer_value=observer_value,
        delta_value=None, delta_pct=None, direction=direction, interpretation="", warnings=[], errors=[]
    )

def compare_observer_to_paper(paper_snapshot: dict[str, Any], observer_payload: dict[str, Any]) -> ObserverPaperComparisonReport:
    metrics = []
    flags = []
    if not paper_snapshot:
        flags.append(ObserverGovernanceRiskFlag.PAPER_BASELINE_MISSING)
    if not observer_payload:
        flags.append(ObserverGovernanceRiskFlag.OBSERVER_OUTPUT_MISSING)

    return ObserverPaperComparisonReport(
        report_id=create_observer_paper_comparison_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        paper_snapshot_id=paper_snapshot.get("snapshot_id"),
        observer_session_id=None, candidate_id=observer_payload.get("candidate_id"),
        outcome=determine_observer_comparison_outcome(metrics, flags),
        metric_comparisons=metrics,
        signal_delta={}, proposal_delta={}, risk_delta={}, drift_delta={}, safety_compliance={},
        notification_comparison={}, blocked_operation_comparison={},
        risk_flags=flags, warnings=[], errors=[]
    )

def determine_observer_comparison_outcome(comparisons: list[ObserverMetricComparison], risk_flags: list[ObserverGovernanceRiskFlag]) -> ObserverComparisonOutcome:
    if ObserverGovernanceRiskFlag.PAPER_BASELINE_MISSING in risk_flags:
        return ObserverComparisonOutcome.PAPER_BASELINE_INSUFFICIENT
    if ObserverGovernanceRiskFlag.OBSERVER_OUTPUT_MISSING in risk_flags:
        return ObserverComparisonOutcome.OBSERVER_DATA_INSUFFICIENT
    if any("RISK" in str(f.value) for f in risk_flags):
        return ObserverComparisonOutcome.BLOCKED
    return ObserverComparisonOutcome.UNKNOWN

def observer_paper_comparison_summary(report: ObserverPaperComparisonReport) -> dict[str, Any]:
    return {"outcome": report.outcome.value, "risk_flags": [f.value for f in report.risk_flags]}

def observer_paper_comparator_to_text(report: ObserverPaperComparisonReport) -> str:
    return str(observer_paper_comparison_summary(report))
