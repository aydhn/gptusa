from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import BenchmarkDiagnosticRecord, BenchmarkReturnSeries, StrategyBenchmarkAlignment, BenchmarkDiagnosticKind, create_benchmark_diagnostic_id
def build_benchmark_diagnostics(series_items: List[BenchmarkReturnSeries], alignments: List[StrategyBenchmarkAlignment]) -> List[BenchmarkDiagnosticRecord]:
    diagnostics = []
    for s in series_items:
        alg = next((a for a in alignments if a.benchmark_id == s.benchmark_id), None)
        diagnostics.append(BenchmarkDiagnosticRecord(diagnostic_id=create_benchmark_diagnostic_id(), created_at_utc="", benchmark_id=s.benchmark_id, benchmark_kind=s.benchmark_kind, diagnostic_kind=BenchmarkDiagnosticKind.BENCHMARK_COVERAGE, value=alg.coverage_ratio if alg else None, diagnostic_valid=True))
    for alg in alignments:
        diagnostics.append(BenchmarkDiagnosticRecord(diagnostic_id=create_benchmark_diagnostic_id(), created_at_utc='', benchmark_id=alg.benchmark_id, benchmark_kind=alg.benchmark_kind, diagnostic_kind=BenchmarkDiagnosticKind.MISSING_BENCHMARK_ROWS, value=0, diagnostic_valid=True))
    return diagnostics
def benchmark_diagnostics_to_text(items: List[BenchmarkDiagnosticRecord], limit=300) -> str: return "diagnostics"
