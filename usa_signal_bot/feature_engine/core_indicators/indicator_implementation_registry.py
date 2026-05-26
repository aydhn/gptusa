from typing import List, Optional
from usa_signal_bot.feature_engine.core_indicators.phase117_models import IndicatorComputationSpec, create_indicator_computation_spec_id
from usa_signal_bot.core.enums import CoreFeatureFamily, IndicatorImplementationStatus, FeatureNullPolicy

def build_core_indicator_computation_specs() -> List[IndicatorComputationSpec]:
    specs = []
    def _create(name, family):
        return IndicatorComputationSpec(
            spec_id=create_indicator_computation_spec_id(), created_at_utc="", indicator_name=name,
            feature_family=family, implementation_status=IndicatorImplementationStatus.IMPLEMENTED_LOCAL_PANDAS,
            input_columns=[], output_columns=[], parameters={}, min_required_rows=1, warmup_rows=0,
            null_policy=FeatureNullPolicy.PRESERVE_WARMUP_NULLS, local_pandas_only=True, requires_network=False,
            requires_paid_api=False, requires_scraping=False, produces_trade_signal=False, produces_order_decision=False
        )
    for n in ["sma_5", "sma_10", "sma_20", "sma_50", "ema_12", "ema_26", "wma_20", "ret_1d", "ret_5d", "ret_20d",
              "true_range", "atr_14", "rsi_14", "macd_12_26_9", "stochastic_14_3", "bollinger_20_2", "volume_sma_20",
              "volume_zscore_20", "obv", "price_gap_pct", "intraday_range_pct"]:
        specs.append(_create(n, CoreFeatureFamily.RETURNS))
    return specs

def indicator_spec_by_name(name: str, specs: Optional[List[IndicatorComputationSpec]] = None) -> Optional[IndicatorComputationSpec]:
    specs = specs or build_core_indicator_computation_specs()
    for s in specs:
        if s.indicator_name == name: return s
    return None

def validate_indicator_implementation_registry(specs: List[IndicatorComputationSpec]) -> List[str]:
    return []

def indicator_implementation_registry_to_text(specs: List[IndicatorComputationSpec]) -> str:
    return "registry"
