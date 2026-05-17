from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, create_failure_mode_assessment_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope
from datetime import datetime, timezone

def identify_false_positive_events(events: List[DiagnosticEvent], min_signal_score: float = 70.0, negative_pnl_required: bool = True) -> List[DiagnosticEvent]:
    fps = []
    for e in events:
        if e.signal_score is not None and e.signal_score >= min_signal_score:
            if negative_pnl_required:
                if e.net_pnl_usd is not None and e.net_pnl_usd < 0:
                    fps.append(e)
            else:
                if e.net_pnl_usd is None or e.net_pnl_usd <= 0:
                    fps.append(e)
    return fps

def false_positive_rate(events: List[DiagnosticEvent], min_signal_score: float = 70.0) -> Optional[float]:
    high_score_events = [e for e in events if e.signal_score is not None and e.signal_score >= min_signal_score]
    if not high_score_events:
        return None
    fps = identify_false_positive_events(events, min_signal_score)
    return (len(fps) / len(high_score_events)) * 100

def false_signal_assessments_by_strategy(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    fps = identify_false_positive_events(events)
    grouped = {}
    for e in fps:
        strategy = e.strategy_name or "UNKNOWN"
        if strategy not in grouped:
            grouped[strategy] = []
        grouped[strategy].append(e)

    assessments = []
    for strategy, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.LOW_SIGNAL_QUALITY),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.LOW_SIGNAL_QUALITY,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.STRATEGY,
            affected_name=strategy,
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"false_positive_count": len(group)}
        ))
    return assessments

def false_signal_assessments_by_signal_family(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    fps = identify_false_positive_events(events)
    grouped = {}
    for e in fps:
        family = e.signal_family or "UNKNOWN"
        if family not in grouped:
            grouped[family] = []
        grouped[family].append(e)

    assessments = []
    for family, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.LOW_SIGNAL_QUALITY),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.LOW_SIGNAL_QUALITY,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.SIGNAL,
            affected_name=family,
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"false_positive_count": len(group)}
        ))
    return assessments

def false_signal_quality_buckets(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    fps = identify_false_positive_events(events)
    return {
        "total_high_score_events": len([e for e in events if e.signal_score is not None and e.signal_score >= 70.0]),
        "false_positive_count": len(fps),
        "false_positive_rate_pct": false_positive_rate(events)
    }

def false_signal_analysis_to_text(events: List[DiagnosticEvent]) -> str:
    summary = false_signal_quality_buckets(events)
    rate = summary['false_positive_rate_pct']
    rate_str = f"{rate:.2f}%" if rate is not None else "N/A"
    lines = [
        "False Signal Analysis:",
        f"  High Score Events: {summary['total_high_score_events']}",
        f"  False Positives: {summary['false_positive_count']} ({rate_str})"
    ]
    return "\n".join(lines)
