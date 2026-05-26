from typing import Any
from usa_signal_bot.feature_engine.core_indicators.phase117_models import IndicatorComputationSpec, IndicatorImplementationStatus, CoreFeatureFamily, FeatureNullPolicy, create_indicator_computation_spec_id, _dt

def build_core_indicator_computation_specs() -> list[IndicatorComputationSpec]:
    names = [
        ("daily_return", CoreFeatureFamily.RETURNS), ("log_return", CoreFeatureFamily.RETURNS),
        ("rolling_return_5", CoreFeatureFamily.RETURNS), ("rolling_return_20", CoreFeatureFamily.RETURNS),
        ("sma_5", CoreFeatureFamily.MOVING_AVERAGES), ("sma_10", CoreFeatureFamily.MOVING_AVERAGES),
        ("sma_20", CoreFeatureFamily.MOVING_AVERAGES), ("sma_50", CoreFeatureFamily.MOVING_AVERAGES),
        ("ema_12", CoreFeatureFamily.MOVING_AVERAGES), ("ema_26", CoreFeatureFamily.MOVING_AVERAGES),
        ("wma_20", CoreFeatureFamily.MOVING_AVERAGES),
        ("rolling_volatility_20", CoreFeatureFamily.VOLATILITY),
        ("true_range", CoreFeatureFamily.TRUE_RANGE_ATR), ("atr_14", CoreFeatureFamily.TRUE_RANGE_ATR),
        ("rsi_14", CoreFeatureFamily.MOMENTUM_RSI),
        ("macd_12_26_9", CoreFeatureFamily.MOMENTUM_MACD),
        ("stochastic_14_3", CoreFeatureFamily.STOCHASTIC),
        ("bollinger_20_2", CoreFeatureFamily.BOLLINGER),
        ("volume_sma_20", CoreFeatureFamily.VOLUME), ("volume_zscore_20", CoreFeatureFamily.VOLUME), ("obv", CoreFeatureFamily.VOLUME),
        ("price_gap_pct", CoreFeatureFamily.GAP_RANGE_CANDLE), ("intraday_range_pct", CoreFeatureFamily.GAP_RANGE_CANDLE),
        ("candle_body_pct", CoreFeatureFamily.GAP_RANGE_CANDLE), ("upper_shadow_pct", CoreFeatureFamily.GAP_RANGE_CANDLE),
        ("lower_shadow_pct", CoreFeatureFamily.GAP_RANGE_CANDLE)
    ]
    return [
        IndicatorComputationSpec(
            spec_id=create_indicator_computation_spec_id(), created_at_utc=_dt(), indicator_name=n, feature_family=f,
            implementation_status=IndicatorImplementationStatus.IMPLEMENTED_LOCAL_PANDAS,
            input_columns=['close'], output_columns=[n], parameters={}, min_required_rows=100, warmup_rows=20,
            null_policy=FeatureNullPolicy.PRESERVE_WARMUP_NULLS, local_pandas_only=True,
            requires_network=False, requires_paid_api=False, requires_scraping=False,
            produces_trade_signal=False, produces_order_decision=False
        ) for n, f in names
    ]

def indicator_spec_by_name(name: str, specs: list[IndicatorComputationSpec] = None) -> IndicatorComputationSpec | None:
    specs = specs or build_core_indicator_computation_specs()
    for s in specs:
        if s.indicator_name == name: return s
    return None

def implemented_indicator_names() -> list[str]: return [s.indicator_name for s in build_core_indicator_computation_specs()]
def validate_indicator_implementation_registry(specs: list[IndicatorComputationSpec]) -> list[str]: return []
def indicator_implementation_registry_summary(specs: list[IndicatorComputationSpec]) -> dict[str, Any]: return {}
def indicator_implementation_registry_to_text(specs: list[IndicatorComputationSpec], limit: int = 200) -> str: return ""
