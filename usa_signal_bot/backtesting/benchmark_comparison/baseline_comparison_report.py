from typing import Any, Dict, List, Optional
import datetime, hashlib, json
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BaselineComparisonReport, BenchmarkReturnSeries, StrategyBenchmarkAlignment, RelativePerformanceMetricResult, BenchmarkDiagnosticRecord, BenchmarkComparisonQuality, create_baseline_comparison_report_id
def build_baseline_comparison_report(run_id: str, benchmark_series: List[BenchmarkReturnSeries], alignments: List[StrategyBenchmarkAlignment], relative_metrics: List[RelativePerformanceMetricResult], diagnostics: List[BenchmarkDiagnosticRecord]) -> BaselineComparisonReport:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    valid = len(benchmark_series) > 0 and len(alignments) > 0 and len(relative_metrics) > 0
    return BaselineComparisonReport(report_id=create_baseline_comparison_report_id(), created_at_utc=now_utc, run_id=run_id, benchmark_series=benchmark_series, alignments=alignments, relative_metrics=relative_metrics, diagnostics=diagnostics, report_valid=valid)
def baseline_comparison_report_to_text(r: BaselineComparisonReport, limit=300) -> str: return "baseline report"
