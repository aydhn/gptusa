from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from usa_signal_bot.paper.paper_models import PaperEquitySnapshot, PaperTrade
from usa_signal_bot.core.enums import PaperMetricStatus, PaperTrendDirection
from usa_signal_bot.paper.paper_equity_analytics import extract_equity_values, calculate_equity_total_return_pct, calculate_max_paper_drawdown
from usa_signal_bot.paper.paper_trade_analytics import filter_closed_paper_trades, calculate_paper_win_rate

@dataclass
class PaperRollingMetricPoint:
    timestamp_utc: str
    window_size: int
    equity_return_pct: Optional[float]
    rolling_max_drawdown_pct: Optional[float]
    rolling_trade_count: int
    rolling_win_rate: Optional[float]
    rolling_net_pnl: Optional[float]
    warnings: List[str] = field(default_factory=list)

@dataclass
class PaperRollingMetricsReport:
    report_id: str
    created_at_utc: str
    status: PaperMetricStatus
    window_size: int
    points: List[PaperRollingMetricPoint]
    trend_direction: PaperTrendDirection
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def calculate_rolling_equity_return(values: List[float], start_idx: int, end_idx: int) -> Optional[float]:
    if start_idx < 0 or end_idx >= len(values) or start_idx >= end_idx:
        return None
    return calculate_equity_total_return_pct(values[start_idx:end_idx+1])

def calculate_rolling_drawdown(values: List[float], start_idx: int, end_idx: int) -> Optional[float]:
    if start_idx < 0 or end_idx >= len(values) or start_idx >= end_idx:
        return None
    _, max_dd_pct = calculate_max_paper_drawdown(values[start_idx:end_idx+1])
    return max_dd_pct

def estimate_paper_trend_direction(points: List[PaperRollingMetricPoint]) -> PaperTrendDirection:
    if not points or len(points) < 2:
        return PaperTrendDirection.INSUFFICIENT_DATA

    returns = [p.equity_return_pct for p in points if p.equity_return_pct is not None]
    if len(returns) < 2:
        return PaperTrendDirection.INSUFFICIENT_DATA

    recent = returns[-1]
    previous = sum(returns[:-1]) / len(returns[:-1])

    if recent > previous and recent > 0:
        return PaperTrendDirection.IMPROVING
    elif recent < previous and recent < 0:
        return PaperTrendDirection.DETERIORATING
    elif abs(recent - previous) < 1.0:
        return PaperTrendDirection.STABLE
    else:
        return PaperTrendDirection.MIXED

def calculate_paper_rolling_metrics(snapshots: List[PaperEquitySnapshot], trades: List[PaperTrade], window_size: int = 20) -> PaperRollingMetricsReport:
    if window_size <= 0:
        raise ValueError("window_size must be positive")

    if not snapshots or len(snapshots) < window_size:
        return PaperRollingMetricsReport(
            report_id=f"rolling_report_{datetime.now(timezone.utc).timestamp()}",
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=PaperMetricStatus.INSUFFICIENT_DATA,
            window_size=window_size,
            points=[],
            trend_direction=PaperTrendDirection.INSUFFICIENT_DATA,
            warnings=["Insufficient data for rolling metrics."],
            errors=[]
        )

    values = extract_equity_values(snapshots)
    closed_trades = filter_closed_paper_trades(trades)

    points = []
    for i in range(window_size - 1, len(snapshots)):
        start_idx = i - window_size + 1
        end_idx = i

        timestamp = snapshots[end_idx].timestamp_utc
        ret_pct = calculate_rolling_equity_return(values, start_idx, end_idx)
        dd_pct = calculate_rolling_drawdown(values, start_idx, end_idx)

        start_time = snapshots[start_idx].timestamp_utc
        window_trades = [t for t in closed_trades if t.closed_at_utc and start_time <= t.closed_at_utc <= timestamp]

        trade_count = len(window_trades)
        win_rate = calculate_paper_win_rate(window_trades) if window_trades else None
        net_pnl = sum(t.realized_pnl for t in window_trades) if window_trades else None

        points.append(PaperRollingMetricPoint(
            timestamp_utc=timestamp,
            window_size=window_size,
            equity_return_pct=ret_pct,
            rolling_max_drawdown_pct=dd_pct,
            rolling_trade_count=trade_count,
            rolling_win_rate=win_rate,
            rolling_net_pnl=net_pnl
        ))

    trend = estimate_paper_trend_direction(points)

    return PaperRollingMetricsReport(
        report_id=f"rolling_report_{datetime.now(timezone.utc).timestamp()}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=PaperMetricStatus.OK,
        window_size=window_size,
        points=points,
        trend_direction=trend,
        warnings=[],
        errors=[]
    )

def paper_rolling_metric_point_to_dict(point: PaperRollingMetricPoint) -> Dict[str, Any]:
    return {
        "timestamp_utc": point.timestamp_utc,
        "window_size": point.window_size,
        "equity_return_pct": point.equity_return_pct,
        "rolling_max_drawdown_pct": point.rolling_max_drawdown_pct,
        "rolling_trade_count": point.rolling_trade_count,
        "rolling_win_rate": point.rolling_win_rate,
        "rolling_net_pnl": point.rolling_net_pnl,
        "warnings": point.warnings
    }

def paper_rolling_metrics_report_to_dict(report: PaperRollingMetricsReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "status": report.status.value,
        "window_size": report.window_size,
        "points": [paper_rolling_metric_point_to_dict(p) for p in report.points],
        "trend_direction": report.trend_direction.value,
        "warnings": report.warnings,
        "errors": report.errors
    }

def paper_rolling_metrics_report_to_text(report: PaperRollingMetricsReport, limit: int = 20) -> str:
    lines = [
        "--- Paper Rolling Metrics ---",
        f"Status: {report.status.value}",
        f"Trend Direction: {report.trend_direction.value}",
        f"Window Size: {report.window_size}",
    ]
    if report.points:
        lines.append(f"\nRecent Points (up to {limit}):")
        for point in report.points[-limit:]:
            ret = f"{point.equity_return_pct:.2f}%" if point.equity_return_pct is not None else "N/A"
            dd = f"{point.rolling_max_drawdown_pct:.2f}%" if point.rolling_max_drawdown_pct is not None else "N/A"
            wr = f"{point.rolling_win_rate*100:.2f}%" if point.rolling_win_rate is not None else "N/A"
            lines.append(f"- [{point.timestamp_utc}] Return: {ret}, MaxDD: {dd}, Trades: {point.rolling_trade_count}, WinRate: {wr}")

    if report.warnings:
        lines.append("\nWarnings: " + ", ".join(report.warnings))
    if report.errors:
        lines.append("\nErrors: " + ", ".join(report.errors))

    lines.append("")
    return "\n".join(lines)
