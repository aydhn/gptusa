from typing import Any
import pandas as pd
from usa_signal_bot.core.enums import FeatureSelectionStatus, FeatureSelectionReason
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    FeatureCoverageProfile,
    FeatureStabilityProfile,
    FeatureRedundancyProfile,
    FeatureSelectionMetadata,
    create_feature_selection_metadata_id,
    validate_feature_selection_metadata,
    _now_str
)
from usa_signal_bot.feature_engine.factor_composition.feature_missingness_analyzer import feature_missingness_by_column

def determine_feature_selection_status(coverage_ratio: float, missingness_ratio: float, stability_score: float, redundancy_score: float, unsafe: bool = False) -> FeatureSelectionStatus:
    if unsafe:
        return FeatureSelectionStatus.EXCLUDED_UNSAFE
    if coverage_ratio < 0.70:
        return FeatureSelectionStatus.EXCLUDED_LOW_COVERAGE
    if missingness_ratio > 0.30:
        return FeatureSelectionStatus.EXCLUDED_HIGH_MISSINGNESS
    if stability_score < 40.0:
        return FeatureSelectionStatus.EXCLUDED_LOW_STABILITY
    if redundancy_score > 80.0:
        return FeatureSelectionStatus.EXCLUDED_HIGH_REDUNDANCY

    return FeatureSelectionStatus.SELECTED_FOR_RESEARCH

def determine_feature_selection_reasons(coverage_ratio: float, missingness_ratio: float, stability_score: float, redundancy_score: float, unsafe: bool = False) -> list[FeatureSelectionReason]:
    reasons = []
    if unsafe:
        reasons.append(FeatureSelectionReason.UNSAFE_NAME)

    if coverage_ratio >= 0.70:
        reasons.append(FeatureSelectionReason.GOOD_COVERAGE)
    else:
        reasons.append(FeatureSelectionReason.LOW_COVERAGE)

    if missingness_ratio <= 0.30:
        reasons.append(FeatureSelectionReason.LOW_MISSINGNESS)
    else:
        reasons.append(FeatureSelectionReason.HIGH_MISSINGNESS)

    if stability_score >= 40.0:
        reasons.append(FeatureSelectionReason.STABLE_DISTRIBUTION)
    else:
        reasons.append(FeatureSelectionReason.LOW_STABILITY)

    if redundancy_score <= 80.0:
        reasons.append(FeatureSelectionReason.LOW_REDUNDANCY)
    else:
        reasons.append(FeatureSelectionReason.HIGH_REDUNDANCY)

    return reasons

def build_feature_selection_metadata_for_symbol(symbol: str, df: pd.DataFrame, groups: list[FeatureGroupDefinition], coverage: FeatureCoverageProfile, stability: FeatureStabilityProfile, redundancy: FeatureRedundancyProfile) -> list[FeatureSelectionMetadata]:
    metadata_list = []

    # We evaluate all feature columns
    cols_to_evaluate = [c for c in df.columns if c not in ('symbol', 'timestamp')]
    missingness_dict = feature_missingness_by_column(df, cols_to_evaluate)

    for col in cols_to_evaluate:
        # Find group
        group_name = next((g.group_name for g in groups if col in g.feature_columns), None)

        # Calculate metrics for the single column
        # Coverage is simply 1 - missingness
        missingness_ratio = missingness_dict.get(col, 1.0)
        coverage_ratio = 1.0 - missingness_ratio

        stab_score = stability.stability_scores.get(col, 0.0)

        # Redundancy score logic: if it's involved in many high-correlation pairs, it gets a high score
        red_pairs = [p for p in redundancy.high_redundancy_pairs if p["feature_1"] == col or p["feature_2"] == col]
        # Max pairs it could be involved in is cols_to_evaluate - 1
        max_pairs = max(1, len(cols_to_evaluate) - 1)
        red_score = float(min(100.0, (len(red_pairs) / max_pairs) * 100.0))

        forbidden_columns = ["buy_signal", "sell_signal", "entry", "exit", "position", "order", "portfolio_weight", "target_weight", "broker_order_id", "real_fill_id", "active_trading_signal"]
        unsafe = any(f in col.lower() and "macd_signal" not in col.lower() for f in forbidden_columns)

        status = determine_feature_selection_status(coverage_ratio, missingness_ratio, stab_score, red_score, unsafe)
        reasons = determine_feature_selection_reasons(coverage_ratio, missingness_ratio, stab_score, red_score, unsafe)

        meta = FeatureSelectionMetadata(
            selection_id=create_feature_selection_metadata_id(),
            created_at_utc=_now_str(),
            symbol=symbol,
            feature_column=col,
            group_name=group_name,
            selection_status=status,
            selection_reasons=reasons,
            coverage_ratio=coverage_ratio,
            missingness_ratio=missingness_ratio,
            stability_score=stab_score,
            redundancy_score=red_score,
            research_metadata_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False
        )
        validate_feature_selection_metadata(meta)
        metadata_list.append(meta)

    return metadata_list

def build_feature_selection_metadata(tables: dict[str, pd.DataFrame], groups_by_symbol: dict[str, list[FeatureGroupDefinition]] | None = None) -> list[FeatureSelectionMetadata]:
    from usa_signal_bot.feature_engine.factor_composition.feature_coverage_analyzer import build_feature_coverage_profile
    from usa_signal_bot.feature_engine.factor_composition.feature_stability_analyzer import build_feature_stability_profile
    from usa_signal_bot.feature_engine.factor_composition.feature_redundancy_analyzer import build_feature_redundancy_profile

    all_metadata = []

    for symbol, df in tables.items():
        groups = groups_by_symbol.get(symbol, []) if groups_by_symbol else []
        coverage = build_feature_coverage_profile(symbol, df)
        stability = build_feature_stability_profile(symbol, df)
        redundancy = build_feature_redundancy_profile(symbol, df)

        symbol_metadata = build_feature_selection_metadata_for_symbol(symbol, df, groups, coverage, stability, redundancy)
        all_metadata.extend(symbol_metadata)

    return all_metadata

def feature_selection_metadata_summary(items: list[FeatureSelectionMetadata]) -> dict[str, Any]:
    selected_count = len([i for i in items if i.selection_status == FeatureSelectionStatus.SELECTED_FOR_RESEARCH])
    return {
        "total_items": len(items),
        "selected_for_research": selected_count,
        "symbols": list(set(i.symbol for i in items))
    }

def feature_selection_metadata_to_text(items: list[FeatureSelectionMetadata], limit: int = 200) -> str:
    summary = feature_selection_metadata_summary(items)
    lines = [
        f"Feature Selection Metadata:",
        f"  Total Evaluations: {summary['total_items']}",
        f"  Selected for Research: {summary['selected_for_research']}"
    ]
    for m in items[:limit]:
        lines.append(f"  - {m.symbol} | {m.feature_column}: {m.selection_status.value}")
    return "\n".join(lines)
