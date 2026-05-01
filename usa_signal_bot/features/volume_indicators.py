import pandas as pd
from typing import Dict, Any

from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec
from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType
from usa_signal_bot.core.exceptions import FeatureComputationError, IndicatorParameterError
from usa_signal_bot.features.volume_utils import (
    calculate_obv, calculate_vwap, calculate_rolling_vwap,
    calculate_money_flow_index, calculate_chaikin_money_flow,
    calculate_accumulation_distribution_line, calculate_volume_sma,
    calculate_volume_ema, calculate_relative_volume,
    calculate_volume_change, calculate_volume_roc,
    calculate_dollar_volume, calculate_average_dollar_volume,
    calculate_volume_trend_strength
)

class OBVIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="obv",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="On-Balance Volume",
            required_columns=["close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={},
            produces=["obv"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        self.validate_params(params)
        for col in ["close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res["obv"] = calculate_obv(df["close"], df["volume"])
        return res

class VWAPIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="vwap",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Volume Weighted Average Price",
            required_columns=["high", "low", "close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={},
            produces=["vwap"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        self.validate_params(params)
        for col in ["high", "low", "close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res["vwap"] = calculate_vwap(df["high"], df["low"], df["close"], df["volume"])
        return res

class RollingVWAPIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="rolling_vwap",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Rolling VWAP",
            required_columns=["high", "low", "close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20},
            produces=["rolling_vwap_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        for col in ["high", "low", "close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"rolling_vwap_{window}"] = calculate_rolling_vwap(df["high"], df["low"], df["close"], df["volume"], window)
        return res

class MFIIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="mfi",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Money Flow Index",
            required_columns=["high", "low", "close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 14},
            produces=["mfi_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="window", param_type="int", default=14, min_value=2, max_value=100)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        for col in ["high", "low", "close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"mfi_{window}"] = calculate_money_flow_index(df["high"], df["low"], df["close"], df["volume"], window)
        return res

class CMFIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="cmf",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Chaikin Money Flow",
            required_columns=["high", "low", "close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20},
            produces=["cmf_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=200)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        for col in ["high", "low", "close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"cmf_{window}"] = calculate_chaikin_money_flow(df["high"], df["low"], df["close"], df["volume"], window)
        return res

class AccumulationDistributionIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="accumulation_distribution",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Accumulation/Distribution Line",
            required_columns=["high", "low", "close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={},
            produces=["adl"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        self.validate_params(params)
        for col in ["high", "low", "close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res["adl"] = calculate_accumulation_distribution_line(df["high"], df["low"], df["close"], df["volume"])
        return res

class VolumeAverageIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volume_average",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Volume SMA/EMA",
            required_columns=["volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "method": "sma"},
            produces=["volume_{method}_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="method", param_type="str", default="sma", allowed_values=["sma", "ema"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        method = p["method"].lower()
        if "volume" not in df.columns:
            raise FeatureComputationError("Missing required column: volume")

        res = df.copy()
        if method == "sma":
            res[f"volume_{method}_{window}"] = calculate_volume_sma(df["volume"], window)
        else:
            res[f"volume_{method}_{window}"] = calculate_volume_ema(df["volume"], window)
        return res

class RelativeVolumeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="relative_volume",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Relative Volume",
            required_columns=["volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20},
            produces=["relative_volume_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        if "volume" not in df.columns:
            raise FeatureComputationError("Missing required column: volume")

        res = df.copy()
        res[f"relative_volume_{window}"] = calculate_relative_volume(df["volume"], window)
        return res

class VolumeChangeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volume_change",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Volume Change",
            required_columns=["volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"periods": 1},
            produces=["volume_change_{periods}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="periods", param_type="int", default=1, min_value=1, max_value=252)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        periods = p["periods"]
        if "volume" not in df.columns:
            raise FeatureComputationError("Missing required column: volume")

        res = df.copy()
        res[f"volume_change_{periods}"] = calculate_volume_change(df["volume"], periods)
        return res

class VolumeROCIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volume_roc",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Volume ROC",
            required_columns=["volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 10},
            produces=["volume_roc_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="window", param_type="int", default=10, min_value=1, max_value=252)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        if "volume" not in df.columns:
            raise FeatureComputationError("Missing required column: volume")

        res = df.copy()
        res[f"volume_roc_{window}"] = calculate_volume_roc(df["volume"], window)
        return res

class DollarVolumeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="dollar_volume",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Dollar Volume",
            required_columns=["close", "volume"],
            min_bars=1,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={"average_window": 20},
            produces=["dollar_volume", "avg_dollar_volume_{average_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="average_window", param_type="int", default=20, min_value=1, max_value=500)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["average_window"]
        for col in ["close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res["dollar_volume"] = calculate_dollar_volume(df["close"], df["volume"])
        res[f"avg_dollar_volume_{window}"] = calculate_average_dollar_volume(df["close"], df["volume"], window)
        return res

class VolumeTrendStrengthIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volume_trend_strength",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Volume Trend Strength",
            required_columns=["close", "volume"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20},
            produces=["volume_trend_strength_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500)]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        for col in ["close", "volume"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"volume_trend_strength_{window}"] = calculate_volume_trend_strength(df["volume"], df["close"], window)
        return res
