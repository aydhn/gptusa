from typing import Any

from usa_signal_bot.backtesting.analytics.phase148_models import (
    BacktestAnalyticsReport,
    ReturnSeriesPoint,
    RollingAnalyticsPoint,
    AdvancedPerformanceMetricResult,
    TradeDiagnosticRecord,
    FillDiagnosticRecord,
    CostDiagnosticRecord,
    ExposureDiagnosticResult,
    DrawdownDiagnosticResult,
    RunValidationReport
)
from usa_signal_bot.core.exceptions import BacktestAnalyticsReportError

def build_backtest_analytics_report(run_id: str, return_series: list[ReturnSeriesPoint], rolling_analytics: list[RollingAnalyticsPoint], performance_metrics: list[AdvancedPerformanceMetricResult], trade_diagnostics: list[TradeDiagnosticRecord], fill_diagnostics: list[FillDiagnosticRecord], cost_diagnostics: list[CostDiagnosticRecord], exposure_diagnostics: list[ExposureDiagnosticResult], drawdown_diagnostics: list[DrawdownDiagnosticResult], run_validation_report: RunValidationReport) -> BacktestAnalyticsReport:
    raise NotImplementedError()

def compute_backtest_analytics_report_hash(report: BacktestAnalyticsReport) -> str:
    raise NotImplementedError()

def validate_backtest_analytics_report(report: BacktestAnalyticsReport) -> list[str]:
    raise NotImplementedError()

def backtest_analytics_report_summary(report: BacktestAnalyticsReport) -> dict[str, Any]:
    raise NotImplementedError()

def backtest_analytics_report_to_text(report: BacktestAnalyticsReport, limit: int = 300) -> str:
    raise NotImplementedError()
