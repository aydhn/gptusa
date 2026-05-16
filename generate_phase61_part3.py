import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/regime_concentration.py ---
regime_code = """from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
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
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/portfolio_construction/regime_concentration.py", regime_code)

# --- portfolio_construction/liquidity_cost_concentration.py ---
liqc_code = """from usa_signal_bot.portfolio_construction.portfolio_models import ExposureSnapshot, ConcentrationAssessment, create_concentration_assessment_id
from usa_signal_bot.portfolio_construction.exposure_calculator import exposure_pct_equity
from usa_signal_bot.portfolio_construction.exposure_limits import exposure_limit_decision
from usa_signal_bot.core.enums import ExposureType, ConcentrationRiskLevel, PortfolioGuardDecision
import datetime

def assess_liquidity_bucket_concentration(snapshot: ExposureSnapshot, max_thin_liquidity_pct_equity: float = 25.0) -> list[ConcentrationAssessment]:
    res = []
    for k, v in snapshot.liquidity_bucket_exposures.items():
        pct = exposure_pct_equity(v, snapshot.total_equity_usd)

        limit = 100.0
        if "THIN" in k.upper(): limit = max_thin_liquidity_pct_equity
        if "ILLIQUID" in k.upper(): limit = 5.0  # very strict

        r_level, dec = exposure_limit_decision(pct, limit)
        warnings = []
        if r_level in [ConcentrationRiskLevel.HIGH, ConcentrationRiskLevel.CRITICAL]:
            warnings.append(f"Liquidity {k} high concentration: {pct:.2f}% vs {limit:.2f}%")

        res.append(ConcentrationAssessment(
            assessment_id=create_concentration_assessment_id(k),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            exposure_type=ExposureType.LIQUIDITY_BUCKET,
            name=k,
            exposure_usd=v,
            exposure_pct_equity=pct,
            limit_pct_equity=limit,
            risk_level=r_level,
            decision=dec,
            warnings=warnings,
            errors=[],
            metadata={}
        ))
    return res

def assess_cost_bucket_concentration(snapshot: ExposureSnapshot, max_high_cost_pct_equity: float = 20.0) -> list[ConcentrationAssessment]:
    res = []
    for k, v in snapshot.cost_bucket_exposures.items():
        pct = exposure_pct_equity(v, snapshot.total_equity_usd)

        limit = 100.0
        if "HIGH" in k.upper() or "STRESSED" in k.upper(): limit = max_high_cost_pct_equity
        if "EXTREME" in k.upper(): limit = 5.0

        r_level, dec = exposure_limit_decision(pct, limit)
        warnings = []
        if r_level in [ConcentrationRiskLevel.HIGH, ConcentrationRiskLevel.CRITICAL]:
            warnings.append(f"Cost bucket {k} high concentration: {pct:.2f}% vs {limit:.2f}%")

        res.append(ConcentrationAssessment(
            assessment_id=create_concentration_assessment_id(k),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            exposure_type=ExposureType.COST_BUCKET,
            name=k,
            exposure_usd=v,
            exposure_pct_equity=pct,
            limit_pct_equity=limit,
            risk_level=r_level,
            decision=dec,
            warnings=warnings,
            errors=[],
            metadata={}
        ))
    return res

def liquidity_cost_concentration_adjustment_hint(snapshot: ExposureSnapshot) -> dict[str, any]:
    for a in assess_liquidity_bucket_concentration(snapshot):
        if a.decision in [PortfolioGuardDecision.BLOCK, PortfolioGuardDecision.CAP]:
            return {"decision": "REDUCE", "reason": f"Excessive illiquid exposure."}
    for a in assess_cost_bucket_concentration(snapshot):
        if a.decision in [PortfolioGuardDecision.BLOCK, PortfolioGuardDecision.CAP]:
            return {"decision": "REDUCE", "reason": f"Excessive high-cost exposure."}
    return {"decision": "CLEAR", "reason": "Liquidity and cost bucket concentration acceptable."}

def liquidity_cost_concentration_to_text(items: list[ConcentrationAssessment]) -> str:
    lines = ["Liquidity & Cost Concentration"]
    for a in items:
        pct_str = f"{a.exposure_pct_equity:.2f}%" if a.exposure_pct_equity is not None else "Unknown"
        lines.append(f"  [{a.exposure_type.value if hasattr(a.exposure_type, 'value') else str(a.exposure_type)}] {a.name}: {pct_str} -> {a.risk_level.value if hasattr(a.risk_level, 'value') else str(a.risk_level)}")
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/portfolio_construction/liquidity_cost_concentration.py", liqc_code)

print("Generated step 3")
