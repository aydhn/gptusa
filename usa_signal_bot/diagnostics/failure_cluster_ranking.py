from typing import Any, Dict, List
from usa_signal_bot.diagnostics.diagnostic_models import FailureCluster

def rank_failure_clusters_by_loss(clusters: List[FailureCluster]) -> List[FailureCluster]:
    return sorted(clusters, key=lambda c: c.total_net_pnl_usd if c.total_net_pnl_usd is not None else 0.0) # Assumes loss is negative

def rank_failure_clusters_by_event_count(clusters: List[FailureCluster]) -> List[FailureCluster]:
    return sorted(clusters, key=lambda c: c.event_count, reverse=True)

def rank_failure_clusters_by_severity(clusters: List[FailureCluster]) -> List[FailureCluster]:
    # Custom ordering for severity
    sev_order = {"CRITICAL": 5, "HIGH": 4, "MODERATE": 3, "LOW": 2, "INFO": 1, "INSUFFICIENT_DATA": 0, "UNKNOWN": -1}
    return sorted(clusters, key=lambda c: sev_order.get(c.severity.value, -1), reverse=True)

def top_failure_clusters(clusters: List[FailureCluster], top_n: int = 10) -> List[FailureCluster]:
    ranked = rank_failure_clusters_by_loss(clusters)
    return ranked[:top_n]

def failure_cluster_ranking_summary(clusters: List[FailureCluster]) -> Dict[str, Any]:
    return {
        "total_clusters": len(clusters),
        "high_severity_clusters": len([c for c in clusters if c.severity.value in ["HIGH", "CRITICAL"]])
    }

def failure_cluster_ranking_to_text(payload: Dict[str, Any]) -> str:
    lines = [
        "Failure Cluster Ranking Summary:",
        f"  Total Clusters: {payload.get('total_clusters', 0)}",
        f"  High Severity Clusters: {payload.get('high_severity_clusters', 0)}"
    ]
    return "\n".join(lines)
