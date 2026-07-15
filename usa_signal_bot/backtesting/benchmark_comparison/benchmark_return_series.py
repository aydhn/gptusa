import pandas as pd
from typing import Any, Dict, List, Optional
import datetime, hashlib, json
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import (
    BenchmarkReturnSeries,
    BenchmarkCurvePoint,
    BenchmarkKind,
    create_benchmark_return_series_id,
    create_benchmark_curve_point_id,
)


def compute_benchmark_simple_return(
    current_equity: float, previous_equity: Optional[float]
) -> Optional[float]:
    if previous_equity is None or previous_equity == 0:
        return 0.0
    return (current_equity - previous_equity) / previous_equity


def compute_benchmark_cumulative_return(
    current_equity: float, initial_equity: Optional[float]
) -> Optional[float]:
    if initial_equity is None or initial_equity == 0:
        return 0.0
    return (current_equity - initial_equity) / initial_equity


def build_benchmark_curve_points_from_equity(
    benchmark_id: str, benchmark_kind: BenchmarkKind, equity_df: pd.DataFrame
) -> List[BenchmarkCurvePoint]:
    points = []
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if equity_df.empty:
        return points
    equity_df = equity_df.sort_values(by="timestamp").reset_index(drop=True)
    initial_equity = float(equity_df.loc[0, "simulated_benchmark_equity"])
    prev_equity = None
    for row in equity_df.itertuples(index=False):
        current_equity = float(row.simulated_benchmark_equity)
        points.append(
            BenchmarkCurvePoint(
                point_id=create_benchmark_curve_point_id(),
                created_at_utc=now_utc,
                benchmark_id=benchmark_id,
                benchmark_kind=benchmark_kind,
                timestamp=str(row.timestamp),
                simulated_benchmark_equity=current_equity,
                benchmark_simple_return=compute_benchmark_simple_return(
                    current_equity, prev_equity
                ),
                benchmark_cumulative_return=compute_benchmark_cumulative_return(
                    current_equity, initial_equity
                ),
                benchmark_valid=True,
            )
        )
        prev_equity = current_equity
    return points


def compute_benchmark_return_series_hash(series: BenchmarkReturnSeries) -> str:
    data_to_hash = [
        {"ts": pt.timestamp, "eq": round(pt.simulated_benchmark_equity, 4)}
        for pt in series.points
    ]
    return hashlib.sha256(
        json.dumps(data_to_hash, sort_keys=True).encode("utf-8")
    ).hexdigest()


def benchmark_return_series_to_dataframe(series: BenchmarkReturnSeries) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "timestamp": pt.timestamp,
                "simulated_benchmark_equity": pt.simulated_benchmark_equity,
                "benchmark_simple_return": pt.benchmark_simple_return,
                "benchmark_cumulative_return": pt.benchmark_cumulative_return,
            }
            for pt in series.points
        ]
    )


def validate_benchmark_return_series(series: BenchmarkReturnSeries) -> List[str]:
    return []


def benchmark_return_series_to_text(s: BenchmarkReturnSeries, limit=300) -> str:
    return "series"
