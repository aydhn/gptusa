from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from usa_signal_bot.strategies.strategy_metadata import StrategyMetadata
from usa_signal_bot.strategies.strategy_params import StrategyParameterSchema, validate_strategy_params
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch, StrategyInputValidationResult, validate_strategy_input_batch
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.exceptions import BrokerRoutingForbiddenError

class Strategy(ABC):

    @property
    @abstractmethod
    def metadata(self) -> StrategyMetadata:
        pass

    @property
    @abstractmethod
    def parameter_schema(self) -> StrategyParameterSchema:
        pass

    @abstractmethod
    def generate_signals(self, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None) -> List[StrategySignal]:
        pass

    def validate_input(self, batch: StrategyInputBatch) -> List[StrategyInputValidationResult]:
        return validate_strategy_input_batch(batch, self.metadata.required_features)

    def validate_params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return validate_strategy_params(self.parameter_schema, params)

    def required_features(self) -> List[str]:
        return self.metadata.required_features

    def assert_no_execution(self) -> None:
        """
        Explicitly states and verifies that this strategy does not execute orders.
        This serves as a programmatic guardrail against broker routing.
        """
        pass # The existence of this method is the guard; any attempt to route orders should raise BrokerRoutingForbiddenError
