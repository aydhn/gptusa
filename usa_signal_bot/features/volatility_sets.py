from typing import List, Dict, Any
from dataclasses import dataclass
from usa_signal_bot.core.exceptions import VolatilityIndicatorSetError

@dataclass
class IndicatorSet:
    name: str
    indicators: List[str]
    params_by_indicator: Dict[str, Dict[str, Any]]

def basic_volatility_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="basic_volatility",
        indicators=[
            "true_range",
            "atr",
            "normalized_atr",
            "rolling_volatility",
            "price_range"
        ],
        params_by_indicator={
            "atr": {"window": 14, "method": "wilder"},
            "normalized_atr": {"window": 14, "method": "wilder"},
            "rolling_volatility": {"window": 20, "annualize": False, "periods_per_year": 252, "column": "close"}
        }
    )

def band_volatility_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="band_volatility",
        indicators=[
            "bollinger_bands",
            "bollinger_bandwidth",
            "bollinger_percent_b"
        ],
        params_by_indicator={
            "bollinger_bands": {"window": 20, "num_std": 2.0, "column": "close"},
            "bollinger_bandwidth": {"window": 20, "num_std": 2.0, "column": "close"},
            "bollinger_percent_b": {"window": 20, "num_std": 2.0, "column": "close"}
        }
    )

def channel_volatility_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="channel_volatility",
        indicators=[
            "keltner_channel",
            "donchian_channel"
        ],
        params_by_indicator={
            "keltner_channel": {"ema_window": 20, "atr_window": 10, "multiplier": 2.0},
            "donchian_channel": {"window": 20}
        }
    )

def compression_volatility_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="compression_volatility",
        indicators=[
            "bollinger_bandwidth",
            "volatility_compression",
            "volatility_expansion",
            "normalized_atr"
        ],
        params_by_indicator={
            "bollinger_bandwidth": {"window": 20, "num_std": 2.0, "column": "close"},
            "volatility_compression": {"window": 20, "reference_window": 100, "num_std": 2.0},
            "volatility_expansion": {"atr_window": 14, "reference_window": 100},
            "normalized_atr": {"window": 14, "method": "wilder"}
        }
    )

def full_volatility_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="full_volatility",
        indicators=[
            "true_range",
            "atr",
            "normalized_atr",
            "bollinger_bands",
            "bollinger_bandwidth",
            "bollinger_percent_b",
            "keltner_channel",
            "donchian_channel",
            "rolling_volatility",
            "price_range",
            "volatility_compression",
            "volatility_expansion"
        ],
        params_by_indicator={
            "atr": {"window": 14, "method": "wilder"},
            "normalized_atr": {"window": 14, "method": "wilder"},
            "bollinger_bands": {"window": 20, "num_std": 2.0, "column": "close"},
            "bollinger_bandwidth": {"window": 20, "num_std": 2.0, "column": "close"},
            "bollinger_percent_b": {"window": 20, "num_std": 2.0, "column": "close"},
            "keltner_channel": {"ema_window": 20, "atr_window": 10, "multiplier": 2.0},
            "donchian_channel": {"window": 20},
            "rolling_volatility": {"window": 20, "annualize": False, "periods_per_year": 252, "column": "close"},
            "volatility_compression": {"window": 20, "reference_window": 100, "num_std": 2.0},
            "volatility_expansion": {"atr_window": 14, "reference_window": 100}
        }
    )

def list_volatility_indicator_sets() -> List[IndicatorSet]:
    return [
        basic_volatility_indicator_set(),
        band_volatility_indicator_set(),
        channel_volatility_indicator_set(),
        compression_volatility_indicator_set(),
        full_volatility_indicator_set()
    ]

def get_volatility_indicator_set(name: str) -> IndicatorSet:
    for s in list_volatility_indicator_sets():
        if s.name == name:
            return s
    raise VolatilityIndicatorSetError(f"Unknown volatility indicator set: {name}")

def volatility_indicator_set_to_dict(indicator_set: IndicatorSet) -> dict:
    return {
        "name": indicator_set.name,
        "indicators": indicator_set.indicators,
        "params_by_indicator": indicator_set.params_by_indicator
    }
