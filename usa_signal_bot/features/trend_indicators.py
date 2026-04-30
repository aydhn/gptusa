import pandas as pd
from typing import Dict, Any, List
from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec
from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType
from usa_signal_bot.core.exceptions import IndicatorParameterError, FeatureComputationError
from usa_signal_bot.features.trend_utils import (
    calculate_sma, calculate_ema, calculate_wma, calculate_dema, calculate_tema,
    calculate_macd, calculate_series_slope, calculate_price_distance_pct,
    calculate_ma_alignment_score, validate_window, validate_macd_params
)

class SMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="sma",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Simple Moving Average",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "column": "close"},
            produces=["{column}_sma_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "volume", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        column = p["column"]
        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        out_col = f"{column}_sma_{window}"
        res = df.copy()
        res[out_col] = calculate_sma(df[column], window)
        return res

class EMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="ema",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Exponential Moving Average",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"span": 20, "column": "close"},
            produces=["{column}_ema_{span}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="span", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "volume", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        span = p["span"]
        column = p["column"]
        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        out_col = f"{column}_ema_{span}"
        res = df.copy()
        res[out_col] = calculate_ema(df[column], span)
        return res

class WMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="wma",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Weighted Moving Average",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "column": "close"},
            produces=["{column}_wma_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "volume", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        column = p["column"]
        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        out_col = f"{column}_wma_{window}"
        res = df.copy()
        res[out_col] = calculate_wma(df[column], window)
        return res

class DEMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="dema",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Double Exponential Moving Average",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"span": 20, "column": "close"},
            produces=["{column}_dema_{span}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="span", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "volume", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        span = p["span"]
        column = p["column"]
        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        out_col = f"{column}_dema_{span}"
        res = df.copy()
        res[out_col] = calculate_dema(df[column], span)
        return res

class TEMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="tema",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Triple Exponential Moving Average",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"span": 20, "column": "close"},
            produces=["{column}_tema_{span}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="span", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "volume", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        span = p["span"]
        column = p["column"]
        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        out_col = f"{column}_tema_{span}"
        res = df.copy()
        res[out_col] = calculate_tema(df[column], span)
        return res

class MACDIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="macd",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Moving Average Convergence Divergence",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={"fast": 12, "slow": 26, "signal": 9},
            produces=["macd_{fast}_{slow}_{signal}", "macd_signal_{fast}_{slow}_{signal}", "macd_hist_{fast}_{slow}_{signal}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="fast", param_type="int", default=12, min_value=2, max_value=100),
                IndicatorParameterSpec(name="slow", param_type="int", default=26, min_value=3, max_value=200),
                IndicatorParameterSpec(name="signal", param_type="int", default=9, min_value=2, max_value=100)
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        fast = p["fast"]
        slow = p["slow"]
        signal = p["signal"]

        try:
            validate_macd_params(fast, slow, signal)
        except IndicatorParameterError as e:
            raise IndicatorParameterError(str(e))

        if "close" not in df.columns:
            raise FeatureComputationError("Missing required column: close")

        res = df.copy()
        macd_df = calculate_macd(df["close"], fast, slow, signal)

        for col in macd_df.columns:
            res[col] = macd_df[col]

        return res

class PriceDistanceToMAIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="price_distance_to_ma",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Price distance to Moving Average in Percentage",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"ma_type": "ema", "window": 20, "price_column": "close"},
            produces=["{price_column}_distance_pct_{ma_type}_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="ma_type", param_type="str", default="ema", allowed_values=["sma", "ema", "wma", "dema", "tema"]),
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="price_column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        ma_type = p["ma_type"]
        window = p["window"]
        price_column = p["price_column"]

        if price_column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {price_column}")

        if ma_type == "sma":
            ma_series = calculate_sma(df[price_column], window)
        elif ma_type == "ema":
            ma_series = calculate_ema(df[price_column], window)
        elif ma_type == "wma":
            ma_series = calculate_wma(df[price_column], window)
        elif ma_type == "dema":
            ma_series = calculate_dema(df[price_column], window)
        elif ma_type == "tema":
            ma_series = calculate_tema(df[price_column], window)
        else:
            raise IndicatorParameterError(f"Unsupported ma_type: {ma_type}")

        out_col = f"{price_column}_distance_pct_{ma_type}_{window}"
        res = df.copy()
        res[out_col] = calculate_price_distance_pct(df[price_column], ma_series)
        return res

class MASlopeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="ma_slope",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Slope of Moving Average",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"ma_type": "ema", "window": 20, "slope_window": 5, "column": "close"},
            produces=["{column}_{ma_type}_{window}_slope_{slope_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="ma_type", param_type="str", default="ema", allowed_values=["sma", "ema", "wma", "dema", "tema"]),
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="slope_window", param_type="int", default=5, min_value=1, max_value=100),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        ma_type = p["ma_type"]
        window = p["window"]
        slope_window = p["slope_window"]
        column = p["column"]

        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        if ma_type == "sma":
            ma_series = calculate_sma(df[column], window)
        elif ma_type == "ema":
            ma_series = calculate_ema(df[column], window)
        elif ma_type == "wma":
            ma_series = calculate_wma(df[column], window)
        elif ma_type == "dema":
            ma_series = calculate_dema(df[column], window)
        elif ma_type == "tema":
            ma_series = calculate_tema(df[column], window)
        else:
            raise IndicatorParameterError(f"Unsupported ma_type: {ma_type}")

        out_col = f"{column}_{ma_type}_{window}_slope_{slope_window}"
        res = df.copy()
        res[out_col] = calculate_series_slope(ma_series, slope_window)
        return res

class MAAlignmentIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="ma_alignment",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Moving Average Alignment",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"ma_type": "ema", "short_window": 20, "medium_window": 50, "long_window": 200, "column": "close"},
            produces=["{column}_{ma_type}_alignment_{short_window}_{medium_window}_{long_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="ma_type", param_type="str", default="ema", allowed_values=["sma", "ema"]),
                IndicatorParameterSpec(name="short_window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="medium_window", param_type="int", default=50, min_value=2, max_value=500),
                IndicatorParameterSpec(name="long_window", param_type="int", default=200, min_value=2, max_value=500),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        ma_type = p["ma_type"]
        short_w = p["short_window"]
        med_w = p["medium_window"]
        long_w = p["long_window"]
        column = p["column"]

        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        if ma_type == "sma":
            short_ma = calculate_sma(df[column], short_w)
            med_ma = calculate_sma(df[column], med_w)
            long_ma = calculate_sma(df[column], long_w)
        elif ma_type == "ema":
            short_ma = calculate_ema(df[column], short_w)
            med_ma = calculate_ema(df[column], med_w)
            long_ma = calculate_ema(df[column], long_w)
        else:
            raise IndicatorParameterError(f"Unsupported ma_type: {ma_type}")

        out_col = f"{column}_{ma_type}_alignment_{short_w}_{med_w}_{long_w}"
        res = df.copy()
        res[out_col] = calculate_ma_alignment_score({
            "short": short_ma, "medium": med_ma, "long": long_ma
        })
        return res

class TrendStrengthBasicIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="trend_strength_basic",
            version="1.0",
            category=IndicatorCategory.TREND,
            description="Basic Trend Strength",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"fast_window": 20, "slow_window": 50, "slope_window": 5, "column": "close"},
            produces=["trend_strength_basic_{fast_window}_{slow_window}_{slope_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="fast_window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="slow_window", param_type="int", default=50, min_value=2, max_value=500),
                IndicatorParameterSpec(name="slope_window", param_type="int", default=5, min_value=1, max_value=100),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["open", "high", "low", "close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        fast_w = p["fast_window"]
        slow_w = p["slow_window"]
        slope_w = p["slope_window"]
        column = p["column"]

        if column not in df.columns:
            raise FeatureComputationError(f"Missing required column: {column}")

        fast_ema = calculate_ema(df[column], fast_w)
        slow_ema = calculate_ema(df[column], slow_w)

        # Percentage difference between fast and slow
        diff_pct = calculate_price_distance_pct(fast_ema, slow_ema)

        # Slope of fast ema
        fast_slope = calculate_series_slope(fast_ema, slope_w)

        out_col = f"trend_strength_basic_{fast_w}_{slow_w}_{slope_w}"
        res = df.copy()
        res[out_col] = diff_pct * fast_slope # combination of difference and slope

        return res
