from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, create_failure_mode_assessment_id, create_failure_cluster_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope, FailureClusterType
from datetime import datetime, timezone

def identify_drawdown_failure_events(events: List[DiagnosticEvent], drawdown_threshold_usd: float = 100.0) -> List[DiagnosticEvent]:
    failures = []
    for e in events:
        if e.drawdown_impact_usd is not None and e.drawdown_impact_usd > drawdown_threshold_usd:
            failures.append(e)
    return failures

def drawdown_failure_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    failures = identify_drawdown_failure_events(events)
    grouped = {}
    for e in failures:
        strategy = e.strategy_name or "UNKNOWN"
        if strategy not in grouped:
            grouped[strategy] = []
        grouped[strategy].append(e)

    assessments = []
    for strategy, group in grouped.items():
        total_dd = sum(e.drawdown_impact_usd for e in group if e.drawdown_impact_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.PORTFOLIO_CONCENTRATION), # Using a proxy failure mode
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.PORTFOLIO_CONCENTRATION,
            severity=DiagnosticSeverity.HIGH if total_dd > 1000 else DiagnosticSeverity.MODERATE,
            evidence_quality=DiagnosticEvidenceQuality.STRONG if len(group) >= 5 else DiagnosticEvidenceQuality.MODERATE,
            affected_scope=DiagnosticScope.STRATEGY,
            affected_name=strategy,
            event_count=len(group),
            loss_count=len([e for e in group if e.net_pnl_usd is not None and e.net_pnl_usd < 0]),
            total_net_loss_usd=sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None),
            evidence={"drawdown_impact_usd": total_dd}
        ))
    return assessments

def drawdown_clusters_by_dimension(events: List[DiagnosticEvent], dimension: str) -> List[FailureCluster]:
    failures = identify_drawdown_failure_events(events)
    grouped = {}
    for e in failures:
        val = getattr(e, dimension, None)
        if val is None:
            val = "UNKNOWN"
        if val not in grouped:
            grouped[val] = []
        grouped[val].append(e)

    clusters = []
    for val, group in grouped.items():
        if len(group) >= 2:
            total_dd = sum(e.drawdown_impact_usd for e in group if e.drawdown_impact_usd is not None)
            clusters.append(FailureCluster(
                cluster_id=create_failure_cluster_id(str(val)),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                cluster_type=FailureClusterType.DRAWDOWN_CLUSTER,
                name=f"{dimension}: {val}",
                event_count=len(group),
                failure_modes=[FailureModeType.UNKNOWN],
                total_net_pnl_usd=sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None),
                severity=DiagnosticSeverity.HIGH if total_dd > 1000 else DiagnosticSeverity.MODERATE,
                evidence_quality=DiagnosticEvidenceQuality.MODERATE,
                representative_events=[e.event_id for e in group[:3]],
                metadata={"drawdown_impact_usd": total_dd}
            ))
    return clusters

def top_drawdown_contributors(events: List[DiagnosticEvent], top_n: int = 10) -> List[DiagnosticEvent]:
    has_dd = [e for e in events if e.drawdown_impact_usd is not None]
    has_dd.sort(key=lambda x: x.drawdown_impact_usd, reverse=True)
    return has_dd[:top_n]

def drawdown_diagnostics_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    has_dd = [e for e in events if e.drawdown_impact_usd is not None]
    return {
        "events_with_drawdown_impact": len(has_dd),
        "total_drawdown_impact": sum(e.drawdown_impact_usd for e in has_dd)
    }

def drawdown_diagnostics_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Drawdown Diagnostics Summary:",
        f"  Events with Drawdown Impact: {payload.get('events_with_drawdown_impact', 0)}",
        f"  Total Drawdown Impact (approx): {payload.get('total_drawdown_impact', 0.0):.2f}"
    ]
    return "\n".join(lines)
