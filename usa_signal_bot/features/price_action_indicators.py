import pandas as pd
import numpy as np
from typing import Dict, Any

from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec
from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType, CandleDirection, BarPatternType, SwingPointType, MarketStructureState

from usa_signal_bot.features.price_action_utils import (
    calculate_candle_body, calculate_candle_body_pct, calculate_full_range, calculate_full_range_pct,
    calculate_upper_wick, calculate_lower_wick, calculate_upper_wick_pct, calculate_lower_wick_pct,
    calculate_close_location_value, calculate_gap_pct, calculate_breakout_distance_pct, calculate_breakdown_distance_pct,
    detect_inside_bar, detect_outside_bar, detect_swing_high, detect_swing_low,
    calculate_higher_high, calculate_lower_low, calculate_range_expansion, calculate_range_contraction, safe_divide
)

class CandleFeaturesIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="candle_features",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Calculates basic candle body and range features",
            required_columns=["open", "high", "low", "close"],
            default_params={},
            min_bars=2,
            produces=["candle_body", "candle_body_pct", "full_range", "full_range_pct", "candle_direction_code"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        out = pd.DataFrame(index=data.index)

        out["candle_body"] = calculate_candle_body(data["open"], data["close"])
        out["candle_body_pct"] = calculate_candle_body_pct(data["open"], data["close"])
        out["full_range"] = calculate_full_range(data["high"], data["low"])
        out["full_range_pct"] = calculate_full_range_pct(data["high"], data["low"], data["close"])

        direction = np.sign(data["close"] - data["open"])
        out["candle_direction_code"] = direction.fillna(0).astype(int)

        return out


class WickFeaturesIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="wick_features",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Calculates upper and lower wick features",
            required_columns=["open", "high", "low", "close"],
            default_params={},
            min_bars=1,
            produces=["upper_wick", "lower_wick", "upper_wick_pct", "lower_wick_pct", "wick_imbalance"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        out = pd.DataFrame(index=data.index)

        out["upper_wick"] = calculate_upper_wick(data["open"], data["high"], data["close"])
        out["lower_wick"] = calculate_lower_wick(data["open"], data["low"], data["close"])
        out["upper_wick_pct"] = calculate_upper_wick_pct(data["open"], data["high"], data["close"])
        out["lower_wick_pct"] = calculate_lower_wick_pct(data["open"], data["low"], data["close"])

        total_wick = out["upper_wick"] + out["lower_wick"]
        out["wick_imbalance"] = safe_divide((out["upper_wick"] - out["lower_wick"]), total_wick).fillna(0)

        return out


class CloseLocationValueIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="close_location_value",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.SERIES,
            description="Calculates Close Location Value (CLV)",
            required_columns=["high", "low", "close"],
            default_params={},
            min_bars=1,
            produces=["close_location_value"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        out = pd.DataFrame(index=data.index)
        out["close_location_value"] = calculate_close_location_value(data["high"], data["low"], data["close"])
        return out


class GapFeaturesIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="gap_features",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Calculates opening gap features",
            required_columns=["open", "close"],
            default_params={},
            min_bars=2,
            produces=["gap_pct", "gap_abs_pct", "gap_direction_code"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        out = pd.DataFrame(index=data.index)

        prev_close = data["close"].shift(1)
        out["gap_pct"] = calculate_gap_pct(data["open"], prev_close)
        out["gap_abs_pct"] = out["gap_pct"].abs()

        direction = np.sign(out["gap_pct"])
        out["gap_direction_code"] = direction.fillna(0).astype(int)

        return out


class BreakoutDistanceIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="breakout_distance",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Distance from close to previous rolling high",
            required_columns=["high", "close"],
            default_params={"window": 20},
            min_bars=2,
            produces=["breakout_distance_pct_{window}", "rolling_high_prev_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[
            IndicatorParameterSpec("window", "int", 20, min_value=2, max_value=500)
        ])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        p = self.validate_params(params)
        self.validate_input_frame(data)
        window = p["window"]

        out = pd.DataFrame(index=data.index)
        out[f"breakout_distance_pct_{window}"] = calculate_breakout_distance_pct(data["close"], data["high"], window)
        out[f"rolling_high_prev_{window}"] = data["high"].shift(1).rolling(window=window).max()

        return out


class BreakdownDistanceIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="breakdown_distance",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Distance from close to previous rolling low",
            required_columns=["low", "close"],
            default_params={"window": 20},
            min_bars=2,
            produces=["breakdown_distance_pct_{window}", "rolling_low_prev_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[
            IndicatorParameterSpec("window", "int", 20, min_value=2, max_value=500)
        ])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        p = self.validate_params(params)
        self.validate_input_frame(data)
        window = p["window"]

        out = pd.DataFrame(index=data.index)
        out[f"breakdown_distance_pct_{window}"] = calculate_breakdown_distance_pct(data["close"], data["low"], window)
        out[f"rolling_low_prev_{window}"] = data["low"].shift(1).rolling(window=window).min()

        return out


class InsideOutsideBarIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="inside_outside_bar",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Detects inside and outside bar patterns",
            required_columns=["high", "low"],
            default_params={},
            min_bars=2,
            produces=["inside_bar", "outside_bar", "bar_pattern_code"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        self.validate_input_frame(data)
        out = pd.DataFrame(index=data.index)

        out["inside_bar"] = detect_inside_bar(data["high"], data["low"])
        out["outside_bar"] = detect_outside_bar(data["high"], data["low"])

        out["bar_pattern_code"] = 0
        out.loc[out["inside_bar"] == 1, "bar_pattern_code"] = -1
        out.loc[out["outside_bar"] == 1, "bar_pattern_code"] = 1

        return out


class SwingPointIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="swing_points",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Detects confirmed swing highs and lows (uses right window, involves lookahead)",
            required_columns=["high", "low"],
            default_params={"left_window": 2, "right_window": 2},
            min_bars=3,
            produces=["confirmed_swing_high_{left_window}_{right_window}", "confirmed_swing_low_{left_window}_{right_window}", "swing_point_code_{left_window}_{right_window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[
            IndicatorParameterSpec("left_window", "int", 2, min_value=1, max_value=20),
            IndicatorParameterSpec("right_window", "int", 2, min_value=1, max_value=20)
        ])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        p = self.validate_params(params)
        self.validate_input_frame(data)

        lw = p["left_window"]
        rw = p["right_window"]

        out = pd.DataFrame(index=data.index)
        out[f"confirmed_swing_high_{lw}_{rw}"] = detect_swing_high(data["high"], lw, rw)
        out[f"confirmed_swing_low_{lw}_{rw}"] = detect_swing_low(data["low"], lw, rw)

        code_col = f"swing_point_code_{lw}_{rw}"
        out[code_col] = 0
        out.loc[out[f"confirmed_swing_high_{lw}_{rw}"] == 1, code_col] = 1
        out.loc[out[f"confirmed_swing_low_{lw}_{rw}"] == 1, code_col] = -1

        return out


class MarketStructureIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="market_structure",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Detects market structure based on confirmed swings (HH, LL)",
            required_columns=["high", "low"],
            default_params={"swing_left": 2, "swing_right": 2},
            min_bars=3,
            produces=["higher_high", "lower_low", "structure_state_code"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[
            IndicatorParameterSpec("swing_left", "int", 2, min_value=1, max_value=20),
            IndicatorParameterSpec("swing_right", "int", 2, min_value=1, max_value=20)
        ])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        p = self.validate_params(params)
        self.validate_input_frame(data)

        lw = p["swing_left"]
        rw = p["swing_right"]

        swing_high = detect_swing_high(data["high"], lw, rw)
        swing_low = detect_swing_low(data["low"], lw, rw)

        out = pd.DataFrame(index=data.index)
        out["higher_high"] = calculate_higher_high(data["high"], swing_high)
        out["lower_low"] = calculate_lower_low(data["low"], swing_low)

        out["structure_state_code"] = 0
        out.loc[out["higher_high"] == 1, "structure_state_code"] = 1
        out.loc[out["lower_low"] == 1, "structure_state_code"] = -1

        return out


class RangeExpansionIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="range_expansion",
            version="1.0.0",
            category=IndicatorCategory.PRICE,
            output_type=IndicatorOutputType.MULTI_SERIES,
            description="Calculates range expansion and contraction compared to previous moving average of range",
            required_columns=["high", "low"],
            default_params={"window": 20},
            min_bars=3,
            produces=["range_expansion_{window}", "range_contraction_{window}"]
        )

    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema(indicator_name=self.metadata.name, parameters=[
            IndicatorParameterSpec("window", "int", 20, min_value=2, max_value=500)
        ])

    def compute(self, data: pd.DataFrame, params: Dict[str, Any] | None = None) -> pd.DataFrame:
        p = self.validate_params(params)
        self.validate_input_frame(data)
        window = p["window"]

        out = pd.DataFrame(index=data.index)
        out[f"range_expansion_{window}"] = calculate_range_expansion(data["high"], data["low"], window)
        out[f"range_contraction_{window}"] = calculate_range_contraction(data["high"], data["low"], window)

        return out
