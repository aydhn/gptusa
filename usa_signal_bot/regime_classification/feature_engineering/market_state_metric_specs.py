from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import MarketStateMetricSpec, MarketStateMetricKind

def build_default_market_state_metric_specs() -> list[MarketStateMetricSpec]:
    return [
        MarketStateMetricSpec(metric_name="market_return_context_20", metric_kind=MarketStateMetricKind.MARKET_RETURN_CONTEXT, output_column="market_return_context_20", window=20),
        MarketStateMetricSpec(metric_name="market_volatility_context_20", metric_kind=MarketStateMetricKind.MARKET_VOLATILITY_CONTEXT, output_column="market_volatility_context_20", window=20),
        MarketStateMetricSpec(metric_name="market_trend_context_50", metric_kind=MarketStateMetricKind.MARKET_TREND_CONTEXT, output_column="market_trend_context_50", window=50),
        MarketStateMetricSpec(metric_name="market_momentum_context_60", metric_kind=MarketStateMetricKind.MARKET_MOMENTUM_CONTEXT, output_column="market_momentum_context_60", window=60),
        MarketStateMetricSpec(metric_name="market_liquidity_context_20", metric_kind=MarketStateMetricKind.MARKET_LIQUIDITY_CONTEXT, output_column="market_liquidity_context_20", window=20),
        MarketStateMetricSpec(metric_name="factor_strength_context", metric_kind=MarketStateMetricKind.FACTOR_STRENGTH_CONTEXT, output_column="factor_strength_context"),
        MarketStateMetricSpec(metric_name="factor_disagreement_context", metric_kind=MarketStateMetricKind.FACTOR_DISAGREEMENT_CONTEXT, output_column="factor_disagreement_context"),
        MarketStateMetricSpec(metric_name="cross_sectional_dispersion_context", metric_kind=MarketStateMetricKind.CROSS_SECTIONAL_DISPERSION, output_column="cross_sectional_dispersion_context"),
        MarketStateMetricSpec(metric_name="data_quality_context", metric_kind=MarketStateMetricKind.DATA_QUALITY_CONTEXT, output_column="data_quality_context"),
        MarketStateMetricSpec(metric_name="event_pressure_context", metric_kind=MarketStateMetricKind.EVENT_PRESSURE_CONTEXT, output_column="event_pressure_context"),
        MarketStateMetricSpec(metric_name="calendar_pressure_context", metric_kind=MarketStateMetricKind.CALENDAR_PRESSURE_CONTEXT, output_column="calendar_pressure_context")
    ]

def validate_market_state_metric_specs(specs: list[MarketStateMetricSpec]) -> list[str]:
    return []
