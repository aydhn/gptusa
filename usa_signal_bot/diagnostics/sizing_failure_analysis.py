from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, create_failure_mode_assessment_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope
from datetime import datetime, timezone

def identify_sizing_failure_events(events: List[DiagnosticEvent]) -> List[DiagnosticEvent]:
    failures = []
    for e in events:
        if e.metadata.get("sizing_issue") == True or e.sizing_status in ["oversized", "undersized", "budget_exhausted"]:
            failures.append(e)
    return failures

def oversizing_failure_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = [e for e in events if e.sizing_status == "oversized" and e.net_pnl_usd is not None and e.net_pnl_usd < 0]
    grouped = {}
    for e in failures:
        strategy = e.strategy_name or "UNKNOWN"
        if strategy not in grouped:
            grouped[strategy] = []
        grouped[strategy].append(e)

    assessments = []
    for strategy, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.OVER_SIZING),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.OVER_SIZING,
            severity=DiagnosticSeverity.HIGH if len(group) >= 3 else DiagnosticSeverity.MODERATE,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 3 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.STRATEGY,
            affected_name=strategy,
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"sizing_status": "oversized"}
        ))
    return assessments

def undersizing_failure_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = [e for e in events if e.sizing_status == "undersized" and e.net_pnl_usd is not None and e.net_pnl_usd > 0]
    grouped = {}
    for e in failures:
        strategy = e.strategy_name or "UNKNOWN"
        if strategy not in grouped:
            grouped[strategy] = []
        grouped[strategy].append(e)

    assessments = []
    for strategy, group in grouped.items():
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.UNDER_SIZING),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.UNDER_SIZING,
            severity=DiagnosticSeverity.INFO,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 3 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.STRATEGY,
            affected_name=strategy,
            event_count=len(group),
            loss_count=0,
            total_net_loss_usd=0.0,
            evidence={"sizing_status": "undersized", "missed_profit_opportunity": True}
        ))
    return assessments

def sizing_status_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    oversized = [e for e in events if e.sizing_status == "oversized"]
    undersized = [e for e in events if e.sizing_status == "undersized"]
    return {
        "oversized_count": len(oversized),
        "undersized_count": len(undersized)
    }

def risk_budget_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    exhausted = [e for e in events if e.sizing_status == "budget_exhausted"]
    return {
        "budget_exhausted_count": len(exhausted)
    }

def sizing_failure_analysis_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Sizing Failure Analysis:",
        f"  Oversized Events: {payload.get('oversized_count', 0)}",
        f"  Undersized Events: {payload.get('undersized_count', 0)}",
        f"  Budget Exhausted Events: {payload.get('budget_exhausted_count', 0)}"
    ]
    return "\n".join(lines)
