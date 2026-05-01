import pandas as pd
from typing import Dict, Any
from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema, IndicatorParameterSpec
from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType
from usa_signal_bot.core.exceptions import IndicatorParameterError, FeatureComputationError
from usa_signal_bot.features.momentum_utils import (calculate_rsi, calculate_stochastic_k, calculate_stochastic_d, calculate_roc, calculate_momentum, calculate_williams_r, calculate_cci, calculate_momentum_slope, calculate_momentum_acceleration, normalize_oscillator_0_100, validate_momentum_window, validate_stochastic_params)

class RSIIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="rsi", version="1.0", category=IndicatorCategory.MOMENTUM, description="RSI", required_columns=["close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"window": 14, "column": "close"}, produces=["{column}_rsi_{window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("rsi", [IndicatorParameterSpec("window", "int", 14, min_value=2, max_value=100), IndicatorParameterSpec("column", "str", "close", allowed_values=["close", "adjusted_close"])])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        validate_momentum_window(params["window"], "window", 2, 100)
        if params["column"] not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        out[f"{params['column']}_rsi_{params['window']}"] = calculate_rsi(df[params["column"]], params["window"])
        return out

class StochasticIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="stochastic", version="1.0", category=IndicatorCategory.MOMENTUM, description="Stochastic", required_columns=["high", "low", "close"], min_bars=2, output_type=IndicatorOutputType.MULTI_SERIES, default_params={"k_window": 14, "d_window": 3}, produces=["stoch_k_{k_window}", "stoch_d_{k_window}_{d_window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("stochastic", [IndicatorParameterSpec("k_window", "int", 14, min_value=2, max_value=100), IndicatorParameterSpec("d_window", "int", 3, min_value=1, max_value=50)])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        validate_stochastic_params(params["k_window"], params["d_window"])
        for c in ["high", "low", "close"]:
            if c not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        out[f"stoch_k_{params['k_window']}"] = calculate_stochastic_k(df["high"], df["low"], df["close"], params["k_window"])
        out[f"stoch_d_{params['k_window']}_{params['d_window']}"] = calculate_stochastic_d(out[f"stoch_k_{params['k_window']}"], params["d_window"])
        return out

class ROCIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="roc", version="1.0", category=IndicatorCategory.MOMENTUM, description="ROC", required_columns=["close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"window": 12, "column": "close"}, produces=["{column}_roc_{window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("roc", [IndicatorParameterSpec("window", "int", 12, min_value=1, max_value=252), IndicatorParameterSpec("column", "str", "close", allowed_values=["close", "adjusted_close"])])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        validate_momentum_window(params["window"], "window", 1, 252)
        if params["column"] not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        out[f"{params['column']}_roc_{params['window']}"] = calculate_roc(df[params["column"]], params["window"])
        return out

class MomentumIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="momentum", version="1.0", category=IndicatorCategory.MOMENTUM, description="Momentum", required_columns=["close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"window": 10, "column": "close"}, produces=["{column}_momentum_{window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("momentum", [IndicatorParameterSpec("window", "int", 10, min_value=1, max_value=252), IndicatorParameterSpec("column", "str", "close", allowed_values=["close", "adjusted_close"])])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        validate_momentum_window(params["window"], "window", 1, 252)
        if params["column"] not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        out[f"{params['column']}_momentum_{params['window']}"] = calculate_momentum(df[params["column"]], params["window"])
        return out

class WilliamsRIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="williams_r", version="1.0", category=IndicatorCategory.MOMENTUM, description="Williams %R", required_columns=["high", "low", "close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"window": 14}, produces=["williams_r_{window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("williams_r", [IndicatorParameterSpec("window", "int", 14, min_value=2, max_value=100)])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        validate_momentum_window(params["window"], "window", 2, 100)
        for c in ["high", "low", "close"]:
            if c not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        out[f"williams_r_{params['window']}"] = calculate_williams_r(df["high"], df["low"], df["close"], params["window"])
        return out

class CCIIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="cci", version="1.0", category=IndicatorCategory.MOMENTUM, description="CCI", required_columns=["high", "low", "close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"window": 20, "constant": 0.015}, produces=["cci_{window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("cci", [IndicatorParameterSpec("window", "int", 20, min_value=2, max_value=200), IndicatorParameterSpec("constant", "float", 0.015, min_value=0.001, max_value=1.0)])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        validate_momentum_window(params["window"], "window", 2, 200)
        for c in ["high", "low", "close"]:
            if c not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        out[f"cci_{params['window']}"] = calculate_cci(df["high"], df["low"], df["close"], params["window"], params["constant"])
        return out

class MomentumSlopeIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="momentum_slope", version="1.0", category=IndicatorCategory.MOMENTUM, description="Momentum Slope", required_columns=["close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"base_indicator": "rsi", "window": 14, "slope_window": 5, "column": "close"}, produces=["{base_indicator}_{window}_slope_{slope_window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("momentum_slope", [IndicatorParameterSpec("base_indicator", "str", "rsi", allowed_values=["rsi", "roc", "momentum"]), IndicatorParameterSpec("window", "int", 14, min_value=2, max_value=252), IndicatorParameterSpec("slope_window", "int", 5, min_value=1, max_value=100), IndicatorParameterSpec("column", "str", "close", allowed_values=["close", "adjusted_close"])])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        base = params.get("base_indicator", "rsi")
        window = params.get("window", 14)
        slope_window = params.get("slope_window", 5)
        column = params.get("column", "close")
        if column not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        if base == "rsi": base_s = calculate_rsi(df[column], window)
        elif base == "roc": base_s = calculate_roc(df[column], window)
        else: base_s = calculate_momentum(df[column], window)
        out[f"{base}_{window}_slope_{slope_window}"] = calculate_momentum_slope(base_s, slope_window)
        return out

class MomentumAccelerationIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="momentum_acceleration", version="1.0", category=IndicatorCategory.MOMENTUM, description="Momentum Accel", required_columns=["close"], min_bars=2, output_type=IndicatorOutputType.SERIES, default_params={"base_indicator": "roc", "window": 12, "slope_window": 5, "column": "close"}, produces=["{base_indicator}_{window}_acceleration_{slope_window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("momentum_acceleration", [IndicatorParameterSpec("base_indicator", "str", "roc", allowed_values=["rsi", "roc", "momentum"]), IndicatorParameterSpec("window", "int", 12, min_value=2, max_value=252), IndicatorParameterSpec("slope_window", "int", 5, min_value=1, max_value=100), IndicatorParameterSpec("column", "str", "close", allowed_values=["close", "adjusted_close"])])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        base = params.get("base_indicator", "roc")
        window = params.get("window", 12)
        slope_window = params.get("slope_window", 5)
        column = params.get("column", "close")
        if column not in df.columns: raise FeatureComputationError("Missing column")
        out = df.copy()
        if base == "rsi": base_s = calculate_rsi(df[column], window)
        elif base == "roc": base_s = calculate_roc(df[column], window)
        else: base_s = calculate_momentum(df[column], window)
        out[f"{base}_{window}_acceleration_{slope_window}"] = calculate_momentum_acceleration(base_s, slope_window)
        return out

class NormalizedMomentumIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(name="normalized_momentum", version="1.0", category=IndicatorCategory.MOMENTUM, description="Norm Mom", required_columns=["close"], min_bars=10, output_type=IndicatorOutputType.SERIES, default_params={"window": 20, "normalization_window": 100, "column": "close"}, produces=["{column}_normalized_momentum_{window}_{normalization_window}"])
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("normalized_momentum", [IndicatorParameterSpec("window", "int", 20, min_value=2, max_value=252), IndicatorParameterSpec("normalization_window", "int", 100, min_value=10, max_value=500), IndicatorParameterSpec("column", "str", "close", allowed_values=["close", "adjusted_close"])])
    def compute(self, df: pd.DataFrame, params: Dict[str, Any] = None) -> pd.DataFrame:
        params = params or self.metadata.default_params
        w = params.get("window", 20)
        nw = params.get("normalization_window", 100)
        c = params.get("column", "close")
        if c not in df.columns: raise FeatureComputationError("Missing col")
        out = df.copy()
        raw = calculate_momentum(df[c], w)
        r_min = raw.rolling(nw).min()
        r_max = raw.rolling(nw).max()
        diff = (r_max - r_min).replace(0, 1)
        out[f"{c}_normalized_momentum_{w}_{nw}"] = ((raw - r_min) / diff) * 100.0
        return out
