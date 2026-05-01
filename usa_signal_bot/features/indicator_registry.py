from typing import List, Dict

from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata, validate_indicator_metadata
from usa_signal_bot.features.indicator_params import validate_parameter_schema
from usa_signal_bot.core.enums import IndicatorCategory
from usa_signal_bot.core.exceptions import IndicatorRegistrationError, IndicatorError

class IndicatorRegistry:
    def __init__(self):
        self._indicators: Dict[str, Indicator] = {}

    def register(self, indicator: Indicator) -> None:
        name = indicator.metadata.name
        if name in self._indicators:
            raise IndicatorRegistrationError(f"Indicator '{name}' is already registered")

        validate_indicator_metadata(indicator.metadata)
        validate_parameter_schema(indicator.parameter_schema)

        self._indicators[name] = indicator

    def get(self, name: str) -> Indicator:
        if name not in self._indicators:
            raise IndicatorError(f"Indicator '{name}' not found in registry")
        return self._indicators[name]

    def has(self, name: str) -> bool:
        return name in self._indicators

    def unregister(self, name: str) -> None:
        if name in self._indicators:
            del self._indicators[name]

    def list_all(self) -> List[Indicator]:
        return list(self._indicators.values())

    def list_names(self) -> List[str]:
        return list(self._indicators.keys())

    def list_metadata(self) -> List[IndicatorMetadata]:
        return [ind.metadata for ind in self._indicators.values()]

    def list_by_category(self, category: IndicatorCategory) -> List[Indicator]:
        return [ind for ind in self._indicators.values() if ind.metadata.category == category]

    def validate_all(self) -> None:
        for ind in self._indicators.values():
            validate_indicator_metadata(ind.metadata)
            validate_parameter_schema(ind.parameter_schema)

_DEFAULT_REGISTRY = None

def get_default_registry() -> IndicatorRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        _DEFAULT_REGISTRY = create_default_indicator_registry()
    return _DEFAULT_REGISTRY

def register_builtin_indicators(registry) -> 'IndicatorRegistry':
    from usa_signal_bot.features.builtins_basic import (
        CloseReturnIndicator, CloseSMAIndicator, CloseEMAIndicator,
        VolumeSMAIndicator, RollingHighIndicator, RollingLowIndicator
    )
    from usa_signal_bot.features.trend_indicators import (
        SMAIndicator, EMAIndicator, WMAIndicator, DEMAIndicator,
        TEMAIndicator, MACDIndicator, PriceDistanceToMAIndicator,
        MASlopeIndicator, MAAlignmentIndicator, TrendStrengthBasicIndicator
    )
    from usa_signal_bot.features.momentum_indicators import (
        RSIIndicator, StochasticIndicator, ROCIndicator,
        MomentumIndicator, WilliamsRIndicator, CCIIndicator,
        MomentumSlopeIndicator, MomentumAccelerationIndicator, NormalizedMomentumIndicator
    )
    from usa_signal_bot.features.volatility_indicators import (
        TrueRangeIndicator, ATRIndicator, NormalizedATRIndicator,
        BollingerBandsIndicator, BollingerBandwidthIndicator, BollingerPercentBIndicator,
        KeltnerChannelIndicator, DonchianChannelIndicator, RollingVolatilityIndicator,
        PriceRangeIndicator, VolatilityCompressionIndicator, VolatilityExpansionIndicator
    )

    registry.register(CloseReturnIndicator())
    registry.register(CloseSMAIndicator())
    registry.register(CloseEMAIndicator())
    registry.register(VolumeSMAIndicator())
    registry.register(RollingHighIndicator())
    registry.register(RollingLowIndicator())

    registry.register(SMAIndicator())
    registry.register(EMAIndicator())
    registry.register(WMAIndicator())
    registry.register(DEMAIndicator())
    registry.register(TEMAIndicator())
    registry.register(MACDIndicator())
    registry.register(PriceDistanceToMAIndicator())
    registry.register(MASlopeIndicator())
    registry.register(MAAlignmentIndicator())
    registry.register(TrendStrengthBasicIndicator())

    registry.register(RSIIndicator())
    registry.register(StochasticIndicator())
    registry.register(ROCIndicator())
    registry.register(MomentumIndicator())
    registry.register(WilliamsRIndicator())
    registry.register(CCIIndicator())
    registry.register(MomentumSlopeIndicator())
    registry.register(MomentumAccelerationIndicator())
    registry.register(NormalizedMomentumIndicator())

    registry.register(TrueRangeIndicator())
    registry.register(ATRIndicator())
    registry.register(NormalizedATRIndicator())
    registry.register(BollingerBandsIndicator())
    registry.register(BollingerBandwidthIndicator())
    registry.register(BollingerPercentBIndicator())
    registry.register(KeltnerChannelIndicator())
    registry.register(DonchianChannelIndicator())
    registry.register(RollingVolatilityIndicator())
    registry.register(PriceRangeIndicator())
    registry.register(VolatilityCompressionIndicator())
    registry.register(VolatilityExpansionIndicator())

    return registry

def create_default_indicator_registry() -> IndicatorRegistry:
    registry = IndicatorRegistry()
    register_builtin_indicators(registry)
    return registry
