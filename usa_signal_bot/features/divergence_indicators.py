import pandas as pd
from typing import Dict, Any, List

from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType, DivergenceSource, DivergenceConfirmationMode
from usa_signal_bot.core.exceptions import FeatureComputationError, IndicatorParameterError
from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec

from usa_signal_bot.features.momentum_utils import calculate_rsi, calculate_roc
from usa_signal_bot.features.trend_utils import calculate_macd
from usa_signal_bot.features.volume_utils import calculate_money_flow_index as calculate_mfi, calculate_obv
from usa_signal_bot.features.divergence_utils import (
    find_confirmed_pivot_highs, find_confirmed_pivot_lows,
    find_left_only_pivot_highs, find_left_only_pivot_lows,
    detect_regular_bullish_divergence, detect_regular_bearish_divergence,
    detect_hidden_bullish_divergence, detect_hidden_bearish_divergence,
    build_divergence_feature_series, validate_divergence_windows
)

class BaseDivergenceIndicator(Indicator):
    def _compute_divergence(
        self,
        df: pd.DataFrame,
        price_series: pd.Series,
        osc_series: pd.Series,
        source: DivergenceSource,
        prefix: str,
        left_window: int,
        right_window: int,
        max_pivot_distance: int,
        confirmation_mode: str
    ) -> pd.DataFrame:

        validate_divergence_windows(left_window, right_window, max_pivot_distance)

        if confirmation_mode == "confirmed_pivot":
            price_highs = find_confirmed_pivot_highs(price_series, left_window, right_window)
            price_lows = find_confirmed_pivot_lows(price_series, left_window, right_window)
            osc_highs = find_confirmed_pivot_highs(osc_series, left_window, right_window)
            osc_lows = find_confirmed_pivot_lows(osc_series, left_window, right_window)
        elif confirmation_mode == "left_only_pivot":
            price_highs = find_left_only_pivot_highs(price_series, left_window)
            price_lows = find_left_only_pivot_lows(price_series, left_window)
            osc_highs = find_left_only_pivot_highs(osc_series, left_window)
            osc_lows = find_left_only_pivot_lows(osc_series, left_window)
        else:
            raise IndicatorParameterError(f"Unsupported confirmation mode: {confirmation_mode}")

        reg_bull = detect_regular_bullish_divergence(price_lows, osc_lows, source, max_pivot_distance)
        reg_bear = detect_regular_bearish_divergence(price_highs, osc_highs, source, max_pivot_distance)
        hid_bull = detect_hidden_bullish_divergence(price_lows, osc_lows, source, max_pivot_distance)
        hid_bear = detect_hidden_bearish_divergence(price_highs, osc_highs, source, max_pivot_distance)

        mode_enum = DivergenceConfirmationMode.CONFIRMED_PIVOT if confirmation_mode == "confirmed_pivot" else DivergenceConfirmationMode.LEFT_ONLY_PIVOT
        all_pairs = reg_bull + reg_bear + hid_bull + hid_bear
        for p in all_pairs:
            p.confirmation_mode = mode_enum

        return build_divergence_feature_series(df, all_pairs, prefix)

