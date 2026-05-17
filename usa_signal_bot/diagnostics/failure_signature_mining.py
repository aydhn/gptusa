from typing import Any, Dict, List, Optional
from usa_signal_bot.diagnostics.diagnostic_models import DiagnosticEvent, FailureCluster, create_failure_cluster_id
from usa_signal_bot.core.enums import FailureClusterType, DiagnosticSeverity, DiagnosticEvidenceQuality
from datetime import datetime, timezone

def build_failure_signature(event: DiagnosticEvent, fields: Optional[List[str]] = None) -> str:
    if fields is None:
        fields = ["strategy_name", "signal_family", "regime_label", "liquidity_bucket", "cost_bucket", "sizing_status", "sector", "cluster"]
    parts = []
    for f in fields:
        val = getattr(event, f, None)
        if val is None:
            val = "N/A"
        parts.append(f"{f}:{val}")
    return "|".join(parts)

def signature_cluster_from_events(signature: str, events: List[DiagnosticEvent]) -> FailureCluster:
    total_loss = sum(e.net_pnl_usd for e in events if e.net_pnl_usd is not None)
    return FailureCluster(
        cluster_id=create_failure_cluster_id(signature[:30]),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cluster_type=FailureClusterType.UNKNOWN,
        name=signature,
        event_count=len(events),
        failure_modes=[],
        total_net_pnl_usd=total_loss,
        severity=DiagnosticSeverity.MODERATE if len(events) >= 5 else DiagnosticSeverity.LOW,
        evidence_quality=DiagnosticEvidenceQuality.MODERATE if len(events) >= 5 else DiagnosticEvidenceQuality.NOISY,
        representative_events=[e.event_id for e in events[:3]]
    )

def mine_failure_signatures(events: List[DiagnosticEvent], min_count: int = 3) -> List[FailureCluster]:
    losing_events = [e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]
    sig_map = {}
    for e in losing_events:
        sig = build_failure_signature(e)
        if sig not in sig_map:
            sig_map[sig] = []
        sig_map[sig].append(e)

    clusters = []
    for sig, group in sig_map.items():
        if len(group) >= min_count:
            clusters.append(signature_cluster_from_events(sig, group))
    return clusters

def failure_signature_frequency(events: List[DiagnosticEvent]) -> Dict[str, int]:
    losing_events = [e for e in events if e.net_pnl_usd is not None and e.net_pnl_usd < 0]
    freq = {}
    for e in losing_events:
        sig = build_failure_signature(e)
        freq[sig] = freq.get(sig, 0) + 1
    return freq

def failure_signature_mining_to_text(clusters: List[FailureCluster], limit: int = 100) -> str:
    lines = [f"Failure Signature Clusters (Total: {len(clusters)}, Showing top {min(len(clusters), limit)}):"]
    for c in clusters[:limit]:
        lines.append(f"  [{c.name}] Events: {c.event_count} | Total Loss: {c.total_net_pnl_usd}")
    return "\n".join(lines)
