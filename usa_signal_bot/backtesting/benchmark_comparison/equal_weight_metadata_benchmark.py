import pandas as pd
from typing import Any, Dict, List
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkReturnSeries, PassiveBenchmarkConfig, BenchmarkKind, create_benchmark_return_series_id
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_return_series import build_benchmark_curve_points_from_equity, compute_benchmark_return_series_hash
def compute_equal_weight_metadata_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by=["symbol", "timestamp"])
    df["daily_ret"] = df.groupby("symbol")["close"].pct_change().fillna(0)
    ew_df = df.groupby("timestamp")["daily_ret"].mean().reset_index()
    ew_df.rename(columns={"daily_ret": "equal_weight_return"}, inplace=True)
    ew_df["timestamp"] = ew_df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return ew_df
def build_equal_weight_metadata_benchmark_series(price_df: pd.DataFrame, config: PassiveBenchmarkConfig) -> BenchmarkReturnSeries:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    series_id = create_benchmark_return_series_id()
    ew_returns = compute_equal_weight_metadata_returns(price_df)
    current_equity = config.initial_cash
    equity_values = []
    for ret in ew_returns["equal_weight_return"]:
        current_equity = current_equity * (1.0 + ret)
        equity_values.append(current_equity)
    ew_returns["simulated_benchmark_equity"] = equity_values
    points = build_benchmark_curve_points_from_equity(config.config_id, BenchmarkKind.EQUAL_WEIGHT_METADATA, ew_returns)
    s = BenchmarkReturnSeries(series_id=series_id, created_at_utc=now_utc, benchmark_id=config.config_id, benchmark_kind=BenchmarkKind.EQUAL_WEIGHT_METADATA, points=points, row_count=len(points), series_valid=True)
    s.series_hash = compute_benchmark_return_series_hash(s)
    return s
