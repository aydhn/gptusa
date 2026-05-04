from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import json

from usa_signal_bot.core.enums import BenchmarkComparisonStatus, RelativePerformanceBucket
from usa_signal_bot.backtesting.benchmark_models import BenchmarkEquityCurve, BenchmarkComparisonReport
from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint

@dataclass
class BenchmarkComparisonMetrics:
    benchmark_symbol: str
    benchmark_name: str
    strategy_return_pct: Optional[float]
    benchmark_return_pct: Optional[float]
    excess_return_pct: Optional[float]
    strategy_max_drawdown_pct: Optional[float]
    benchmark_max_drawdown_pct: Optional[float]
    relative_max_drawdown_pct: Optional[float]
    correlation_like: Optional[float]
    beta_like: Optional[float]
    tracking_error_like: Optional[float]
    information_ratio_like: Optional[float]
    relative_bucket: RelativePerformanceBucket
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class BenchmarkComparisonTable:
    strategy_run_id: Optional[str]
    rows: list[BenchmarkComparisonMetrics]
    created_at_utc: str
    status: BenchmarkComparisonStatus
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def align_equity_curves(
    strategy_curve: EquityCurve,
    benchmark_curve: BenchmarkEquityCurve
) -> tuple[list[EquityCurvePoint], list[EquityCurvePoint]]:
    """Aligns two equity curves on matching timestamps."""
    s_dict = {p.timestamp_utc: p for p in strategy_curve.points}
    b_dict = {p.timestamp_utc: p for p in benchmark_curve.points}

    common_ts = sorted(list(set(s_dict.keys()) & set(b_dict.keys())))

    s_aligned = [s_dict[ts] for ts in common_ts]
    b_aligned = [b_dict[ts] for ts in common_ts]

    return s_aligned, b_aligned

def calculate_curve_returns(points: list[EquityCurvePoint]) -> list[float]:
    """Calculates period-to-period returns."""
    returns = []
    for i in range(1, len(points)):
        prev_eq = points[i-1].equity
        curr_eq = points[i].equity
        if prev_eq > 0:
            returns.append((curr_eq - prev_eq) / prev_eq)
        else:
            returns.append(0.0)
    return returns

def calculate_correlation_like(strategy_returns: list[float], benchmark_returns: list[float]) -> Optional[float]:
    if not strategy_returns or len(strategy_returns) != len(benchmark_returns) or len(strategy_returns) < 2:
        return None

    import math
    n = len(strategy_returns)
    sum_s = sum(strategy_returns)
    sum_b = sum(benchmark_returns)
    sum_s_sq = sum(s*s for s in strategy_returns)
    sum_b_sq = sum(b*b for b in benchmark_returns)
    sum_sb = sum(s*b for s, b in zip(strategy_returns, benchmark_returns))

    numerator = n * sum_sb - sum_s * sum_b

    val1 = (n * sum_s_sq - sum_s**2)
    val2 = (n * sum_b_sq - sum_b**2)

    if val1 <= 0 or val2 <= 0:
        return 0.0

    denominator = math.sqrt(val1 * val2)

    if denominator == 0:
        return 0.0
    return numerator / denominator

def calculate_beta_like(strategy_returns: list[float], benchmark_returns: list[float]) -> Optional[float]:
    if not strategy_returns or len(strategy_returns) != len(benchmark_returns) or len(strategy_returns) < 2:
        return None

    import math
    n = len(strategy_returns)
    sum_b = sum(benchmark_returns)
    sum_b_sq = sum(b*b for b in benchmark_returns)
    sum_s = sum(strategy_returns)
    sum_sb = sum(s*b for s, b in zip(strategy_returns, benchmark_returns))

    numerator = n * sum_sb - sum_b * sum_s
    denominator = n * sum_b_sq - sum_b**2

    if denominator == 0:
        return None
    return numerator / denominator

def calculate_tracking_error_like(strategy_returns: list[float], benchmark_returns: list[float]) -> Optional[float]:
    if not strategy_returns or len(strategy_returns) != len(benchmark_returns) or len(strategy_returns) < 2:
        return None

    import math
    excess_returns = [s - b for s, b in zip(strategy_returns, benchmark_returns)]
    mean_excess = sum(excess_returns) / len(excess_returns)
    variance = sum((r - mean_excess)**2 for r in excess_returns) / (len(excess_returns) - 1)

    # Annualization factor assumes daily returns (252 days) - simple proxy
    return math.sqrt(variance) * math.sqrt(252)

