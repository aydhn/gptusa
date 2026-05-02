from typing import Dict, Any, List
from usa_signal_bot.features.models import IndicatorSet
from usa_signal_bot.core.exceptions import DivergenceIndicatorSetError

def basic_divergence_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="basic_divergence",
        description="Basic divergence indicators (RSI, MACD Histogram)",
        indicators=["rsi_divergence", "macd_hist_divergence"],
        params_by_indicator={}
    )

def oscillator_divergence_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="oscillator_divergence",
        description="Oscillator-based divergence indicators (RSI, MACD, ROC)",
        indicators=["rsi_divergence", "macd_hist_divergence", "roc_divergence"],
        params_by_indicator={}
    )

def volume_divergence_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="volume_divergence",
        description="Volume-based divergence indicators (MFI, OBV)",
        indicators=["mfi_divergence", "obv_divergence"],
        params_by_indicator={}
    )

def full_divergence_indicator_set() -> IndicatorSet:
    return IndicatorSet(
        name="full_divergence",
        description="Full suite of divergence indicators",
        indicators=[
            "rsi_divergence",
            "macd_hist_divergence",
            "roc_divergence",
            "mfi_divergence",
            "obv_divergence"
        ],
        params_by_indicator={}
    )

_DIVERGENCE_SETS = {
    "basic_divergence": basic_divergence_indicator_set,
    "oscillator_divergence": oscillator_divergence_indicator_set,
    "volume_divergence": volume_divergence_indicator_set,
    "full_divergence": full_divergence_indicator_set
}

def get_divergence_indicator_set(name: str) -> IndicatorSet:
    if name not in _DIVERGENCE_SETS:
        raise DivergenceIndicatorSetError(f"Unknown divergence indicator set: {name}")
    return _DIVERGENCE_SETS[name]()

def list_divergence_indicator_sets() -> List[IndicatorSet]:
    return [func() for func in _DIVERGENCE_SETS.values()]

def divergence_indicator_set_to_dict(indicator_set: IndicatorSet) -> Dict[str, Any]:
    return {
        "name": indicator_set.name,
        "description": indicator_set.description,
        "indicators": indicator_set.indicators,
        "params_by_indicator": indicator_set.params_by_indicator
    }
