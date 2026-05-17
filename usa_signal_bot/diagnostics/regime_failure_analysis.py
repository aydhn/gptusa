from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, create_failure_mode_assessment_id, create_failure_cluster_id
)
from usa_signal_bot.core.enums import FailureModeType, DiagnosticSeverity, DiagnosticEvidenceQuality, DiagnosticScope, FailureClusterType
from datetime import datetime, timezone

def identify_regime_mismatch_events(events: List[DiagnosticEvent]) -> List[DiagnosticEvent]:
    mismatches = []
    for e in events:
        if e.net_pnl_usd is not None and e.net_pnl_usd < 0:
            # Heuristic: large loss in a specified regime, or explicitly tagged
            mismatches.append(e)
    return mismatches

def regime_failure_assessments(events: List[DiagnosticEvent]) -> List[FailureModeAssessment]:
    mismatches = identify_regime_mismatch_events(events)
    grouped = {}
    for e in mismatches:
        regime = e.regime_label or "unknown_regime"
        if regime not in grouped:
            grouped[regime] = []
        grouped[regime].append(e)

    assessments = []
    for regime, group in grouped.items():
        total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
        assessments.append(FailureModeAssessment(
            assessment_id=create_failure_mode_assessment_id(FailureModeType.REGIME_MISMATCH),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            failure_mode=FailureModeType.REGIME_MISMATCH,
            severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
            evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
            affected_scope=DiagnosticScope.REGIME,
            affected_name=regime,
            event_count=len(group),
            loss_count=len(group),
            total_net_loss_usd=total_loss,
            evidence={"regime": regime}
        ))
    return assessments

def failure_by_regime_label(events: List[DiagnosticEvent]) -> List[FailureCluster]:
    mismatches = identify_regime_mismatch_events(events)
    grouped = {}
    for e in mismatches:
        regime = e.regime_label or "unknown_regime"
        if regime not in grouped:
            grouped[regime] = []
        grouped[regime].append(e)

    clusters = []
    for regime, group in grouped.items():
        if len(group) >= 3:
            total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
            clusters.append(FailureCluster(
                cluster_id=create_failure_cluster_id(regime),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                cluster_type=FailureClusterType.REGIME_CLUSTER,
                name=regime,
                event_count=len(group),
                failure_modes=[FailureModeType.REGIME_MISMATCH],
                total_net_pnl_usd=total_loss,
                severity=DiagnosticSeverity.MODERATE,
                evidence_quality=DiagnosticEvidenceQuality.MODERATE,
                representative_events=[e.event_id for e in group[:3]]
            ))
    return clusters

def strategy_regime_failure_matrix(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    matrix = {}
    mismatches = identify_regime_mismatch_events(events)
    for e in mismatches:
        strategy = e.strategy_name or "UNKNOWN"
        regime = e.regime_label or "unknown_regime"
        if strategy not in matrix:
            matrix[strategy] = {}
        if regime not in matrix[strategy]:
            matrix[strategy][regime] = 0
        matrix[strategy][regime] += 1
    return matrix

def transition_risk_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    # Placeholder for logic extracting transition metadata
    transitions = [e for e in events if e.metadata.get("transition_risk") == "high" and e.net_pnl_usd is not None and e.net_pnl_usd < 0]
    return {
        "high_transition_risk_losses": len(transitions)
    }

def regime_failure_analysis_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Regime Failure Analysis:",
        f"  Total Regime Failure Clusters: {payload.get('cluster_count', 0)}"
    ]
    return "\n".join(lines)
