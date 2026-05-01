from dataclasses import dataclass, field
from typing import List, Dict, Any
from usa_signal_bot.core.exceptions import IndicatorSetError

@dataclass
class IndicatorSet:
    name: str
    description: str
    indicators: List[str]
    params_by_indicator: Dict[str, Dict[str, Any]] = field(default_factory=dict)

def basic_price_action_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="basic_price_action",
        description="Basic price action features",
        indicators=["candle_features", "wick_features", "close_location_value", "gap_features"]
    )

def breakout_price_action_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="breakout_price_action",
        description="Breakout and range expansion features",
        indicators=["breakout_distance", "breakdown_distance", "range_expansion"],
        params_by_indicator={
            "breakout_distance": {"window": 20},
            "breakdown_distance": {"window": 20},
            "range_expansion": {"window": 20}
        }
    )

def structure_price_action_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="structure_price_action",
        description="Market structure and bar pattern features",
        indicators=["inside_outside_bar", "swing_points", "market_structure"],
        params_by_indicator={
            "swing_points": {"left_window": 2, "right_window": 2},
            "market_structure": {"swing_left": 2, "swing_right": 2}
        }
    )

def candle_price_action_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="candle_price_action",
        description="Detailed candle shape and pattern features",
        indicators=["candle_features", "wick_features", "close_location_value", "inside_outside_bar"]
    )

def full_price_action_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="full_price_action",
        description="Full suite of price action features",
        indicators=[
            "candle_features", "wick_features", "close_location_value", "gap_features",
            "breakout_distance", "breakdown_distance", "inside_outside_bar",
            "swing_points", "market_structure", "range_expansion"
        ],
        params_by_indicator={
            "breakout_distance": {"window": 20},
            "breakdown_distance": {"window": 20},
            "swing_points": {"left_window": 2, "right_window": 2},
            "market_structure": {"swing_left": 2, "swing_right": 2},
            "range_expansion": {"window": 20}
        }
    )

_PRESET_SETS = {
    "basic_price_action": basic_price_action_indicator_set,
    "breakout_price_action": breakout_price_action_indicator_set,
    "structure_price_action": structure_price_action_indicator_set,
    "candle_price_action": candle_price_action_indicator_set,
    "full_price_action": full_price_action_indicator_set,
}

def get_price_action_indicator_set(name: str) -> IndicatorSet:
    if name not in _PRESET_SETS:
        raise IndicatorSetError(f"Unknown price action indicator set: {name}")
    return _PRESET_SETS[name]()

def list_price_action_indicator_sets() -> List[IndicatorSet]:
    return [func() for func in _PRESET_SETS.values()]

def price_action_indicator_set_to_dict(indicator_set: IndicatorSet) -> Dict[str, Any]:
    return {
        "name": indicator_set.name,
        "description": indicator_set.description,
        "indicators": indicator_set.indicators,
        "params_by_indicator": indicator_set.params_by_indicator
    }
