from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    PaperAnalyticsStatus,
    PaperMetricStatus,
    PaperRiskLevel,
    PaperDrawdownStatus,
    PaperRiskLimitStatus,
    PaperPerformanceBucket,
    PaperTrendDirection,
    PaperAnalyticsReportType
)

@dataclass
class PaperEquityMetrics:
    status: PaperMetricStatus
    starting_equity: Optional[float]
    ending_equity: Optional[float]
    absolute_return: Optional[float]
    total_return_pct: Optional[float]
    peak_equity: Optional[float]
    trough_equity: Optional[float]
    max_drawdown: Optional[float]
    max_drawdown_pct: Optional[float]
    current_drawdown: Optional[float]
    current_drawdown_pct: Optional[float]
    equity_points: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class PaperTradeMetrics:
    status: PaperMetricStatus
    total_trades: int
    closed_trades: int
    open_trades: int
    winning_trades: int
    losing_trades: int
    breakeven_trades: int
    win_rate: Optional[float]
    loss_rate: Optional[float]
    average_win: Optional[float]
    average_loss: Optional[float]
    average_trade: Optional[float]
    gross_profit: float
    gross_loss: float
    net_pnl: float
    profit_factor: Optional[float]
    expectancy: Optional[float]
    best_trade: Optional[float]
    worst_trade: Optional[float]
    max_win_streak: int
    max_loss_streak: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class PaperExposureMetrics:
    status: PaperMetricStatus
    average_gross_exposure: Optional[float]
    max_gross_exposure: Optional[float]
    average_net_exposure: Optional[float]
    max_net_exposure: Optional[float]
    average_open_positions: Optional[float]
    max_open_positions: Optional[int]
    final_open_positions: int
    exposure_to_equity_avg: Optional[float]
    exposure_to_equity_max: Optional[float]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class PaperRiskMetrics:
    status: PaperMetricStatus
    risk_level: PaperRiskLevel
    drawdown_status: PaperDrawdownStatus
    risk_limit_status: PaperRiskLimitStatus
    max_drawdown_pct: Optional[float]
    current_drawdown_pct: Optional[float]
    exposure_to_equity_max: Optional[float]
    cash_buffer_pct: Optional[float]
    open_position_count: int
    largest_position_weight: Optional[float]
    concentration_warning: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class PaperPerformanceReport:
    report_id: str
    created_at_utc: str
    report_type: PaperAnalyticsReportType
    status: PaperAnalyticsStatus
    account_id: Optional[str]
    source_run_id: Optional[str]
    equity_metrics: PaperEquityMetrics
    trade_metrics: PaperTradeMetrics
    exposure_metrics: PaperExposureMetrics
    risk_metrics: PaperRiskMetrics
    performance_bucket: PaperPerformanceBucket
    trend_direction: PaperTrendDirection
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

def paper_equity_metrics_to_dict(metrics: PaperEquityMetrics) -> Dict[str, Any]:
    return {
        "status": metrics.status.value,
        "starting_equity": metrics.starting_equity,
        "ending_equity": metrics.ending_equity,
        "absolute_return": metrics.absolute_return,
        "total_return_pct": metrics.total_return_pct,
        "peak_equity": metrics.peak_equity,
        "trough_equity": metrics.trough_equity,
        "max_drawdown": metrics.max_drawdown,
        "max_drawdown_pct": metrics.max_drawdown_pct,
        "current_drawdown": metrics.current_drawdown,
        "current_drawdown_pct": metrics.current_drawdown_pct,
        "equity_points": metrics.equity_points,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def paper_trade_metrics_to_dict(metrics: PaperTradeMetrics) -> Dict[str, Any]:
    return {
        "status": metrics.status.value,
        "total_trades": metrics.total_trades,
        "closed_trades": metrics.closed_trades,
        "open_trades": metrics.open_trades,
        "winning_trades": metrics.winning_trades,
        "losing_trades": metrics.losing_trades,
        "breakeven_trades": metrics.breakeven_trades,
        "win_rate": metrics.win_rate,
        "loss_rate": metrics.loss_rate,
        "average_win": metrics.average_win,
        "average_loss": metrics.average_loss,
        "average_trade": metrics.average_trade,
        "gross_profit": metrics.gross_profit,
        "gross_loss": metrics.gross_loss,
        "net_pnl": metrics.net_pnl,
        "profit_factor": metrics.profit_factor,
        "expectancy": metrics.expectancy,
        "best_trade": metrics.best_trade,
        "worst_trade": metrics.worst_trade,
        "max_win_streak": metrics.max_win_streak,
        "max_loss_streak": metrics.max_loss_streak,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def paper_exposure_metrics_to_dict(metrics: PaperExposureMetrics) -> Dict[str, Any]:
    return {
        "status": metrics.status.value,
        "average_gross_exposure": metrics.average_gross_exposure,
        "max_gross_exposure": metrics.max_gross_exposure,
        "average_net_exposure": metrics.average_net_exposure,
        "max_net_exposure": metrics.max_net_exposure,
        "average_open_positions": metrics.average_open_positions,
        "max_open_positions": metrics.max_open_positions,
        "final_open_positions": metrics.final_open_positions,
        "exposure_to_equity_avg": metrics.exposure_to_equity_avg,
        "exposure_to_equity_max": metrics.exposure_to_equity_max,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def paper_risk_metrics_to_dict(metrics: PaperRiskMetrics) -> Dict[str, Any]:
    return {
        "status": metrics.status.value,
        "risk_level": metrics.risk_level.value,
        "drawdown_status": metrics.drawdown_status.value,
        "risk_limit_status": metrics.risk_limit_status.value,
        "max_drawdown_pct": metrics.max_drawdown_pct,
        "current_drawdown_pct": metrics.current_drawdown_pct,
        "exposure_to_equity_max": metrics.exposure_to_equity_max,
        "cash_buffer_pct": metrics.cash_buffer_pct,
        "open_position_count": metrics.open_position_count,
        "largest_position_weight": metrics.largest_position_weight,
        "concentration_warning": metrics.concentration_warning,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def paper_performance_report_to_dict(report: PaperPerformanceReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "report_type": report.report_type.value,
        "status": report.status.value,
        "account_id": report.account_id,
        "source_run_id": report.source_run_id,
        "equity_metrics": paper_equity_metrics_to_dict(report.equity_metrics),
        "trade_metrics": paper_trade_metrics_to_dict(report.trade_metrics),
        "exposure_metrics": paper_exposure_metrics_to_dict(report.exposure_metrics),
        "risk_metrics": paper_risk_metrics_to_dict(report.risk_metrics),
        "performance_bucket": report.performance_bucket.value,
        "trend_direction": report.trend_direction.value,
        "warnings": report.warnings,
        "errors": report.errors,
        "metadata": report.metadata
    }

def validate_paper_equity_metrics(metrics: PaperEquityMetrics) -> None:
    pass

def validate_paper_trade_metrics(metrics: PaperTradeMetrics) -> None:
    pass

def validate_paper_exposure_metrics(metrics: PaperExposureMetrics) -> None:
    pass

def validate_paper_risk_metrics(metrics: PaperRiskMetrics) -> None:
    pass

def validate_paper_performance_report(report: PaperPerformanceReport) -> None:
    pass

def create_paper_performance_report_id(prefix: str = "paper_perf") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}"
