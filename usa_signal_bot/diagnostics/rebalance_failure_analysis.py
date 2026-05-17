from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, create_failure_mode_assessment_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope
from datetime import datetime, timezone

def identify_rebalance_related_failures(events: List[DiagnosticEvent]) -> List[DiagnosticEvent]:
    failures = []
    for e in events:
        if e.rebalance_action_type in ["REDUCE", "EXIT", "INCREASE"]:
            if e.net_pnl_usd is not None and e.net_pnl_usd < 0:
                failures.append(e)
    return failures

def rebalance_turnover_drag_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = identify_rebalance_related_failures(events)
    grouped = {}
    for e in failures:
        action = e.rebalance_action_type or "UNKNOWN"
        if action not in grouped:
            grouped[action] = []
        grouped[action].append(e)

    assessments = []
    for action, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        total_cost = sum(e.total_cost_usd for e in group if e.total_cost_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.REBALANCE_TURNOVER_DRAG),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.REBALANCE_TURNOVER_DRAG,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.PORTFOLIO,
            affected_name=f"Rebalance Action: {action}",
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            total_cost_drag_usd=total_cost,
            evidence={"action_type": action}
        ))
    return assessments

def signal_decay_rebalance_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = [e for e in identify_rebalance_related_failures(events) if e.metadata.get("signal_decay") == True]
    if not failures:
        return []
    total_loss = sum(e.net_pnl_usd for e in failures if e.net_pnl_usd is not None)
    return [FailureModeAssessment(
        assessment_id=create_failure_mode_assessment_id(FailureModeType.SIGNAL_DECAY),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        failure_mode=FailureModeType.SIGNAL_DECAY,
        severity=DiagnosticSeverity.MODERATE if len(failures) >= 3 else DiagnosticSeverity.LOW,
        evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(failures) >= 3 else DiagnosticEvidenceQuality.NOISY,
        affected_scope=DiagnosticScope.SIGNAL,
        affected_name="DECAYED_SIGNALS",
        event_count=len(failures),
        loss_count=len(failures),
        total_net_loss_usd=total_loss,
        evidence={"decayed_count": len(failures)}
    )]

def rebalance_action_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    failures = identify_rebalance_related_failures(events)
    counts = {"INCREASE": 0, "REDUCE": 0, "EXIT": 0, "UNKNOWN": 0}
    for e in failures:
        action = e.rebalance_action_type or "UNKNOWN"
        if action in counts:
            counts[action] += 1
        else:
            counts["UNKNOWN"] += 1
    return counts

def turnover_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    failures = identify_rebalance_related_failures(events)
    return {
        "rebalance_failure_count": len(failures),
        "total_turnover_loss": sum(e.net_pnl_usd for e in failures if e.net_pnl_usd is not None)
    }

def rebalance_failure_analysis_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Rebalance Failure Analysis:",
        f"  INCREASE Failures: {payload.get('INCREASE', 0)}",
        f"  REDUCE Failures: {payload.get('REDUCE', 0)}",
        f"  EXIT Failures: {payload.get('EXIT', 0)}"
    ]
    return "\n".join(lines)
