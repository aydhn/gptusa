import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/exposure_limits.py ---
limits_code = """from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
from usa_signal_bot.portfolio_construction.exposure_calculator import exposure_pct_equity
from usa_signal_bot.core.enums import ExposureType, ConcentrationRiskLevel, PortfolioGuardDecision
import datetime

def exposure_limit_decision(exposure_pct: float | None, limit_pct: float | None) -> tuple[ConcentrationRiskLevel, PortfolioGuardDecision]:
    if exposure_pct is None or limit_pct is None:
        return ConcentrationRiskLevel.INSUFFICIENT_DATA, PortfolioGuardDecision.INSUFFICIENT_DATA
    if limit_pct == 0:
        return ConcentrationRiskLevel.CRITICAL, PortfolioGuardDecision.BLOCK if exposure_pct > 0 else PortfolioGuardDecision.CLEAR

    ratio = exposure_pct / limit_pct
    if ratio > 1.0:
        return ConcentrationRiskLevel.CRITICAL, PortfolioGuardDecision.BLOCK
    elif ratio > 0.9:
        return ConcentrationRiskLevel.HIGH, PortfolioGuardDecision.CAP
    elif ratio > 0.8:
        return ConcentrationRiskLevel.MODERATE, PortfolioGuardDecision.REDUCE
    return ConcentrationRiskLevel.LOW, PortfolioGuardDecision.CLEAR

def _build_assessment(snapshot: ExposureSnapshot, exp_type: ExposureType, name: str, usd: float, limit_pct: float) -> ConcentrationAssessment:
    pct = exposure_pct_equity(abs(usd), snapshot.total_equity_usd)
    r_level, dec = exposure_limit_decision(pct, limit_pct)

    warnings = []
    if r_level in [ConcentrationRiskLevel.HIGH, ConcentrationRiskLevel.CRITICAL]:
        warnings.append(f"{name} limit exceeded or high risk: {pct:.2f}% vs limit {limit_pct:.2f}%")

    return ConcentrationAssessment(
        assessment_id=create_concentration_assessment_id(name),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        exposure_type=exp_type,
        name=name,
        exposure_usd=usd,
        exposure_pct_equity=pct,
        limit_pct_equity=limit_pct,
        risk_level=r_level,
        decision=dec,
        warnings=warnings,
        errors=[],
        metadata={}
    )

def check_gross_exposure_limit(snapshot: ExposureSnapshot, max_gross_pct_equity: float) -> ConcentrationAssessment:
    return _build_assessment(snapshot, ExposureType.GROSS, "GROSS_EXPOSURE", snapshot.gross_exposure_usd, max_gross_pct_equity)

def check_net_exposure_limit(snapshot: ExposureSnapshot, max_abs_net_pct_equity: float) -> ConcentrationAssessment:
    return _build_assessment(snapshot, ExposureType.NET, "NET_EXPOSURE", snapshot.net_exposure_usd, max_abs_net_pct_equity)

def check_long_exposure_limit(snapshot: ExposureSnapshot, max_long_pct_equity: float) -> ConcentrationAssessment:
    return _build_assessment(snapshot, ExposureType.LONG, "LONG_EXPOSURE", snapshot.long_exposure_usd, max_long_pct_equity)

def check_short_exposure_limit(snapshot: ExposureSnapshot, max_short_pct_equity: float) -> ConcentrationAssessment:
    return _build_assessment(snapshot, ExposureType.SHORT, "SHORT_EXPOSURE", snapshot.short_exposure_usd, max_short_pct_equity)

def exposure_limits_summary_to_text(assessments: list[ConcentrationAssessment]) -> str:
    lines = ["Exposure Limits Summary"]
    for a in assessments:
        pct_str = f"{a.exposure_pct_equity:.2f}%" if a.exposure_pct_equity is not None else "Unknown"
        lim_str = f"{a.limit_pct_equity:.2f}%" if a.limit_pct_equity is not None else "Unknown"
        lines.append(f"  {a.name}: {pct_str} (Limit: {lim_str}) -> Risk: {a.risk_level.value if hasattr(a.risk_level, 'value') else str(a.risk_level)}, Decision: {a.decision.value if hasattr(a.decision, 'value') else str(a.decision)}")
    return "\\n".join(lines)
"""

write_file("usa_signal_bot/portfolio_construction/exposure_limits.py", limits_code)

