from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate
from usa_signal_bot.core.enums import CorrelationProxyBucket, ConcentrationRiskLevel

def estimate_pairwise_correlation_proxy(symbol_a: str, symbol_b: str, metadata_a: dict | None = None, metadata_b: dict | None = None) -> CorrelationProxyBucket:
    if symbol_a == symbol_b:
        return CorrelationProxyBucket.VERY_HIGH
    meta_a = metadata_a or {}
    meta_b = metadata_b or {}
    clus_a = meta_a.get("cluster")
    clus_b = meta_b.get("cluster")
    sec_a = meta_a.get("sector")
    sec_b = meta_b.get("sector")

    if clus_a and clus_b and clus_a != "unknown_cluster" and clus_a == clus_b:
        return CorrelationProxyBucket.HIGH
    if sec_a and sec_b and sec_a != "unknown_sector" and sec_a == sec_b:
        return CorrelationProxyBucket.MODERATE

    if not sec_a or not sec_b or sec_a == "unknown_sector" or sec_b == "unknown_sector":
        return CorrelationProxyBucket.INSUFFICIENT_DATA

    return CorrelationProxyBucket.LOW

def estimate_portfolio_correlation_proxy(candidates: list[PortfolioCandidate]) -> dict[str, any]:
    if not candidates: return {"summary": "No candidates"}
    buckets = {b.value if hasattr(b, 'value') else str(b): 0 for b in CorrelationProxyBucket}
    pairs = 0
    for i, c1 in enumerate(candidates):
        meta1 = {"cluster": c1.cluster, "sector": c1.sector}
        for c2 in candidates[i+1:]:
            meta2 = {"cluster": c2.cluster, "sector": c2.sector}
            b = estimate_pairwise_correlation_proxy(c1.symbol, c2.symbol, meta1, meta2)
            buckets[b.value if hasattr(b, 'value') else str(b)] += 1
            pairs += 1
    return {
        "total_pairs": pairs,
        "buckets": buckets
    }

def correlation_proxy_risk_level(bucket: CorrelationProxyBucket) -> ConcentrationRiskLevel:
    m = {
        CorrelationProxyBucket.VERY_HIGH: ConcentrationRiskLevel.CRITICAL,
        CorrelationProxyBucket.HIGH: ConcentrationRiskLevel.HIGH,
        CorrelationProxyBucket.MODERATE: ConcentrationRiskLevel.MODERATE,
        CorrelationProxyBucket.LOW: ConcentrationRiskLevel.LOW,
        CorrelationProxyBucket.INSUFFICIENT_DATA: ConcentrationRiskLevel.INSUFFICIENT_DATA
    }
    return m.get(bucket, ConcentrationRiskLevel.UNKNOWN)

def correlation_proxy_adjustment_hint(candidates: list[PortfolioCandidate]) -> dict[str, any]:
    summary = estimate_portfolio_correlation_proxy(candidates)
    high_corr = summary.get("buckets", {}).get("HIGH", 0) + summary.get("buckets", {}).get("VERY_HIGH", 0)
    total = summary.get("total_pairs", 1)
    ratio = high_corr / total if total > 0 else 0

    if ratio > 0.5:
        return {"decision": "REDUCE", "reason": "Portfolio is highly correlated based on proxy."}
    elif ratio > 0.3:
        return {"decision": "WARNING", "reason": "Portfolio shows moderate correlation clustering."}
    return {"decision": "CLEAR", "reason": "Correlation proxy is within acceptable limits."}

def correlation_proxy_summary_to_text(summary: dict[str, any]) -> str:
    lines = ["Correlation Proxy Summary"]
    lines.append(f"  Total Pairs: {summary.get('total_pairs', 0)}")
    for k, v in summary.get('buckets', {}).items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    lines.append("Note: Correlation proxy is based on sector/cluster heuristics, not statistical correlation.")
    return "\n".join(lines)
