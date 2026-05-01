import pandas as pd
from typing import Dict, Any

from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec
from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType
from usa_signal_bot.core.exceptions import IndicatorParameterError, FeatureComputationError

from usa_signal_bot.features.volatility_utils import (
    calculate_true_range, calculate_atr, calculate_normalized_atr,
    calculate_bollinger_bands, calculate_bollinger_bandwidth, calculate_bollinger_percent_b,
    calculate_keltner_channels, calculate_donchian_channels, calculate_rolling_volatility,
    calculate_price_range_pct, calculate_body_range_pct, calculate_volatility_compression,
    calculate_volatility_expansion
)

class TrueRangeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="true_range",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="True Range",
            required_columns=["high", "low", "close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={},
            produces=["true_range"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        self.validate_params(params)
        for col in ["high", "low", "close"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res["true_range"] = calculate_true_range(df["high"], df["low"], df["close"])
        return res

class ATRIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="atr",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Average True Range",
            required_columns=["high", "low", "close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 14, "method": "wilder"},
            produces=["atr_{window}_{method}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=14, min_value=2, max_value=252),
                IndicatorParameterSpec(name="method", param_type="str", default="wilder", allowed_values=["wilder", "sma", "ema"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        method = p["method"]
        for col in ["high", "low", "close"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"atr_{window}_{method}"] = calculate_atr(df["high"], df["low"], df["close"], window, method)
        return res

class NormalizedATRIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="normalized_atr",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Normalized ATR",
            required_columns=["high", "low", "close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 14, "method": "wilder"},
            produces=["normalized_atr_{window}_{method}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=14, min_value=2, max_value=252),
                IndicatorParameterSpec(name="method", param_type="str", default="wilder", allowed_values=["wilder", "sma", "ema"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        method = p["method"]
        for col in ["high", "low", "close"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"normalized_atr_{window}_{method}"] = calculate_normalized_atr(df["high"], df["low"], df["close"], window, method)
        return res


class BollingerBandsIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="bollinger_bands",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Bollinger Bands",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={"window": 20, "num_std": 2.0, "column": "close"},
            produces=[
                "{column}_bb_middle_{window}_{num_std}",
                "{column}_bb_upper_{window}_{num_std}",
                "{column}_bb_lower_{window}_{num_std}"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="num_std", param_type="float", default=2.0, min_value=0.1, max_value=10.0),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        num_std = p["num_std"]
        col = p["column"]

        if col not in df.columns:
            raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        num_std_str = str(num_std).replace(".", "p")
        bb_df = calculate_bollinger_bands(df[col], window, num_std)
        res[f"{col}_bb_middle_{window}_{num_std_str}"] = bb_df["middle"]
        res[f"{col}_bb_upper_{window}_{num_std_str}"] = bb_df["upper"]
        res[f"{col}_bb_lower_{window}_{num_std_str}"] = bb_df["lower"]
        return res

class BollingerBandwidthIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="bollinger_bandwidth",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Bollinger Bandwidth",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "num_std": 2.0, "column": "close"},
            produces=["{column}_bb_bandwidth_{window}_{num_std}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="num_std", param_type="float", default=2.0, min_value=0.1, max_value=10.0),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        num_std = p["num_std"]
        col = p["column"]

        if col not in df.columns:
            raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        num_std_str = str(num_std).replace(".", "p")
        bb_df = calculate_bollinger_bands(df[col], window, num_std)
        res[f"{col}_bb_bandwidth_{window}_{num_std_str}"] = calculate_bollinger_bandwidth(bb_df["upper"], bb_df["middle"], bb_df["lower"])
        return res

class BollingerPercentBIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="bollinger_percent_b",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Bollinger %B",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "num_std": 2.0, "column": "close"},
            produces=["{column}_bb_percent_b_{window}_{num_std}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="num_std", param_type="float", default=2.0, min_value=0.1, max_value=10.0),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        num_std = p["num_std"]
        col = p["column"]

        if col not in df.columns:
            raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        num_std_str = str(num_std).replace(".", "p")
        bb_df = calculate_bollinger_bands(df[col], window, num_std)
        res[f"{col}_bb_percent_b_{window}_{num_std_str}"] = calculate_bollinger_percent_b(df[col], bb_df["upper"], bb_df["lower"])
        return res

class KeltnerChannelIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="keltner_channel",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Keltner Channels",
            required_columns=["high", "low", "close"],
            min_bars=2,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={"ema_window": 20, "atr_window": 10, "multiplier": 2.0},
            produces=[
                "keltner_middle_{ema_window}_{atr_window}_{multiplier}",
                "keltner_upper_{ema_window}_{atr_window}_{multiplier}",
                "keltner_lower_{ema_window}_{atr_window}_{multiplier}"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="ema_window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="atr_window", param_type="int", default=10, min_value=2, max_value=252),
                IndicatorParameterSpec(name="multiplier", param_type="float", default=2.0, min_value=0.1, max_value=10.0)
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        ema_window = p["ema_window"]
        atr_window = p["atr_window"]
        multiplier = p["multiplier"]

        for col in ["high", "low", "close"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        kc_df = calculate_keltner_channels(df["high"], df["low"], df["close"], ema_window, atr_window, multiplier)
        multiplier_str = str(multiplier).replace(".", "p")
        res[f"keltner_middle_{ema_window}_{atr_window}_{multiplier_str}"] = kc_df["middle"]
        res[f"keltner_upper_{ema_window}_{atr_window}_{multiplier_str}"] = kc_df["upper"]
        res[f"keltner_lower_{ema_window}_{atr_window}_{multiplier_str}"] = kc_df["lower"]
        return res

class DonchianChannelIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="donchian_channel",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Donchian Channels",
            required_columns=["high", "low"],
            min_bars=2,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={"window": 20},
            produces=[
                "donchian_upper_{window}",
                "donchian_middle_{window}",
                "donchian_lower_{window}"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500)
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]

        for col in ["high", "low"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        dc_df = calculate_donchian_channels(df["high"], df["low"], window)
        res[f"donchian_upper_{window}"] = dc_df["upper"]
        res[f"donchian_middle_{window}"] = dc_df["middle"]
        res[f"donchian_lower_{window}"] = dc_df["lower"]
        return res

class RollingVolatilityIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="rolling_volatility",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Rolling Volatility",
            required_columns=["close"],
            min_bars=2,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "annualize": False, "periods_per_year": 252, "column": "close"},
            produces=["{column}_rolling_volatility_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="annualize", param_type="bool", default=False),
                IndicatorParameterSpec(name="periods_per_year", param_type="int", default=252, min_value=1, max_value=10000),
                IndicatorParameterSpec(name="column", param_type="str", default="close", allowed_values=["close", "adjusted_close"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        annualize = p["annualize"]
        periods_per_year = p["periods_per_year"]
        col = p["column"]

        if col not in df.columns:
            raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res[f"{col}_rolling_volatility_{window}"] = calculate_rolling_volatility(df[col], window, annualize, periods_per_year)
        return res

class PriceRangeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="price_range",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Price Range Percentages",
            required_columns=["open", "high", "low", "close"],
            min_bars=2,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={},
            produces=["high_low_range_pct", "body_range_pct"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        self.validate_params(params)
        for col in ["open", "high", "low", "close"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        res["high_low_range_pct"] = calculate_price_range_pct(df["high"], df["low"], df["close"])
        res["body_range_pct"] = calculate_body_range_pct(df["open"], df["close"], df["high"], df["low"])
        return res

class VolatilityCompressionIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volatility_compression",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Volatility Compression",
            required_columns=["close"],
            min_bars=10,
            output_type=IndicatorOutputType.SERIES,
            default_params={"window": 20, "reference_window": 100, "num_std": 2.0},
            produces=["volatility_compression_{window}_{reference_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="window", param_type="int", default=20, min_value=2, max_value=500),
                IndicatorParameterSpec(name="reference_window", param_type="int", default=100, min_value=10, max_value=1000),
                IndicatorParameterSpec(name="num_std", param_type="float", default=2.0, min_value=0.1, max_value=10.0)
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        window = p["window"]
        ref_window = p["reference_window"]
        num_std = p["num_std"]

        if "close" not in df.columns:
            raise FeatureComputationError("Missing required column: close")

        res = df.copy()
        bb_df = calculate_bollinger_bands(df["close"], window, num_std)
        bandwidth = calculate_bollinger_bandwidth(bb_df["upper"], bb_df["middle"], bb_df["lower"])
        res[f"volatility_compression_{window}_{ref_window}"] = calculate_volatility_compression(bandwidth, ref_window)
        return res

class VolatilityExpansionIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="volatility_expansion",
            version="1.0",
            category=IndicatorCategory.VOLATILITY,
            description="Volatility Expansion",
            required_columns=["high", "low", "close"],
            min_bars=10,
            output_type=IndicatorOutputType.SERIES,
            default_params={"atr_window": 14, "reference_window": 100},
            produces=["volatility_expansion_{atr_window}_{reference_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="atr_window", param_type="int", default=14, min_value=2, max_value=252),
                IndicatorParameterSpec(name="reference_window", param_type="int", default=100, min_value=10, max_value=1000)
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        atr_w = p["atr_window"]
        ref_w = p["reference_window"]

        for col in ["high", "low", "close"]:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        res = df.copy()
        atr = calculate_atr(df["high"], df["low"], df["close"], atr_w)
        res[f"volatility_expansion_{atr_w}_{ref_w}"] = calculate_volatility_expansion(atr, ref_w)
        return res