def calculate_information_ratio_like(strategy_returns: list[float], benchmark_returns: list[float]) -> Optional[float]:
    if not strategy_returns or len(strategy_returns) != len(benchmark_returns) or len(strategy_returns) < 2:
        return None

    import math
    excess_returns = [s - b for s, b in zip(strategy_returns, benchmark_returns)]
    mean_excess = sum(excess_returns) / len(excess_returns)

    tracking_error = calculate_tracking_error_like(strategy_returns, benchmark_returns)

    if tracking_error is None or tracking_error == 0:
        return None

    # Annualized mean excess
    return (mean_excess * 252) / tracking_error

def compare_strategy_to_benchmark(
    strategy_curve: EquityCurve,
    benchmark_curve: BenchmarkEquityCurve,
    strategy_run_id: Optional[str] = None
) -> BenchmarkComparisonMetrics:
    warnings = []
    errors = []

    s_aligned, b_aligned = align_equity_curves(strategy_curve, benchmark_curve)

    if not s_aligned:
        return BenchmarkComparisonMetrics(
            benchmark_symbol=benchmark_curve.benchmark.symbol,
            benchmark_name=benchmark_curve.benchmark.name,
            strategy_return_pct=None, benchmark_return_pct=None, excess_return_pct=None,
            strategy_max_drawdown_pct=None, benchmark_max_drawdown_pct=None, relative_max_drawdown_pct=None,
            correlation_like=None, beta_like=None, tracking_error_like=None, information_ratio_like=None,
            relative_bucket=RelativePerformanceBucket.INSUFFICIENT_DATA,
            warnings=warnings, errors=["No common timestamps for comparison"]
        )

    s_ret = ((s_aligned[-1].equity - s_aligned[0].equity) / s_aligned[0].equity) * 100.0 if s_aligned[0].equity > 0 else 0.0
    b_ret = ((b_aligned[-1].equity - b_aligned[0].equity) / b_aligned[0].equity) * 100.0 if b_aligned[0].equity > 0 else 0.0
    excess_ret = s_ret - b_ret

    if s_ret > b_ret + 0.01:
        bucket = RelativePerformanceBucket.OUTPERFORMED
    elif s_ret < b_ret - 0.01:
        bucket = RelativePerformanceBucket.UNDERPERFORMED
    else:
        bucket = RelativePerformanceBucket.MATCHED

    s_max_dd = max([p.drawdown_pct for p in s_aligned]) * 100.0 if s_aligned else 0.0
    b_max_dd = max([p.drawdown_pct for p in b_aligned]) * 100.0 if b_aligned else 0.0
    rel_dd = s_max_dd - b_max_dd

    s_period_returns = calculate_curve_returns(s_aligned)
    b_period_returns = calculate_curve_returns(b_aligned)

    corr = calculate_correlation_like(s_period_returns, b_period_returns)
    beta = calculate_beta_like(s_period_returns, b_period_returns)
    te = calculate_tracking_error_like(s_period_returns, b_period_returns)
    ir = calculate_information_ratio_like(s_period_returns, b_period_returns)

    return BenchmarkComparisonMetrics(
        benchmark_symbol=benchmark_curve.benchmark.symbol,
        benchmark_name=benchmark_curve.benchmark.name,
        strategy_return_pct=s_ret,
        benchmark_return_pct=b_ret,
        excess_return_pct=excess_ret,
        strategy_max_drawdown_pct=s_max_dd,
        benchmark_max_drawdown_pct=b_max_dd,
        relative_max_drawdown_pct=rel_dd,
        correlation_like=corr,
        beta_like=beta,
        tracking_error_like=te,
        information_ratio_like=ir,
        relative_bucket=bucket,
        warnings=warnings,
        errors=errors
    )

def compare_strategy_to_benchmark_set(
    strategy_curve: EquityCurve,
    benchmark_curves: list[BenchmarkEquityCurve],
    strategy_run_id: Optional[str] = None
) -> BenchmarkComparisonTable:
    rows = []
    errors = []

    for b_curve in benchmark_curves:
        try:
            metrics = compare_strategy_to_benchmark(strategy_curve, b_curve, strategy_run_id)
            rows.append(metrics)
        except Exception as e:
            errors.append(f"Failed to compare with {b_curve.benchmark.symbol}: {e}")

    status = BenchmarkComparisonStatus.OK
    if not rows:
        status = BenchmarkComparisonStatus.EMPTY
    elif errors:
        status = BenchmarkComparisonStatus.WARNING

    return BenchmarkComparisonTable(
        strategy_run_id=strategy_run_id,
        rows=rows,
        created_at_utc=datetime.now().isoformat(),
        status=status,
        warnings=[],
        errors=errors
    )

