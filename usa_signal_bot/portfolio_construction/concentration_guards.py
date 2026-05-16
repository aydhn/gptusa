from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
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
    return "\n".join(lines)
