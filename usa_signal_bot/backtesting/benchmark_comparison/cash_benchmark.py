import pandas as pd
from typing import Any, Dict, List
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkReturnSeries, PassiveBenchmarkConfig, BenchmarkKind, create_benchmark_return_series_id
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_return_series import build_benchmark_curve_points_from_equity, compute_benchmark_return_series_hash
def build_cash_benchmark_series(strategy_equity_df: pd.DataFrame, config: PassiveBenchmarkConfig) -> BenchmarkReturnSeries:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    series_id = create_benchmark_return_series_id()
    if strategy_equity_df.empty: return BenchmarkReturnSeries(series_id=series_id, created_at_utc=now_utc, benchmark_id=config.config_id, benchmark_kind=BenchmarkKind.CASH_BASELINE, errors=["empty"])
    df = strategy_equity_df.copy().sort_values(by="timestamp").reset_index(drop=True)
    df["simulated_benchmark_equity"] = [config.initial_cash] * len(df)
    points = build_benchmark_curve_points_from_equity(config.config_id, BenchmarkKind.CASH_BASELINE, df)
    s = BenchmarkReturnSeries(series_id=series_id, created_at_utc=now_utc, benchmark_id=config.config_id, benchmark_kind=BenchmarkKind.CASH_BASELINE, points=points, row_count=len(points), series_valid=True)
    s.series_hash = compute_benchmark_return_series_hash(s)
    return s