def build_benchmark_comparison_report(
    strategy_run_id: Optional[str],
    benchmark_set_name: str,
    strategy_curve: EquityCurve,
    benchmark_curves: list[BenchmarkEquityCurve]
) -> BenchmarkComparisonReport:
    table = compare_strategy_to_benchmark_set(strategy_curve, benchmark_curves, strategy_run_id)

    s_ret = None
    if strategy_curve.points and strategy_curve.starting_cash > 0:
        s_ret = ((strategy_curve.points[-1].equity - strategy_curve.starting_cash) / strategy_curve.starting_cash) * 100.0

    best_sym = None
    worst_sym = None
    best_excess = float('-inf')
    worst_excess = float('inf')
    out_cnt = 0
    under_cnt = 0

    results = []
    for r in table.rows:
        results.append(benchmark_comparison_metrics_to_dict(r))
        if r.excess_return_pct is not None:
            if r.excess_return_pct > best_excess:
                best_excess = r.excess_return_pct
                best_sym = r.benchmark_symbol
            if r.excess_return_pct < worst_excess:
                worst_excess = r.excess_return_pct
                worst_sym = r.benchmark_symbol

        if r.relative_bucket == RelativePerformanceBucket.OUTPERFORMED:
            out_cnt += 1
        elif r.relative_bucket == RelativePerformanceBucket.UNDERPERFORMED:
            under_cnt += 1

    return BenchmarkComparisonReport(
        report_id=f"bmr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        created_at_utc=table.created_at_utc,
        strategy_run_id=strategy_run_id,
        benchmark_set_name=benchmark_set_name,
        status=table.status,
        strategy_total_return_pct=s_ret,
        benchmark_results=results,
        best_benchmark_symbol=best_sym,
        worst_benchmark_symbol=worst_sym,
        outperformed_count=out_cnt,
        underperformed_count=under_cnt,
        warnings=table.warnings,
        errors=table.errors
    )

def benchmark_comparison_metrics_to_dict(metrics: BenchmarkComparisonMetrics) -> dict:
    return {
        "benchmark_symbol": metrics.benchmark_symbol,
        "benchmark_name": metrics.benchmark_name,
        "strategy_return_pct": metrics.strategy_return_pct,
        "benchmark_return_pct": metrics.benchmark_return_pct,
        "excess_return_pct": metrics.excess_return_pct,
        "strategy_max_drawdown_pct": metrics.strategy_max_drawdown_pct,
        "benchmark_max_drawdown_pct": metrics.benchmark_max_drawdown_pct,
        "relative_max_drawdown_pct": metrics.relative_max_drawdown_pct,
        "correlation_like": metrics.correlation_like,
        "beta_like": metrics.beta_like,
        "tracking_error_like": metrics.tracking_error_like,
        "information_ratio_like": metrics.information_ratio_like,
        "relative_bucket": metrics.relative_bucket.value if hasattr(metrics.relative_bucket, "value") else metrics.relative_bucket,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def benchmark_comparison_table_to_dict(table: BenchmarkComparisonTable) -> dict:
    return {
        "strategy_run_id": table.strategy_run_id,
        "rows": [benchmark_comparison_metrics_to_dict(r) for r in table.rows],
        "created_at_utc": table.created_at_utc,
        "status": table.status.value if hasattr(table.status, "value") else table.status,
        "warnings": table.warnings,
        "errors": table.errors
    }

def benchmark_comparison_table_to_text(table: BenchmarkComparisonTable) -> str:
    if not table.rows:
        return "No benchmark comparisons available."

    lines = ["Benchmark Comparison Table"]
    lines.append("-" * 60)
    lines.append(f"{'Benchmark':<10} | {'S.Ret%':<8} | {'B.Ret%':<8} | {'Excess%':<8} | {'RelBucket':<15} | {'Beta':<6}")
    lines.append("-" * 60)

    for r in table.rows:
        s_ret = f"{r.strategy_return_pct:.2f}" if r.strategy_return_pct is not None else "N/A"
        b_ret = f"{r.benchmark_return_pct:.2f}" if r.benchmark_return_pct is not None else "N/A"
        exc = f"{r.excess_return_pct:.2f}" if r.excess_return_pct is not None else "N/A"
        beta = f"{r.beta_like:.2f}" if r.beta_like is not None else "N/A"
        bucket = r.relative_bucket.value if hasattr(r.relative_bucket, 'value') else str(r.relative_bucket)
        lines.append(f"{r.benchmark_symbol:<10} | {s_ret:<8} | {b_ret:<8} | {exc:<8} | {bucket:<15} | {beta:<6}")

    return "\n".join(lines)
