from dataclasses import dataclass, field
from typing import List, Dict, Any
from usa_signal_bot.core.exceptions import MomentumIndicatorSetError

@dataclass
class IndicatorSet:
    name: str
    description: str
    indicators: List[str]
    params_by_indicator: Dict[str, Dict[str, Any]] = field(default_factory=dict)

_PRESET_SETS = {
    "basic_momentum": lambda: IndicatorSet("basic_momentum", "Basic", ["rsi", "roc", "momentum"], {"rsi": {"window": 14, "column": "close"}, "roc": {"window": 12, "column": "close"}, "momentum": {"window": 10, "column": "close"}}),
    "oscillator_momentum": lambda: IndicatorSet("oscillator_momentum", "Oscillator", ["rsi", "stochastic", "williams_r", "cci"], {"rsi": {"window": 14, "column": "close"}, "stochastic": {"k_window": 14, "d_window": 3}, "williams_r": {"window": 14}, "cci": {"window": 20, "constant": 0.015}}),
    "rate_of_change_momentum": lambda: IndicatorSet("rate_of_change_momentum", "ROC", ["roc", "momentum", "momentum_slope", "momentum_acceleration", "normalized_momentum"], {"roc": {"window": 12, "column": "close"}, "momentum": {"window": 10, "column": "close"}, "momentum_slope": {"base_indicator": "roc", "window": 12, "slope_window": 5, "column": "close"}, "momentum_acceleration": {"base_indicator": "roc", "window": 12, "slope_window": 5, "column": "close"}, "normalized_momentum": {"window": 20, "normalization_window": 100, "column": "close"}}),
    "full_momentum": lambda: IndicatorSet("full_momentum", "Full", ["rsi", "stochastic", "roc", "momentum", "williams_r", "cci", "momentum_slope", "momentum_acceleration", "normalized_momentum"], {"rsi": {"window": 14, "column": "close"}, "stochastic": {"k_window": 14, "d_window": 3}, "roc": {"window": 12, "column": "close"}, "momentum": {"window": 10, "column": "close"}, "williams_r": {"window": 14}, "cci": {"window": 20, "constant": 0.015}, "momentum_slope": {"base_indicator": "rsi", "window": 14, "slope_window": 5, "column": "close"}, "momentum_acceleration": {"base_indicator": "roc", "window": 12, "slope_window": 5, "column": "close"}, "normalized_momentum": {"window": 20, "normalization_window": 100, "column": "close"}})
}

def get_momentum_indicator_set(name: str) -> IndicatorSet:
    if name not in _PRESET_SETS: raise MomentumIndicatorSetError(f"Unknown momentum indicator set: {name}")
    return _PRESET_SETS[name]()

def list_momentum_indicator_sets() -> List[IndicatorSet]:
    return [func() for func in _PRESET_SETS.values()]

def momentum_indicator_set_to_dict(indicator_set: IndicatorSet) -> Dict[str, Any]:
    return {"name": indicator_set.name, "description": indicator_set.description, "indicators": indicator_set.indicators, "params_by_indicator": indicator_set.params_by_indicator}
