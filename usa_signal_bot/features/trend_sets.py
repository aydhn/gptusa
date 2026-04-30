from dataclasses import dataclass, field
from typing import List, Dict, Any
from usa_signal_bot.core.exceptions import IndicatorSetError

@dataclass
class IndicatorSet:
    name: str
    description: str
    indicators: List[str]
    params_by_indicator: Dict[str, Dict[str, Any]] = field(default_factory=dict)

def basic_trend_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="basic_trend",
        description="Basic trend indicators set",
        indicators=["close_return", "sma", "ema", "price_distance_to_ma", "ma_slope"],
        params_by_indicator={
            "sma": {"window": 20, "column": "close"},
            "ema": {"span": 20, "column": "close"},
            "price_distance_to_ma": {"ma_type": "ema", "window": 20, "price_column": "close"},
            "ma_slope": {"ma_type": "ema", "window": 20, "slope_window": 5, "column": "close"}
        }
    )

def moving_average_trend_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="moving_average_trend",
        description="Moving average trend indicators set",
        indicators=["sma", "ema", "wma", "dema", "tema", "ma_alignment"],
        params_by_indicator={
            "sma": {"window": 20, "column": "close"},
            "ema": {"span": 20, "column": "close"},
            "wma": {"window": 20, "column": "close"},
            "dema": {"span": 20, "column": "close"},
            "tema": {"span": 20, "column": "close"},
            "ma_alignment": {"ma_type": "ema", "short_window": 20, "medium_window": 50, "long_window": 200, "column": "close"}
        }
    )

def macd_trend_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="macd_trend",
        description="MACD trend indicators set",
        indicators=["macd"],
        params_by_indicator={
            "macd": {"fast": 12, "slow": 26, "signal": 9}
        }
    )

def full_trend_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="full_trend",
        description="Full trend indicators set",
        indicators=[
            "close_return", "sma", "ema", "wma", "dema", "tema", "macd",
            "price_distance_to_ma", "ma_slope", "ma_alignment", "trend_strength_basic"
        ],
        params_by_indicator={
            "sma": {"window": 20, "column": "close"},
            "ema": {"span": 20, "column": "close"},
            "wma": {"window": 20, "column": "close"},
            "dema": {"span": 20, "column": "close"},
            "tema": {"span": 20, "column": "close"},
            "macd": {"fast": 12, "slow": 26, "signal": 9},
            "price_distance_to_ma": {"ma_type": "ema", "window": 20, "price_column": "close"},
            "ma_slope": {"ma_type": "ema", "window": 20, "slope_window": 5, "column": "close"},
            "ma_alignment": {"ma_type": "ema", "short_window": 20, "medium_window": 50, "long_window": 200, "column": "close"},
            "trend_strength_basic": {"fast_window": 20, "slow_window": 50, "slope_window": 5, "column": "close"}
        }
    )

_PRESET_SETS = {
    "basic_trend": basic_trend_indicator_set,
    "moving_average_trend": moving_average_trend_indicator_set,
    "macd_trend": macd_trend_indicator_set,
    "full_trend": full_trend_indicator_set,
}

def get_trend_indicator_set(name: str) -> IndicatorSet:
    if name not in _PRESET_SETS:
        raise IndicatorSetError(f"Unknown indicator set: {name}")
    return _PRESET_SETS[name]()

def list_trend_indicator_sets() -> List[IndicatorSet]:
    return [func() for func in _PRESET_SETS.values()]

def indicator_set_to_dict(indicator_set: IndicatorSet) -> Dict[str, Any]:
    return {
        "name": indicator_set.name,
        "description": indicator_set.description,
        "indicators": indicator_set.indicators,
        "params_by_indicator": indicator_set.params_by_indicator
    }
