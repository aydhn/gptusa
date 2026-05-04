from usa_signal_bot.backtesting.benchmark_models import BenchmarkSet, BenchmarkEquityCurve, BenchmarkComparisonReport
from usa_signal_bot.backtesting.benchmark_comparison import BenchmarkComparisonMetrics, BenchmarkComparisonTable, benchmark_comparison_table_to_text
from usa_signal_bot.backtesting.buy_and_hold import BuyAndHoldResult, buy_and_hold_result_to_text
from usa_signal_bot.backtesting.performance_attribution import AttributionReport, attribution_report_to_text

def benchmark_set_to_text(benchmark_set: BenchmarkSet) -> str:
    lines = [
        f"Benchmark Set: {benchmark_set.name}",
        f"Description: {benchmark_set.description or 'N/A'}",
        f"Created At: {benchmark_set.created_at_utc}",
        "Benchmarks:"
    ]
    for b in benchmark_set.benchmarks:
        status = "ENABLED" if b.enabled else "DISABLED"
        lines.append(f"  - {b.symbol} ({b.benchmark_type.value if hasattr(b.benchmark_type, 'value') else b.benchmark_type}) [{status}]: {b.name}")
    return "\n".join(lines)

def benchmark_equity_curve_to_text(curve: BenchmarkEquityCurve) -> str:
    lines = [
        f"Benchmark Equity Curve: {curve.benchmark.symbol}",
        f"Starting Cash: ${curve.starting_cash:.2f}"
    ]
    if curve.ending_equity is not None:
        lines.append(f"Ending Equity: ${curve.ending_equity:.2f}")
    if curve.total_return_pct is not None:
        lines.append(f"Total Return: {curve.total_return_pct:.2f}%")
    if curve.errors:
        lines.append(f"Errors: {curve.errors}")
    return "\n".join(lines)

def benchmark_comparison_metrics_to_text(metrics: BenchmarkComparisonMetrics) -> str:
    s_ret = f"{metrics.strategy_return_pct:.2f}%" if metrics.strategy_return_pct is not None else "N/A"
    b_ret = f"{metrics.benchmark_return_pct:.2f}%" if metrics.benchmark_return_pct is not None else "N/A"
    exc = f"{metrics.excess_return_pct:.2f}%" if metrics.excess_return_pct is not None else "N/A"

    s_dd = f"{metrics.strategy_max_drawdown_pct:.2f}%" if metrics.strategy_max_drawdown_pct is not None else "N/A"
    b_dd = f"{metrics.benchmark_max_drawdown_pct:.2f}%" if metrics.benchmark_max_drawdown_pct is not None else "N/A"

    beta = f"{metrics.beta_like:.2f}" if metrics.beta_like is not None else "N/A"
    corr = f"{metrics.correlation_like:.2f}" if metrics.correlation_like is not None else "N/A"
    ir = f"{metrics.information_ratio_like:.2f}" if metrics.information_ratio_like is not None else "N/A"

    bucket = metrics.relative_bucket.value if hasattr(metrics.relative_bucket, "value") else str(metrics.relative_bucket)

    lines = [
        f"Comparison vs {metrics.benchmark_symbol} ({metrics.benchmark_name})",
        f"  Relative Performance: {bucket}",
        f"  Strategy Return:      {s_ret}",
        f"  Benchmark Return:     {b_ret}",
        f"  Excess Return:        {exc}",
        f"  Strategy Max DD:      {s_dd}",
        f"  Benchmark Max DD:     {b_dd}",
        f"  Beta-like:            {beta}",
        f"  Correlation-like:     {corr}",
        f"  Info Ratio-like:      {ir}"
    ]
    return "\n".join(lines)

def benchmark_comparison_report_to_text(report: BenchmarkComparisonReport) -> str:
    lines = [
        f"Benchmark Comparison Report (Set: {report.benchmark_set_name})",
        f"Status: {report.status.value if hasattr(report.status, 'value') else str(report.status)}",
        f"Strategy Return: {report.strategy_total_return_pct:.2f}%" if report.strategy_total_return_pct is not None else "Strategy Return: N/A",
        f"Outperformed: {report.outperformed_count} | Underperformed: {report.underperformed_count}",
        f"Best Relative: {report.best_benchmark_symbol or 'N/A'} | Worst Relative: {report.worst_benchmark_symbol or 'N/A'}",
        "\nDetailed Metrics:"
    ]
    for res in report.benchmark_results:
        metrics = BenchmarkComparisonMetrics(**res)
        s_ret = f"{metrics.strategy_return_pct:.2f}%" if metrics.strategy_return_pct is not None else "N/A"
        b_ret = f"{metrics.benchmark_return_pct:.2f}%" if metrics.benchmark_return_pct is not None else "N/A"
        exc = f"{metrics.excess_return_pct:.2f}%" if metrics.excess_return_pct is not None else "N/A"
        bucket = str(metrics.relative_bucket)

        lines.append(f"  - {metrics.benchmark_symbol:<5}: Strat={s_ret:<8} Bench={b_ret:<8} Excess={exc:<8} ({bucket})")

    lines.append("\nLimitations: These metrics are simplified 'correlation-like' research estimations, not strictly defined institutional financial metrics.")
    return "\n".join(lines)

def full_benchmark_analysis_to_text(table: BenchmarkComparisonTable, attribution: AttributionReport | None = None) -> str:
    parts = []
    parts.append(benchmark_comparison_table_to_text(table))
    parts.append("\nLimitations: These metrics are simplified 'correlation-like' research estimations, not strictly defined institutional financial metrics.")

    if attribution:
        parts.append("\n" + "="*60 + "\n")
        parts.append(attribution_report_to_text(attribution))
        parts.append("\nLimitations: This is a simplified attribution estimation, not a formal fund performance attribution report.")

    return "\n".join(parts)
