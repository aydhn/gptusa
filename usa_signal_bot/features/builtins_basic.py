from typing import Dict, Any
import pandas as pd

from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec
from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType

class CloseReturnIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="close_return",
            version="1.0.0",
            category=IndicatorCategory.MOMENTUM,
            output_type=IndicatorOutputType.SERIES,
            description="Calculates percentage return of close price over N periods.",
            required_columns=["close"],
            default_params={"periods": 1},
            min_bars=2,
            produces=["close_return_{periods}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name="close_return",
            parameters=[
                IndicatorParameterSpec(name="periods", param_type="int", default=1, required=False, min_value=1, max_value=252, description="Periods to calculate return")
            ]
        )

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        valid_params = self.validate_params(params)
        periods = valid_params["periods"]

        output_col = self.metadata.produces[0].format(periods=periods)

        df = pd.DataFrame(index=data.index)
        df[output_col] = data["close"].pct_change(periods=periods)
        return df

class CloseSMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="close_sma",
            version="1.0.0",
            category=IndicatorCategory.TREND,
            output_type=IndicatorOutputType.SERIES,
            description="Simple Moving Average of close price.",
            required_columns=["close"],
            default_params={"window": 20},
            min_bars=2,
            produces=["close_sma_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name="close_sma",
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, required=False, min_value=2, max_value=500, description="SMA window size")
            ]
        )

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        valid_params = self.validate_params(params)
        window = valid_params["window"]

        output_col = self.metadata.produces[0].format(window=window)

        df = pd.DataFrame(index=data.index)
        df[output_col] = data["close"].rolling(window=window).mean()
        return df

class CloseEMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="close_ema",
            version="1.0.0",
            category=IndicatorCategory.TREND,
            output_type=IndicatorOutputType.SERIES,
            description="Exponential Moving Average of close price.",
            required_columns=["close"],
            default_params={"span": 20},
            min_bars=2,
            produces=["close_ema_{span}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name="close_ema",
            parameters=[
                IndicatorParameterSpec(name="span", param_type="int", default=20, required=False, min_value=2, max_value=500, description="EMA span")
            ]
        )

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        valid_params = self.validate_params(params)
        span = valid_params["span"]

        output_col = self.metadata.produces[0].format(span=span)

        df = pd.DataFrame(index=data.index)
        df[output_col] = data["close"].ewm(span=span, adjust=False).mean()
        return df

class VolumeSMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volume_sma",
            version="1.0.0",
            category=IndicatorCategory.VOLUME,
            output_type=IndicatorOutputType.SERIES,
            description="Simple Moving Average of volume.",
            required_columns=["volume"],
            default_params={"window": 20},
            min_bars=2,
            produces=["volume_sma_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name="volume_sma",
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, required=False, min_value=2, max_value=500, description="SMA window size")
            ]
        )

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        valid_params = self.validate_params(params)
        window = valid_params["window"]

        output_col = self.metadata.produces[0].format(window=window)

        df = pd.DataFrame(index=data.index)
        df[output_col] = data["volume"].rolling(window=window).mean()
        return df

class RollingHighIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="rolling_high",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.SERIES,
            description="Rolling maximum of high price.",
            required_columns=["high"],
            default_params={"window": 20},
            min_bars=2,
            produces=["rolling_high_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name="rolling_high",
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, required=False, min_value=2, max_value=500, description="Rolling window size")
            ]
        )

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        valid_params = self.validate_params(params)
        window = valid_params["window"]

        output_col = self.metadata.produces[0].format(window=window)

        df = pd.DataFrame(index=data.index)
        df[output_col] = data["high"].rolling(window=window).max()
        return df

class RollingLowIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="rolling_low",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.SERIES,
            description="Rolling minimum of low price.",
            required_columns=["low"],
            default_params={"window": 20},
            min_bars=2,
            produces=["rolling_low_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name="rolling_low",
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, required=False, min_value=2, max_value=500, description="Rolling window size")
            ]
        )

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        valid_params = self.validate_params(params)
        window = valid_params["window"]

        output_col = self.metadata.produces[0].format(window=window)

        df = pd.DataFrame(index=data.index)
        df[output_col] = data["low"].rolling(window=window).min()
        return df
