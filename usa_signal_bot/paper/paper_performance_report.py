from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from usa_signal_bot.paper.paper_models import VirtualAccount, PaperEquitySnapshot, PaperTrade, PaperFill, PaperPosition
from usa_signal_bot.paper.paper_analytics_models import (
    PaperPerformanceReport,
    PaperEquityMetrics,
    PaperTradeMetrics,
    PaperExposureMetrics,
    PaperRiskMetrics,
    create_paper_performance_report_id,
    paper_performance_report_to_dict
)
from usa_signal_bot.core.enums import (
    PaperAnalyticsStatus,
    PaperPerformanceBucket,
    PaperTrendDirection,
    PaperAnalyticsReportType,
    PaperMetricStatus,
    PaperRiskLevel
)
from usa_signal_bot.paper.paper_equity_analytics import calculate_paper_equity_metrics
from usa_signal_bot.paper.paper_trade_analytics import calculate_paper_trade_metrics
from usa_signal_bot.paper.paper_exposure_analytics import calculate_paper_exposure_metrics
from usa_signal_bot.paper.paper_risk_report import build_paper_risk_metrics

def classify_paper_performance_bucket(equity_metrics: PaperEquityMetrics, trade_metrics: PaperTradeMetrics, risk_metrics: PaperRiskMetrics) -> PaperPerformanceBucket:
    if equity_metrics.status != PaperMetricStatus.OK or trade_metrics.status != PaperMetricStatus.OK:
        return PaperPerformanceBucket.INSUFFICIENT_DATA

    ret = equity_metrics.total_return_pct or 0.0
    max_dd = equity_metrics.max_drawdown_pct or 0.0
    win_rate = trade_metrics.win_rate or 0.0
    profit_factor = trade_metrics.profit_factor or 0.0

    if ret < 0:
        if max_dd > 20.0 or (profit_factor > 0 and profit_factor < 0.5):
            return PaperPerformanceBucket.POOR
        return PaperPerformanceBucket.WEAK

    if ret > 5.0 and max_dd < 10.0 and win_rate > 0.5 and profit_factor > 1.2:
        return PaperPerformanceBucket.STRONG

    return PaperPerformanceBucket.ACCEPTABLE

def estimate_paper_performance_trend(snapshots: List[PaperEquitySnapshot], trades: List[PaperTrade]) -> PaperTrendDirection:
    # Just a simple heuristic over the latest snapshots for the overall report
    if not snapshots or len(snapshots) < 10:
        return PaperTrendDirection.INSUFFICIENT_DATA

    recent_snapshots = snapshots[-10:]
    older_snapshots = snapshots[-20:-10] if len(snapshots) >= 20 else snapshots[:-10]

    recent_eq = recent_snapshots[-1].total_equity
    recent_start = recent_snapshots[0].total_equity
    if recent_start > 0:
         recent_ret = (recent_eq - recent_start) / recent_start
    else:
         recent_ret = 0

    older_eq = older_snapshots[-1].total_equity if older_snapshots else recent_start
    older_start = older_snapshots[0].total_equity if older_snapshots else recent_start
    if older_start > 0:
         older_ret = (older_eq - older_start) / older_start
    else:
         older_ret = 0

    if recent_ret > older_ret and recent_ret > 0:
        return PaperTrendDirection.IMPROVING
    elif recent_ret < older_ret and recent_ret < 0:
        return PaperTrendDirection.DETERIORATING
    elif abs(recent_ret - older_ret) < 0.01:
        return PaperTrendDirection.STABLE

    return PaperTrendDirection.MIXED

def build_paper_performance_report(account: VirtualAccount, snapshots: List[PaperEquitySnapshot], trades: List[PaperTrade], fills: List[PaperFill], positions: List[PaperPosition], source_run_id: Optional[str] = None) -> PaperPerformanceReport:
    equity_metrics = calculate_paper_equity_metrics(snapshots)
    trade_metrics = calculate_paper_trade_metrics(trades)
    exposure_metrics = calculate_paper_exposure_metrics(snapshots, positions)
    risk_metrics = build_paper_risk_metrics(account, equity_metrics, exposure_metrics, positions)

    bucket = classify_paper_performance_bucket(equity_metrics, trade_metrics, risk_metrics)
    trend = estimate_paper_performance_trend(snapshots, trades)

    status = PaperAnalyticsStatus.COMPLETED
    if equity_metrics.status != PaperMetricStatus.OK or trade_metrics.status != PaperMetricStatus.OK:
        status = PaperAnalyticsStatus.WARNING
    if risk_metrics.risk_level == PaperRiskLevel.CRITICAL:
        status = PaperAnalyticsStatus.WARNING

    if not snapshots and not trades:
         status = PaperAnalyticsStatus.EMPTY

    return PaperPerformanceReport(
        report_id=create_paper_performance_report_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=PaperAnalyticsReportType.FULL_SUMMARY,
        status=status,
        account_id=account.account_id,
        source_run_id=source_run_id,
        equity_metrics=equity_metrics,
        trade_metrics=trade_metrics,
        exposure_metrics=exposure_metrics,
        risk_metrics=risk_metrics,
        performance_bucket=bucket,
        trend_direction=trend,
        warnings=[],
        errors=[]
    )

def paper_performance_report_to_text(report: PaperPerformanceReport) -> str:
    lines = [
        "--- Paper Performance Report ---",
        f"Status: {report.status.value}",
        f"Performance Bucket: {report.performance_bucket.value}",
        f"Trend Direction: {report.trend_direction.value}",
        f"Risk Level: {report.risk_metrics.risk_level.value}",
        "\nEquity Highlights:"
    ]
    if report.equity_metrics.total_return_pct is not None:
         lines.append(f"- Total Return %: {report.equity_metrics.total_return_pct:.2f}%")
    if report.equity_metrics.max_drawdown_pct is not None:
         lines.append(f"- Max Drawdown %: {report.equity_metrics.max_drawdown_pct:.2f}%")

    lines.append("\nTrade Highlights:")
    if report.trade_metrics.win_rate is not None:
         lines.append(f"- Win Rate: {report.trade_metrics.win_rate * 100:.2f}%")
    if report.trade_metrics.profit_factor is not None:
         lines.append(f"- Profit Factor: {report.trade_metrics.profit_factor:.2f}")

    lines.append(f"- Total Trades: {report.trade_metrics.total_trades}")

    if report.warnings:
        lines.append("\nWarnings: " + ", ".join(report.warnings))
    if report.errors:
        lines.append("\nErrors: " + ", ".join(report.errors))

    lines.append("\nDisclaimer: This is a local paper simulation only. Not investment advice.")
    return "\n".join(lines)

def build_full_paper_analytics_bundle(account: VirtualAccount, snapshots: List[PaperEquitySnapshot], trades: List[PaperTrade], fills: List[PaperFill], positions: List[PaperPosition], source_run_id: Optional[str] = None) -> Dict[str, Any]:
    report = build_paper_performance_report(account, snapshots, trades, fills, positions, source_run_id)
    return paper_performance_report_to_dict(report)
