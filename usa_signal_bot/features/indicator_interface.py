from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd

from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, merge_params_with_defaults
from usa_signal_bot.core.exceptions import FeatureComputationError

class Indicator(ABC):

    @property
    @abstractmethod
    def metadata(self) -> IndicatorMetadata:
        pass

    @property
    @abstractmethod
    def parameter_schema(self) -> IndicatorParameterSchema:
        pass

    @abstractmethod
    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        pass

    def validate_input_frame(self, data: pd.DataFrame) -> None:
        if data.empty:
            raise FeatureComputationError(f"Input DataFrame is empty for indicator {self.metadata.name}")

        missing_cols = [col for col in self.metadata.required_columns if col not in data.columns]
        if missing_cols:
            raise FeatureComputationError(f"Missing required columns for {self.metadata.name}: {missing_cols}")

        if len(data) < self.metadata.min_bars:
            raise FeatureComputationError(f"Not enough bars for {self.metadata.name}. Expected >= {self.metadata.min_bars}, got {len(data)}")

    def validate_params(self, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return merge_params_with_defaults(self.parameter_schema, params)

    def required_columns(self) -> List[str]:
        return self.metadata.required_columns

    def output_columns(self, params: Dict[str, Any] | None = None) -> List[str]:
        valid_params = self.validate_params(params)
        return [p.format(**valid_params) for p in self.metadata.produces]
