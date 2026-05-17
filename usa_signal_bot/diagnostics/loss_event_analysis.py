from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, create_failure_mode_assessment_id, create_failure_cluster_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope, FailureClusterType
from datetime import datetime, timezone

def filter_losing_events(events: List[DiagnosticEvent]) -> List[DiagnosticEvent]:
    return [e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]

def loss_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    losing_events = filter_losing_events(events)
    total_loss = sum(e.net_pnl_usd for e in losing_events if e.net_pnl_usd is not None)
    total_cost = sum(e.total_cost_usd for e in losing_events if e.total_cost_usd is not None)
    return {
        "total_events": len(events),
        "loss_events": len(losing_events),
        "total_net_loss_usd": total_loss,
        "total_cost_usd": total_cost,
        "loss_rate_pct": (len(losing_events) / len(events) * 100) if events else 0.0
    }

def classify_loss_severity(event: DiagnosticEvent) -> DiagnosticSeverity:
    if event.net_pnl_usd is None or event.net_pnl_usd >= 0:
        return DiagnosticSeverity.INFO
    loss = abs(event.net_pnl_usd)
    # Using hardcoded thresholds as a fallback if not injected from config
    if loss < 50:
        return DiagnosticSeverity.LOW
    elif loss < 500:
        return DiagnosticSeverity.MODERATE
    elif loss < 2000:
        return DiagnosticSeverity.HIGH
    else:
        return DiagnosticSeverity.CRITICAL

def loss_assessments_by_dimension(events: List[DiagnosticEvent], dimension: str) -> List[FailureModeAssessment]:
    losing_events = filter_losing_events(events)
    grouped = {}
    for e in losing_events:
        val = getattr(e, dimension, None)
        if val is None:
            val = "UNKNOWN"
        if val not in grouped:
            grouped[val] = []
        grouped[val].append(e)

    assessments = []
    for val, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.UNKNOWN),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.UNKNOWN,
            severity=DiagnosticSeverity.MODERATE if abs(total_loss) > 500 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 3 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.UNKNOWN,
            affected_name=str(val),
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"dimension": dimension, "value": val}
        ))
    return assessments

def detect_repeated_loss_patterns(events: List[DiagnosticEvent]) -> List[FailureCluster]:
    losing_events = filter_losing_events(events)
    # Basic clustering by symbol and strategy
    clusters_map = {}
    for e in losing_events:
        if e.symbol and e.strategy_name:
            key = f"{e.symbol}_{e.strategy_name}"
            if key not in clusters_map:
                clusters_map[key] = []
            clusters_map[key].append(e)

    clusters = []
    for key, group in clusters_map.items():
        if len(group) >= 3:
            total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
            clusters.append(FailureCluster(
                cluster_id=create_failure_cluster_id(key),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                cluster_type=FailureClusterType.SYMBOL_CLUSTER,
                name=key,
                event_count=len(group),
                failure_modes=[],
                total_net_pnl_usd=total_loss,
                severity=DiagnosticSeverity.HIGH if abs(total_loss) > 2000 else DiagnosticSeverity.MODERATE,
                evidence_quality=DiagnosticEvidenceQuality.STRONG if len(group) >= 5 else DiagnosticEvidenceQuality.MODERATE,
                representative_events=[e.event_id for e in group[:3]]
            ))
    return clusters

def loss_event_analysis_to_text(events: List[DiagnosticEvent], limit: int = 100) -> str:
    summary = loss_summary(events)
    lines = [
        "Loss Event Analysis:",
        f"  Total Events: {summary['total_events']}",
        f"  Loss Events: {summary['loss_events']} ({summary['loss_rate_pct']:.2f}%)",
        f"  Total Net Loss: {summary['total_net_loss_usd']:.2f} USD"
    ]
    return "\n".join(lines)
