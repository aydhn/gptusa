try:
    import pandas as pd
except ImportError:
    pass
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureTableResult

def build_regime_feature_table_for_symbol(symbol: str, df, metric_specs=None, feature_specs=None):
    from usa_signal_bot.regime_classification.feature_engineering.market_state_metrics_engine import add_market_state_metrics
    from usa_signal_bot.regime_classification.feature_engineering.rolling_market_state_metrics import add_rolling_market_state_metrics
    from usa_signal_bot.regime_classification.feature_engineering.factor_context_regime_mapper import map_factor_context_to_regime_features
    from usa_signal_bot.regime_classification.feature_engineering.regime_feature_schema_validator import validate_regime_feature_dataframe_schema

    df, _ = add_market_state_metrics(df, metric_specs)
    df = add_rolling_market_state_metrics(df)
    df["cross_sectional_dispersion_context"] = 0.0
    df = map_factor_context_to_regime_features(df, feature_specs)

    res = RegimeFeatureTableResult(symbol=symbol)
    res.schema_valid = len(validate_regime_feature_dataframe_schema(df)) == 0
    return df, res