class RSIDivergenceIndicator(BaseDivergenceIndicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="rsi_divergence",
            version="1.0",
            category=IndicatorCategory.MOMENTUM,
            description="Detects RSI divergences (regular and hidden)",
            required_columns=["close"],
            min_bars=20,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={
                "rsi_window": 14, "left_window": 2, "right_window": 2,
                "max_pivot_distance": 5, "confirmation_mode": "confirmed_pivot"
            },
            produces=[
                "rsi_regular_bullish_divergence", "rsi_regular_bearish_divergence",
                "rsi_hidden_bullish_divergence", "rsi_hidden_bearish_divergence",
                "rsi_divergence_strength", "rsi_latest_divergence_code"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="rsi_window", param_type="int", default=14, min_value=2, max_value=100),
                IndicatorParameterSpec(name="left_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="right_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="max_pivot_distance", param_type="int", default=5, min_value=0, max_value=50),
                IndicatorParameterSpec(name="confirmation_mode", param_type="str", default="confirmed_pivot", allowed_values=["confirmed_pivot", "left_only_pivot"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        if "close" not in df.columns:
            raise FeatureComputationError("Missing required column: close")

        rsi = calculate_rsi(df["close"], p["rsi_window"])

        return self._compute_divergence(
            df, df["close"], rsi, DivergenceSource.RSI, "rsi",
            p["left_window"], p["right_window"], p["max_pivot_distance"], p["confirmation_mode"]
        )

class MACDHistogramDivergenceIndicator(BaseDivergenceIndicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="macd_hist_divergence",
            version="1.0",
            category=IndicatorCategory.MOMENTUM,
            description="Detects MACD Histogram divergences",
            required_columns=["close"],
            min_bars=35,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={
                "fast": 12, "slow": 26, "signal": 9,
                "left_window": 2, "right_window": 2, "max_pivot_distance": 5,
                "confirmation_mode": "confirmed_pivot"
            },
            produces=[
                "macd_hist_regular_bullish_divergence", "macd_hist_regular_bearish_divergence",
                "macd_hist_hidden_bullish_divergence", "macd_hist_hidden_bearish_divergence",
                "macd_hist_divergence_strength", "macd_hist_latest_divergence_code"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="fast", param_type="int", default=12, min_value=2, max_value=100),
                IndicatorParameterSpec(name="slow", param_type="int", default=26, min_value=3, max_value=200),
                IndicatorParameterSpec(name="signal", param_type="int", default=9, min_value=2, max_value=100),
                IndicatorParameterSpec(name="left_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="right_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="max_pivot_distance", param_type="int", default=5, min_value=0, max_value=50),
                IndicatorParameterSpec(name="confirmation_mode", param_type="str", default="confirmed_pivot", allowed_values=["confirmed_pivot", "left_only_pivot"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        if "close" not in df.columns:
            raise FeatureComputationError("Missing required column: close")

        macd_df = calculate_macd(df["close"], p["fast"], p["slow"], p["signal"])
        macd_hist = macd_df[f"macd_hist_{p['fast']}_{p['slow']}_{p['signal']}"]

        return self._compute_divergence(
            df, df["close"], macd_hist, DivergenceSource.MACD_HIST, "macd_hist",
            p["left_window"], p["right_window"], p["max_pivot_distance"], p["confirmation_mode"]
        )

class ROCDivergenceIndicator(BaseDivergenceIndicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="roc_divergence",
            version="1.0",
            category=IndicatorCategory.MOMENTUM,
            description="Detects Rate of Change (ROC) divergences",
            required_columns=["close"],
            min_bars=20,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={
                "roc_window": 12, "left_window": 2, "right_window": 2,
                "max_pivot_distance": 5, "confirmation_mode": "confirmed_pivot"
            },
            produces=[
                "roc_regular_bullish_divergence", "roc_regular_bearish_divergence",
                "roc_hidden_bullish_divergence", "roc_hidden_bearish_divergence",
                "roc_divergence_strength", "roc_latest_divergence_code"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="roc_window", param_type="int", default=12, min_value=1, max_value=252),
                IndicatorParameterSpec(name="left_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="right_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="max_pivot_distance", param_type="int", default=5, min_value=0, max_value=50),
                IndicatorParameterSpec(name="confirmation_mode", param_type="str", default="confirmed_pivot", allowed_values=["confirmed_pivot", "left_only_pivot"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        if "close" not in df.columns:
            raise FeatureComputationError("Missing required column: close")

        roc = calculate_roc(df["close"], p["roc_window"])

        return self._compute_divergence(
            df, df["close"], roc, DivergenceSource.ROC, "roc",
            p["left_window"], p["right_window"], p["max_pivot_distance"], p["confirmation_mode"]
        )

class MFIDivergenceIndicator(BaseDivergenceIndicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="mfi_divergence",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Detects Money Flow Index (MFI) divergences",
            required_columns=["high", "low", "close", "volume"],
            min_bars=20,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={
                "mfi_window": 14, "left_window": 2, "right_window": 2,
                "max_pivot_distance": 5, "confirmation_mode": "confirmed_pivot"
            },
            produces=[
                "mfi_regular_bullish_divergence", "mfi_regular_bearish_divergence",
                "mfi_hidden_bullish_divergence", "mfi_hidden_bearish_divergence",
                "mfi_divergence_strength", "mfi_latest_divergence_code"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="mfi_window", param_type="int", default=14, min_value=2, max_value=100),
                IndicatorParameterSpec(name="left_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="right_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="max_pivot_distance", param_type="int", default=5, min_value=0, max_value=50),
                IndicatorParameterSpec(name="confirmation_mode", param_type="str", default="confirmed_pivot", allowed_values=["confirmed_pivot", "left_only_pivot"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        for col in self.metadata.required_columns:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        mfi = calculate_mfi(df["high"], df["low"], df["close"], df["volume"], p["mfi_window"])

        return self._compute_divergence(
            df, df["close"], mfi, DivergenceSource.MFI, "mfi",
            p["left_window"], p["right_window"], p["max_pivot_distance"], p["confirmation_mode"]
        )

class OBVDivergenceIndicator(BaseDivergenceIndicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="obv_divergence",
            version="1.0",
            category=IndicatorCategory.VOLUME,
            description="Detects On-Balance Volume (OBV) divergences",
            required_columns=["close", "volume"],
            min_bars=20,
            output_type=IndicatorOutputType.MULTI_SERIES,
            default_params={
                "left_window": 2, "right_window": 2, "max_pivot_distance": 5,
                "confirmation_mode": "confirmed_pivot"
            },
            produces=[
                "obv_regular_bullish_divergence", "obv_regular_bearish_divergence",
                "obv_hidden_bullish_divergence", "obv_hidden_bearish_divergence",
                "obv_divergence_strength", "obv_latest_divergence_code"
            ]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(
            indicator_name=self.metadata.name,
            parameters=[
                IndicatorParameterSpec(name="left_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="right_window", param_type="int", default=2, min_value=1, max_value=20),
                IndicatorParameterSpec(name="max_pivot_distance", param_type="int", default=5, min_value=0, max_value=50),
                IndicatorParameterSpec(name="confirmation_mode", param_type="str", default="confirmed_pivot", allowed_values=["confirmed_pivot", "left_only_pivot"])
            ]
        )

    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        p = self.validate_params(params)
        for col in self.metadata.required_columns:
            if col not in df.columns:
                raise FeatureComputationError(f"Missing required column: {col}")

        obv = calculate_obv(df["close"], df["volume"])

        return self._compute_divergence(
            df, df["close"], obv, DivergenceSource.OBV, "obv",
            p["left_window"], p["right_window"], p["max_pivot_distance"], p["confirmation_mode"]
        )
