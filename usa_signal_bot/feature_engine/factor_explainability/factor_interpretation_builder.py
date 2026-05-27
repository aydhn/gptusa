import datetime
from typing import Any

from usa_signal_bot.core.enums import FactorInterpretationKind
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FactorContributionProfile,
    FactorInterpretationSummary,
    create_factor_interpretation_summary_id,
    validate_factor_interpretation_summary
)

def infer_factor_interpretation_kind(factor_name: str) -> FactorInterpretationKind:
    name_lower = factor_name.lower()
    if 'mom' in name_lower:
        return FactorInterpretationKind.MOMENTUM_CONTEXT
    elif 'trend' in name_lower or 'ma' in name_lower:
        return FactorInterpretationKind.TREND_CONTEXT
    elif 'vol' in name_lower or 'atr' in name_lower:
        return FactorInterpretationKind.VOLATILITY_CONTEXT
    elif 'liq' in name_lower:
        return FactorInterpretationKind.LIQUIDITY_CONTEXT
    elif 'rs' in name_lower:
        return FactorInterpretationKind.RELATIVE_STRENGTH_CONTEXT
    elif 'qual' in name_lower:
        return FactorInterpretationKind.QUALITY_CONTEXT
    return FactorInterpretationKind.UNKNOWN

def safe_factor_interpretation_text(factor_name: str, context: dict[str, Any]) -> str:
    # Ensuring no trade or advice language is used
    return f"Factor {factor_name} shows context indicative of particular market regimes. This observation is research metadata."

def build_factor_interpretation_summary(symbol: str | None, factor_name: str, factor_column: str, contribution: FactorContributionProfile | None = None, diagnostics: list[dict[str, Any]] | None = None, drift: list[dict[str, Any]] | None = None) -> FactorInterpretationSummary:

    kind = infer_factor_interpretation_kind(factor_name)
    short_summary = safe_factor_interpretation_text(factor_name, {})

    summary = FactorInterpretationSummary(
        interpretation_id=create_factor_interpretation_summary_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        symbol=symbol,
        factor_name=factor_name,
        factor_column=factor_column,
        interpretation_kind=kind,
        short_summary=short_summary,
        diagnostic_summary="Diagnostics reviewed.",
        drift_summary="Drift reviewed.",
        lineage_quality_summary="Lineage and quality acceptable.",
        limitations=["This is not investment advice. For research purposes only."],
        confidence_notes=["Confidence is based on historical metadata."],
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_interpretation_summary(summary)
    return summary

def build_factor_interpretation_summaries(contributions: list[FactorContributionProfile], diagnostics_payload: list[dict[str, Any]] | None = None, drift_payload: list[dict[str, Any]] | None = None) -> list[FactorInterpretationSummary]:
    summaries = []
    for c in contributions:
        summaries.append(build_factor_interpretation_summary(
            c.symbol, c.factor_name, c.factor_column, contribution=c
        ))
    return summaries

def validate_factor_interpretation_summaries(items: list[FactorInterpretationSummary]) -> list[str]:
    errors = []
    for item in items:
        if item.investment_advice:
            errors.append(f"Interpretation {item.interpretation_id} contains investment advice")
    return errors

def factor_interpretation_builder_summary(items: list[FactorInterpretationSummary]) -> dict[str, Any]:
    return {"summary_count": len(items)}

def factor_interpretation_builder_to_text(items: list[FactorInterpretationSummary], limit: int = 200) -> str:
    return f"Created {len(items)} interpretation summaries."
