from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class IndicatorSet:
    name: str
    indicators: List[str]
    params_by_indicator: Dict[str, Dict[str, Any]]

def basic_volume_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="basic_volume",
        indicators=[
            "volume_average",
            "relative_volume",
            "volume_change",
            "dollar_volume"
        ],
        params_by_indicator={
            "volume_average": {"window": 20, "method": "sma"},
            "relative_volume": {"window": 20},
            "volume_change": {"periods": 1},
            "dollar_volume": {"average_window": 20}
        }
    )

def flow_volume_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="flow_volume",
        indicators=[
            "obv",
            "mfi",
            "cmf",
            "accumulation_distribution"
        ],
        params_by_indicator={
            "mfi": {"window": 14},
            "cmf": {"window": 20}
        }
    )

def liquidity_volume_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="liquidity_volume",
        indicators=[
            "dollar_volume",
            "volume_average",
            "relative_volume",
            "rolling_vwap",
            "vwap"
        ],
        params_by_indicator={
            "dollar_volume": {"average_window": 20},
            "volume_average": {"window": 20, "method": "sma"},
            "relative_volume": {"window": 20},
            "rolling_vwap": {"window": 20}
        }
    )

def full_volume_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="full_volume",
        indicators=[
            "obv",
            "vwap",
            "rolling_vwap",
            "mfi",
            "cmf",
            "accumulation_distribution",
            "volume_average",
            "relative_volume",
            "volume_change",
            "volume_roc",
            "dollar_volume",
            "volume_trend_strength"
        ],
        params_by_indicator={
            "rolling_vwap": {"window": 20},
            "mfi": {"window": 14},
            "cmf": {"window": 20},
            "volume_average": {"window": 20, "method": "sma"},
            "relative_volume": {"window": 20},
            "volume_change": {"periods": 1},
            "volume_roc": {"window": 10},
            "dollar_volume": {"average_window": 20},
            "volume_trend_strength": {"window": 20}
        }
    )

def list_volume_indicator_sets() -> List[IndicatorSet]:
    return [
        basic_volume_indicator_set(),
        flow_volume_indicator_set(),
        liquidity_volume_indicator_set(),
        full_volume_indicator_set()
    ]

def get_volume_indicator_set(name: str) -> IndicatorSet:
    for s in list_volume_indicator_sets():
        if s.name == name:
            return s
    raise ValueError(f"Unknown volume indicator set: {name}")

def volume_indicator_set_to_dict(indicator_set: IndicatorSet) -> dict:
    return {
        "name": indicator_set.name,
        "indicators": indicator_set.indicators,
        "params_by_indicator": indicator_set.params_by_indicator
    }
