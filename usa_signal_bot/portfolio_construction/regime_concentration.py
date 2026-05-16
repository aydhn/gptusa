from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
from usa_signal_bot.portfolio_construction.exposure_calculator import exposure_pct_equity
from usa_signal_bot.portfolio_construction.exposure_limits import exposure_limit_decision
from usa_signal_bot.core.enums import ExposureType, ConcentrationRiskLevel, PortfolioGuardDecision
import datetime

def assess_regime_concentration(snapshot: ExposureSnapshot, max_regime_pct_equity: float = 50.0) -> list[ConcentrationAssessment]:
    res = []
    for k, v in snapshot.regime_exposures.items():
        pct = exposure_pct_equity(v, snapshot.total_equity_usd)
        r_level, dec = exposure_limit_decision(pct, max_regime_pct_equity)

        # High transition regimes are riskier
        if k in ["TRANSITION", "HIGH_VOLATILITY", "THIN_LIQUIDITY"] and r_level == ConcentrationRiskLevel.MODERATE:
            r_level = ConcentrationRiskLevel.HIGH
            dec = PortfolioGuardDecision.CAP

        warnings = []
        if r_level in [ConcentrationRiskLevel.HIGH, ConcentrationRiskLevel.CRITICAL]:
            warnings.append(f"Regime {k} high concentration: {pct:.2f}% vs {max_regime_pct_equity:.2f}%")

        res.append(ConcentrationAssessment(
            assessment_id=create_concentration_assessment_id(k),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            exposure_type=ExposureType.REGIME,
            name=k,
            exposure_usd=v,
            exposure_pct_equity=pct,
            limit_pct_equity=max_regime_pct_equity,
            risk_level=r_level,
            decision=dec,
            warnings=warnings,
            errors=[],
            metadata={}
        ))
    return res

def regime_concentration_risk(regime_label: str | None, exposure_pct: float | None) -> ConcentrationRiskLevel:
    if regime_label is None or exposure_pct is None: return ConcentrationRiskLevel.INSUFFICIENT_DATA
    if exposure_pct > 50.0: return ConcentrationRiskLevel.HIGH
    if exposure_pct > 30.0: return ConcentrationRiskLevel.MODERATE
    return ConcentrationRiskLevel.LOW

def regime_concentration_adjustment_hint(snapshot: ExposureSnapshot) -> dict[str, any]:
    assessments = assess_regime_concentration(snapshot)
    for a in assessments:
        if a.decision in [PortfolioGuardDecision.BLOCK, PortfolioGuardDecision.CAP]:
            return {"decision": "REDUCE", "reason": f"Regime {a.name} is over-concentrated."}
    return {"decision": "CLEAR", "reason": "Regime concentration is acceptable."}

def regime_concentration_to_text(items: list[ConcentrationAssessment]) -> str:
    lines = ["Regime Concentration"]
    for a in items:
        pct_str = f"{a.exposure_pct_equity:.2f}%" if a.exposure_pct_equity is not None else "Unknown"
        lines.append(f"  {a.name}: {pct_str} -> {a.risk_level.value if hasattr(a.risk_level, 'value') else str(a.risk_level)}")
    return "\n".join(lines)
