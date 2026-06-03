import pandas as pd
from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkReturnSeries, PassiveBenchmarkConfig, BenchmarkKind, create_benchmark_return_series_id
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_return_series import build_benchmark_curve_points_from_equity, compute_benchmark_return_series_hash
def choose_default_buy_and_hold_symbol(price_df: pd.DataFrame) -> Optional[str]:
    if "symbol" not in price_df.columns: return None
    return sorted(price_df["symbol"].dropna().unique().tolist())[0] if len(price_df) > 0 else None
def build_buy_and_hold_benchmark_series(price_df: pd.DataFrame, config: PassiveBenchmarkConfig, symbol: Optional[str] = None) -> BenchmarkReturnSeries:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    series_id = create_benchmark_return_series_id()
    target = symbol or choose_default_buy_and_hold_symbol(price_df)
    if not target: return BenchmarkReturnSeries(series_id=series_id, created_at_utc=now_utc, benchmark_id=config.config_id, benchmark_kind=BenchmarkKind.BUY_AND_HOLD_SINGLE_ASSET, errors=["no target"])
    df = price_df[price_df["symbol"] == target].copy().sort_values(by="timestamp").reset_index(drop=True)
    initial_price = float(df.loc[0, "close"])
    shares = config.initial_cash / initial_price if initial_price > 0 else 0
    df["simulated_benchmark_equity"] = df["close"] * shares
    points = build_benchmark_curve_points_from_equity(config.config_id, BenchmarkKind.BUY_AND_HOLD_SINGLE_ASSET, df)
    s = BenchmarkReturnSeries(series_id=series_id, created_at_utc=now_utc, benchmark_id=config.config_id, benchmark_kind=BenchmarkKind.BUY_AND_HOLD_SINGLE_ASSET, points=points, row_count=len(points), series_valid=True)
    s.series_hash = compute_benchmark_return_series_hash(s)
    return s
