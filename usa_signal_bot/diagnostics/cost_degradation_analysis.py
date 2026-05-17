from typing import Any, Dict, List, Optional
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, create_failure_mode_assessment_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope
from datetime import datetime, timezone

def cost_drag_pct_for_event(event: DiagnosticEvent) -> Optional[float]:
    if event.total_cost_usd is None or event.gross_pnl_usd is None:
        return None
    if event.gross_pnl_usd <= 0:
        return None # If gross is negative, it's not purely a cost degradation
    return (event.total_cost_usd / event.gross_pnl_usd) * 100

def identify_cost_degraded_events(events: List[DiagnosticEvent], cost_drag_threshold_pct: float = 50.0) -> List[DiagnosticEvent]:
    degraded = []
    for e in events:
        drag = cost_drag_pct_for_event(e)
        if drag is not None and drag >= cost_drag_threshold_pct:
            degraded.append(e)
    return degraded

def cost_degradation_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    degraded = identify_cost_degraded_events(events)
    if not degraded:
        return []
    total_cost = sum(e.total_cost_usd for e in degraded if e.total_cost_usd is not None)
    return [FailureModeAssessment(
        assessment_id=create_failure_mode_assessment_id(FailureModeType.COST_DRAG_ERASED_EDGE),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        failure_mode=FailureModeType.COST_DRAG_ERASED_EDGE,
        severity=DiagnosticSeverity.HIGH if len(degraded) >= 10 else DiagnosticSeverity.MODERATE,
        evidence_quality=DiagnosticEvidenceQuality.STRONG if len(degraded) >= 10 else DiagnosticEvidenceQuality.MODERATE,
        affected_scope=DiagnosticScope.PORTFOLIO,
        affected_name="OVERALL",
        event_count=len(degraded),
        loss_count=len([e for e in degraded if e.net_pnl_usd is not None and e.net_pnl_usd < 0]),
        total_cost_drag_usd=total_cost,
        evidence={"degraded_event_count": len(degraded)}
    )]

def cost_degradation_by_strategy(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    degraded = identify_cost_degraded_events(events)
    grouped = {}
    for e in degraded:
        strategy = e.strategy_name or "UNKNOWN"
        if strategy not in grouped:
            grouped[strategy] = []
        grouped[strategy].append(e)

    assessments = []
    for strategy, group in grouped.items():
        total_cost = sum(e.total_cost_usd for e in group if e.total_cost_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.COST_DRAG_ERASED_EDGE),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.COST_DRAG_ERASED_EDGE,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.STRATEGY,
            affected_name=strategy,
            event_count=len(group),
            loss_count=len([e for e in group if e.net_pnl_usd is not None and e.net_pnl_usd < 0]),
            total_cost_drag_usd=total_cost,
            evidence={"degraded_event_count": len(group)}
        ))
    return assessments

def cost_degradation_by_liquidity_bucket(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    degraded = identify_cost_degraded_events(events)
    grouped = {}
    for e in degraded:
        bucket = e.liquidity_bucket or "UNKNOWN"
        if bucket not in grouped:
            grouped[bucket] = []
        grouped[bucket].append(e)

    assessments = []
    for bucket, group in grouped.items():
        total_cost = sum(e.total_cost_usd for e in group if e.total_cost_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.HIGH_SLIPPAGE),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.HIGH_SLIPPAGE,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.CLUSTER, # Assuming liquidity bucket acts like a cluster
            affected_name=f"Liquidity: {bucket}",
            event_count=len(group),
            loss_count=len([e for e in group if e.net_pnl_usd is not None and e.net_pnl_usd < 0]),
            total_cost_drag_usd=total_cost,
            evidence={"degraded_event_count": len(group)}
        ))
    return assessments

def cost_degradation_analysis_to_text(events: List[DiagnosticEvent]) -> str:
    degraded = identify_cost_degraded_events(events)
    lines = [
        "Cost Degradation Analysis:",
        f"  Total Degraded Events: {len(degraded)}"
    ]
    return "\n".join(lines)
