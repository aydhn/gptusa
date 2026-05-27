from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringSpec,
    FactorScoreKind,
    FactorNormalizationMethod,
    create_factor_scoring_spec_id
)

def _build_spec(name: str, score_kind: FactorScoreKind, inputs: list[str]) -> FactorScoringSpec:
    return FactorScoringSpec(
        spec_id=create_factor_scoring_spec_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        factor_name=name,
        score_kind=score_kind,
        input_feature_columns=inputs,
        output_raw_column=f"{name}_raw",
        output_normalized_column=f"{name}_zscore",
        output_percentile_column=f"{name}_percentile",
        output_rank_column=f"{name}_rank",
        component_weights={},
        normalization_method=FactorNormalizationMethod.Z_SCORE,
        min_required_rows=30,
        min_required_symbols=1,
        local_pandas_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_factor_scoring_specs(factor_candidates: list[dict[str, Any]] | None = None) -> list[FactorScoringSpec]:
    specs = [
        _build_spec("momentum_research_factor", FactorScoreKind.MOMENTUM_SCORE, []),
        _build_spec("trend_research_factor", FactorScoreKind.TREND_SCORE, []),
        _build_spec("volatility_research_factor", FactorScoreKind.VOLATILITY_SCORE, []),
        _build_spec("liquidity_research_factor", FactorScoreKind.LIQUIDITY_SCORE, []),
        _build_spec("relative_strength_research_factor", FactorScoreKind.RELATIVE_STRENGTH_SCORE, []),
        _build_spec("quality_context_research_factor", FactorScoreKind.QUALITY_CONTEXT_SCORE, []),
        _build_spec("event_context_research_factor", FactorScoreKind.EVENT_CONTEXT_SCORE, []),
        _build_spec("calendar_context_research_factor", FactorScoreKind.CALENDAR_CONTEXT_SCORE, []),
        _build_spec("data_confidence_research_factor", FactorScoreKind.DATA_CONFIDENCE_SCORE, []),
        _build_spec("composite_research_factor", FactorScoreKind.COMPOSITE_RESEARCH_SCORE, [])
    ]
    return specs

def factor_scoring_spec_by_name(name: str, specs: list[FactorScoringSpec] | None = None) -> FactorScoringSpec | None:
    if specs is None:
        specs = build_factor_scoring_specs()
    for s in specs:
        if s.factor_name == name:
            return s
    return None

def default_factor_scoring_spec_names() -> list[str]:
    return [s.factor_name for s in build_factor_scoring_specs()]

def validate_factor_scoring_specs(specs: list[FactorScoringSpec]) -> list[str]:
    errors = []
    for s in specs:
        if s.produces_trade_signal:
            errors.append(f"Spec {s.factor_name} produces trade signal")
        if s.produces_order_decision:
            errors.append(f"Spec {s.factor_name} produces order decision")
        if s.produces_portfolio_weights:
            errors.append(f"Spec {s.factor_name} produces portfolio weights")
    return errors

def factor_scoring_registry_summary(specs: list[FactorScoringSpec]) -> dict[str, Any]:
    return {
        "spec_count": len(specs),
        "names": [s.factor_name for s in specs]
    }

def factor_scoring_registry_to_text(specs: list[FactorScoringSpec], limit: int = 200) -> str:
    summary = factor_scoring_registry_summary(specs)
    return f"Registry contains {summary['spec_count']} specs."
