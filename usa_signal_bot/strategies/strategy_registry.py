from typing import Dict, List, Optional
from usa_signal_bot.strategies.strategy_interface import Strategy
from usa_signal_bot.strategies.strategy_metadata import StrategyMetadata, validate_strategy_metadata
from usa_signal_bot.core.enums import StrategyCategory
from usa_signal_bot.core.exceptions import StrategyRegistrationError

class StrategyRegistry:
    def __init__(self):
        self._strategies: Dict[str, Strategy] = {}

    def register(self, strategy: Strategy) -> None:
        if not strategy:
            raise StrategyRegistrationError("Cannot register None strategy")

        name = strategy.metadata.name
        if not name:
            raise StrategyRegistrationError("Strategy must have a name")

        if name in self._strategies:
            raise StrategyRegistrationError(f"Strategy already registered: {name}")

        validate_strategy_metadata(strategy.metadata)
        self._strategies[name] = strategy

    def get(self, name: str) -> Strategy:
        if name not in self._strategies:
            raise StrategyRegistrationError(f"Strategy not found: {name}")
        return self._strategies[name]

    def has(self, name: str) -> bool:
        return name in self._strategies

    def unregister(self, name: str) -> None:
        if name in self._strategies:
            del self._strategies[name]

    def list_names(self) -> List[str]:
        return list(self._strategies.keys())

    def list_metadata(self) -> List[StrategyMetadata]:
        return [s.metadata for s in self._strategies.values()]

    def list_by_category(self, category: StrategyCategory) -> List[Strategy]:
        return [s for s in self._strategies.values() if s.metadata.category == category]

    def validate_all(self) -> None:
        for name, strategy in self._strategies.items():
            try:
                validate_strategy_metadata(strategy.metadata)
            except Exception as e:
                raise StrategyRegistrationError(f"Validation failed for strategy {name}: {e}")

def create_default_strategy_registry() -> StrategyRegistry:
    from usa_signal_bot.strategies.example_strategies import (
        TrendFollowingSkeletonStrategy,
        MeanReversionSkeletonStrategy,
        MomentumSkeletonStrategy,
        VolatilityBreakoutSkeletonStrategy
    )

    registry = StrategyRegistry()
    registry.register(TrendFollowingSkeletonStrategy())
    registry.register(MeanReversionSkeletonStrategy())
    registry.register(MomentumSkeletonStrategy())
    registry.register(VolatilityBreakoutSkeletonStrategy())

    return registry
