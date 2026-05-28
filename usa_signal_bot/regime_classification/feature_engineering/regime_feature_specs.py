from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureSpec, RegimeFeatureKind

def build_default_regime_feature_specs() -> list[RegimeFeatureSpec]:
    return [
        RegimeFeatureSpec(feature_name="regime_volatility_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_volatility_state_feature", source_metric_names=["market_volatility_context_20"]),
        RegimeFeatureSpec(feature_name="regime_trend_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_trend_state_feature", source_metric_names=["market_trend_context_50"]),
        RegimeFeatureSpec(feature_name="regime_momentum_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_momentum_state_feature", source_metric_names=["market_momentum_context_60"]),
        RegimeFeatureSpec(feature_name="regime_liquidity_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_liquidity_state_feature", source_metric_names=["market_liquidity_context_20"]),
        RegimeFeatureSpec(feature_name="regime_breadth_state_feature", feature_kind=RegimeFeatureKind.MARKET_STATE_FEATURE, output_column="regime_breadth_state_feature", source_metric_names=["cross_sectional_dispersion_context"]),
        RegimeFeatureSpec(feature_name="regime_factor_strength_feature", feature_kind=RegimeFeatureKind.FACTOR_CONTEXT_FEATURE, output_column="regime_factor_strength_feature", source_metric_names=["factor_strength_context"]),
        RegimeFeatureSpec(feature_name="regime_factor_disagreement_feature", feature_kind=RegimeFeatureKind.FACTOR_CONTEXT_FEATURE, output_column="regime_factor_disagreement_feature", source_metric_names=["factor_disagreement_context"]),
        RegimeFeatureSpec(feature_name="regime_quality_state_feature", feature_kind=RegimeFeatureKind.QUALITY_CONTEXT_FEATURE, output_column="regime_quality_state_feature", source_metric_names=["data_quality_context"]),
        RegimeFeatureSpec(feature_name="regime_event_pressure_feature", feature_kind=RegimeFeatureKind.EVENT_CONTEXT_FEATURE, output_column="regime_event_pressure_feature", source_metric_names=["event_pressure_context"]),
        RegimeFeatureSpec(feature_name="regime_calendar_pressure_feature", feature_kind=RegimeFeatureKind.CALENDAR_CONTEXT_FEATURE, output_column="regime_calendar_pressure_feature", source_metric_names=["calendar_pressure_context"]),
        RegimeFeatureSpec(feature_name="regime_candidate_prep_feature", feature_kind=RegimeFeatureKind.CANDIDATE_PREP_FEATURE, output_column="regime_candidate_prep_feature", source_metric_names=[])
    ]

def validate_regime_feature_specs(specs: list[RegimeFeatureSpec]) -> list[str]:
    return []