# --- portfolio_construction/concentration_guards.py ---
guards_code = """from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
from usa_signal_bot.portfolio_construction.exposure_calculator import exposure_pct_equity
from usa_signal_bot.portfolio_construction.exposure_limits import exposure_limit_decision
from usa_signal_bot.core.enums import ExposureType, ConcentrationRiskLevel, PortfolioGuardDecision
import datetime

def _assess_dict(snapshot: ExposureSnapshot, exp_dict: dict[str, float], exp_type: ExposureType, limit_pct: float) -> list[ConcentrationAssessment]:
    res = []
    for k, v in exp_dict.items():
        pct = exposure_pct_equity(v, snapshot.total_equity_usd)
        r_level, dec = exposure_limit_decision(pct, limit_pct)
        warnings = []
        if r_level in [ConcentrationRiskLevel.HIGH, ConcentrationRiskLevel.CRITICAL]:
            warnings.append(f"{exp_type.value if hasattr(exp_type, 'value') else str(exp_type)} {k} high concentration: {pct:.2f}% vs {limit_pct:.2f}%")
        res.append(ConcentrationAssessment(
            assessment_id=create_concentration_assessment_id(k),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            exposure_type=exp_type,
            name=k,
            exposure_usd=v,
            exposure_pct_equity=pct,
            limit_pct_equity=limit_pct,
            risk_level=r_level,
            decision=dec,
            warnings=warnings,
            errors=[],
            metadata={}
        ))
    return res

def assess_symbol_concentration(snapshot: ExposureSnapshot, max_symbol_pct_equity: float = 10.0) -> list[ConcentrationAssessment]:
    return _assess_dict(snapshot, snapshot.symbol_exposures, ExposureType.SYMBOL, max_symbol_pct_equity)

def assess_strategy_concentration(snapshot: ExposureSnapshot, max_strategy_pct_equity: float = 25.0) -> list[ConcentrationAssessment]:
    return _assess_dict(snapshot, snapshot.strategy_exposures, ExposureType.STRATEGY, max_strategy_pct_equity)

def assess_sector_concentration(snapshot: ExposureSnapshot, max_sector_pct_equity: float = 30.0) -> list[ConcentrationAssessment]:
    return _assess_dict(snapshot, snapshot.sector_exposures, ExposureType.SECTOR, max_sector_pct_equity)

def assess_cluster_concentration(snapshot: ExposureSnapshot, max_cluster_pct_equity: float = 20.0) -> list[ConcentrationAssessment]:
    return _assess_dict(snapshot, snapshot.cluster_exposures, ExposureType.CLUSTER, max_cluster_pct_equity)

def assess_all_concentration(snapshot: ExposureSnapshot, config: dict | None = None) -> list[ConcentrationAssessment]:
    cfg = config or {}
    sym_lim = cfg.get("max_symbol_pct_equity", 10.0)
    str_lim = cfg.get("max_strategy_pct_equity", 25.0)
    sec_lim = cfg.get("max_sector_pct_equity", 30.0)
    clu_lim = cfg.get("max_cluster_pct_equity", 20.0)

    res = []
    res.extend(assess_symbol_concentration(snapshot, sym_lim))
    res.extend(assess_strategy_concentration(snapshot, str_lim))
    res.extend(assess_sector_concentration(snapshot, sec_lim))
    res.extend(assess_cluster_concentration(snapshot, clu_lim))
    return res

def concentration_assessments_to_text(items: list[ConcentrationAssessment]) -> str:
    lines = ["Concentration Assessments"]
    for a in items:
        pct_str = f"{a.exposure_pct_equity:.2f}%" if a.exposure_pct_equity is not None else "Unknown"
        lim_str = f"{a.limit_pct_equity:.2f}%" if a.limit_pct_equity is not None else "Unknown"
        lines.append(f"  [{a.exposure_type.value if hasattr(a.exposure_type, 'value') else str(a.exposure_type)}] {a.name}: {pct_str} (Limit: {lim_str}) -> {a.risk_level.value if hasattr(a.risk_level, 'value') else str(a.risk_level)}")
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/portfolio_construction/concentration_guards.py", guards_code)

# --- portfolio_construction/correlation_proxy.py ---
corr_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioCandidate
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/portfolio_construction/correlation_proxy.py", corr_code)

print("Generated step 2")
