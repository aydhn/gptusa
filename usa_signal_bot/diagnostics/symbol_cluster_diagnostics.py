from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent, FailureCluster, create_failure_cluster_id
from usa_signal_bot.core.enums import FailureClusterType, DiagnosticSeverity, DiagnosticEvidenceQuality
from datetime import datetime, timezone

def _build_clusters(events: List[DiagnosticEvent], dimension: str, cluster_type: FailureClusterType) -> List[FailureCluster]:
    losing_events = [e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]
    grouped = {}
    for e in losing_events:
        val = getattr(e, dimension, None)
        if val is None:
            val = "UNKNOWN"
        if val not in grouped:
            grouped[val] = []
        grouped[val].append(e)

    clusters = []
    for val, group in grouped.items():
        if len(group) >= 2:
            total_loss = sum(e.net_pnl_usd for e in group if e.net_pnl_usd is not None)
            clusters.append(FailureCluster(
                cluster_id=create_failure_cluster_id(str(val)),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                cluster_type=cluster_type,
                name=f"{dimension}: {val}",
                event_count=len(group),
                failure_modes=[],
                total_net_pnl_usd=total_loss,
                severity=DiagnosticSeverity.MODERATE if len(group) >= 5 else DiagnosticSeverity.LOW,
                evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(group) >= 5 else DiagnosticEvidenceQuality.NOISY,
                representative_events=[e.event_id for e in group[:3]]
            ))
    return clusters

def diagnose_symbol_failures(events: List[DiagnosticEvent]) -> List[FailureCluster]:
    return _build_clusters(events, "symbol", FailureClusterType.SYMBOL_CLUSTER)

def diagnose_sector_failures(events: List[DiagnosticEvent]) -> List[FailureCluster]:
    return _build_clusters(events, "sector", FailureClusterType.SYMBOL_CLUSTER) # Using SYMBOL_CLUSTER as proxy for sector

def diagnose_cluster_failures(events: List[DiagnosticEvent]) -> List[FailureCluster]:
    return _build_clusters(events, "cluster", FailureClusterType.SYMBOL_CLUSTER)

def repeated_symbol_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    clusters = diagnose_symbol_failures(events)
    return {"repeated_symbol_failure_clusters": len(clusters)}

def sector_cluster_failure_summary(events: List[DiagnosticEvent]) -> Dict[str, Any]:
    sec_clusters = diagnose_sector_failures(events)
    clus_clusters = diagnose_cluster_failures(events)
    return {
        "sector_failure_clusters": len(sec_clusters),
        "cluster_failure_clusters": len(clus_clusters)
    }

def symbol_cluster_diagnostics_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Symbol/Cluster Diagnostics:",
        f"  Sector Clusters: {payload.get('sector_failure_clusters', 0)}",
        f"  Cluster Clusters: {payload.get('cluster_failure_clusters', 0)}"
    ]
    return "\n".join(lines)
