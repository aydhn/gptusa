import pandas as pd
from typing import Any, Dict, List
import datetime, hashlib, json
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import StrategyBenchmarkAlignment, StrategyBenchmarkAlignedPoint, BenchmarkReturnSeries, BenchmarkKind, create_strategy_benchmark_alignment_id, create_strategy_benchmark_aligned_point_id
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_return_series import benchmark_return_series_to_dataframe
def align_strategy_and_benchmark_returns(strategy_return_df: pd.DataFrame, benchmark_series: BenchmarkReturnSeries, run_id: str) -> StrategyBenchmarkAlignment:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    alignment_id = create_strategy_benchmark_alignment_id()
    bm_df = benchmark_return_series_to_dataframe(benchmark_series)
    strategy_return_df["timestamp"] = strategy_return_df["timestamp"].astype(str)
    bm_df["timestamp"] = bm_df["timestamp"].astype(str)
    merged_df = pd.merge(strategy_return_df, bm_df, on="timestamp", how="inner")
    aligned_points = []
    for row in merged_df.to_dict("records"):
        s_ret = row.get("simple_return")
        b_ret = row.get("benchmark_simple_return")
        exc = (s_ret - b_ret) if s_ret is not None and b_ret is not None else None
        aligned_points.append(StrategyBenchmarkAlignedPoint(
            point_id=create_strategy_benchmark_aligned_point_id(), created_at_utc=now_utc,
            run_id=run_id, benchmark_id=benchmark_series.benchmark_id, benchmark_kind=benchmark_series.benchmark_kind,
            timestamp=str(row["timestamp"]), strategy_equity=float(row.get("simulated_equity", 0.0)),
            benchmark_equity=float(row.get("simulated_benchmark_equity", 0.0)),
            strategy_return=s_ret, strategy_cumulative_return=row.get("cumulative_return"),
            benchmark_return=b_ret, benchmark_cumulative_return=row.get("benchmark_cumulative_return"),
            excess_return=exc, tracking_difference=exc, aligned=True
        ))
    alg = StrategyBenchmarkAlignment(alignment_id=alignment_id, created_at_utc=now_utc, run_id=run_id, benchmark_id=benchmark_series.benchmark_id, benchmark_kind=benchmark_series.benchmark_kind, aligned_points=aligned_points, row_count=len(aligned_points), coverage_ratio=len(merged_df)/len(strategy_return_df) if len(strategy_return_df) > 0 else 0, alignment_valid=True)
    return alg
def strategy_benchmark_alignment_to_dataframe(alg: StrategyBenchmarkAlignment) -> pd.DataFrame: return pd.DataFrame()
def strategy_benchmark_alignment_to_text(alg: StrategyBenchmarkAlignment, limit=300) -> str: return "alignment"
