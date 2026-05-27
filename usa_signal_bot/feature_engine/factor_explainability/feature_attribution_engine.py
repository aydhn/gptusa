import datetime
import pandas as pd
from typing import Any

from usa_signal_bot.core.enums import FeatureAttributionMethod, AttributionDirection
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FeatureAttributionSpec,
    FeatureAttributionResult,
    create_feature_attribution_result_id,
    validate_feature_attribution_result
)

def compute_feature_attribution_score(df: pd.DataFrame, factor_column: str, feature_column: str, method: FeatureAttributionMethod) -> float:
    # Dummy deterministic logic to compute attribution score
    # e.g., correlation proxy mapping
    if factor_column not in df.columns or feature_column not in df.columns:
        return 0.0

    try:
        corr = df[factor_column].corr(df[feature_column])
        if pd.isna(corr):
            corr = 0.0
    except Exception:
        corr = 0.0

    return abs(corr * 100.0)

def attribution_direction_from_score(score: float, feature_mean: float | None = None) -> AttributionDirection:
    # Deterministic mapping
    if score > 50:
        return AttributionDirection.POSITIVE_CONTEXT
    elif score < -50:
        return AttributionDirection.NEGATIVE_CONTEXT
    elif score != 0:
        return AttributionDirection.MIXED_CONTEXT
    return AttributionDirection.NEUTRAL_CONTEXT

def normalize_attribution_scores(results: list[FeatureAttributionResult]) -> list[FeatureAttributionResult]:
    total_score = sum(r.attribution_score for r in results)
    if total_score > 0:
        for r in results:
            r.normalized_attribution_score = r.attribution_score / total_score
    else:
        for r in results:
            r.normalized_attribution_score = 0.0
    return results

def build_feature_attributions_for_symbol(symbol: str, df: pd.DataFrame, specs: list[FeatureAttributionSpec]) -> list[FeatureAttributionResult]:
    results = []
    for spec in specs:
        for feature_col in spec.input_feature_columns:
            score = compute_feature_attribution_score(df, spec.factor_column, feature_col, spec.attribution_method)
            direction = attribution_direction_from_score(score)

            res = FeatureAttributionResult(
                attribution_id=create_feature_attribution_result_id(),
                created_at_utc=datetime.datetime.utcnow().isoformat(),
                symbol=symbol,
                factor_name=spec.factor_name,
                factor_column=spec.factor_column,
                feature_column=feature_col,
                attribution_score=score,
                normalized_attribution_score=0.0, # will be set in normalization
                attribution_direction=direction,
                method=spec.attribution_method,
                coverage_ratio=None,
                quality_score=None,
                confidence_score=None,
                lineage_score=None,
                explanation_text=f"Heuristic attribution calculated for {feature_col} relative to {spec.factor_column}.",
                research_metadata_only=True,
                produces_trade_signal=False,
                produces_order_decision=False,
                produces_portfolio_weights=False,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
            validate_feature_attribution_result(res)
            results.append(res)

    if specs and specs[0].normalize_attributions:
        results = normalize_attribution_scores(results)

    return results

def validate_feature_attribution_results(results: list[FeatureAttributionResult]) -> list[str]:
    errors = []
    for r in results:
        if r.produces_trade_signal:
            errors.append(f"Result {r.attribution_id} produces trade signal")
        if r.errors:
            errors.extend(r.errors)
    return errors

def feature_attribution_engine_summary(results: list[FeatureAttributionResult]) -> dict[str, Any]:
    return {"result_count": len(results)}

def feature_attribution_engine_to_text(results: list[FeatureAttributionResult], limit: int = 200) -> str:
    return f"Computed {len(results)} attribution results."
