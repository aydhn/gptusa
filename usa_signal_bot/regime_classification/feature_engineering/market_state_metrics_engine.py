from typing import Any
try:
    import pandas as pd
except ImportError:
    pass
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import MarketStateMetricSpec, MarketStateMetricResult, MarketStateMetricKind, RegimeFeatureQuality

def compute_market_state_metric(df, spec: MarketStateMetricSpec):
    if spec.metric_kind == MarketStateMetricKind.MARKET_RETURN_CONTEXT and "close" in df.columns:
        return df["close"].pct_change(spec.window or 20)
    elif spec.metric_kind == MarketStateMetricKind.MARKET_VOLATILITY_CONTEXT and "close" in df.columns:
        return df["close"].pct_change().rolling(spec.window or 20).std()
    return pd.Series(0.0, index=df.index)

def add_market_state_metrics(df, specs: list[MarketStateMetricSpec] | None = None) -> tuple[Any, list[MarketStateMetricResult]]:
    if specs is None:
        from usa_signal_bot.regime_classification.feature_engineering.market_state_metric_specs import build_default_market_state_metric_specs
        specs = build_default_market_state_metric_specs()
    results = []
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and len(df) > 0 else None
    for spec in specs:
        series = compute_market_state_metric(df, spec)
        df[spec.output_column] = series
        res = MarketStateMetricResult(symbol=symbol, metric_name=spec.metric_name, metric_kind=spec.metric_kind, output_column=spec.output_column)
        results.append(res)
    return df, results
