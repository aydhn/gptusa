from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
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
    return "\n".join(lines)
