from pathlib import Path
from typing import Optional

from usa_signal_bot.paper.paper_analytics_models import (
    PaperPerformanceReport,
    PaperEquityMetrics,
    PaperTradeMetrics,
    PaperExposureMetrics,
    PaperRiskMetrics
)
from usa_signal_bot.paper.paper_risk_report import PaperRiskReport
from usa_signal_bot.paper.paper_drawdown_monitor import PaperDrawdownReport
from usa_signal_bot.paper.paper_rolling_metrics import PaperRollingMetricsReport

from usa_signal_bot.paper.paper_equity_analytics import paper_equity_metrics_to_text
from usa_signal_bot.paper.paper_trade_analytics import paper_trade_metrics_to_text
from usa_signal_bot.paper.paper_exposure_analytics import paper_exposure_metrics_to_text
from usa_signal_bot.paper.paper_performance_report import paper_performance_report_to_text
from usa_signal_bot.paper.paper_risk_report import paper_risk_report_to_text
from usa_signal_bot.paper.paper_drawdown_monitor import paper_drawdown_report_to_text
from usa_signal_bot.paper.paper_rolling_metrics import paper_rolling_metrics_report_to_text
from usa_signal_bot.paper.paper_analytics_store import write_paper_analytics_bundle_json

def paper_equity_metrics_report_to_text(metrics: PaperEquityMetrics) -> str:
    return paper_equity_metrics_to_text(metrics)

def paper_trade_metrics_report_to_text(metrics: PaperTradeMetrics) -> str:
    return paper_trade_metrics_to_text(metrics)

def paper_exposure_metrics_report_to_text(metrics: PaperExposureMetrics) -> str:
    return paper_exposure_metrics_to_text(metrics)

def paper_risk_metrics_report_to_text(metrics: PaperRiskMetrics) -> str:
    lines = [
        "--- Paper Risk Metrics ---",
        f"Status: {metrics.status.value}",
        f"Risk Level: {metrics.risk_level.value}",
        f"Risk Limit Status: {metrics.risk_limit_status.value}",
        f"Drawdown Status: {metrics.drawdown_status.value}"
    ]
    if metrics.cash_buffer_pct is not None:
         lines.append(f"Cash Buffer: {metrics.cash_buffer_pct * 100:.2f}%")
    if metrics.largest_position_weight is not None:
         lines.append(f"Largest Position: {metrics.largest_position_weight * 100:.2f}%")
    if metrics.concentration_warning:
         lines.append("CONCENTRATION WARNING")
    return "\n".join(lines)

def paper_analytics_limitations_text() -> str:
    return (
        "*** PAPER ANALYTICS LIMITATIONS ***\n"
        "- This is a purely local paper trading simulation.\n"
        "- Order fills do not reflect real market conditions (no true slippage/liquidity modeling).\n"
        "- Equity values depend on cached daily close prices.\n"
        "- Drawdown monitor does not and will not issue live broker stop-loss orders.\n- No live broker orders will be issued.\n"
        "- This report is for research analytics only. It is NOT investment advice.\n"
        "- Past simulated performance is not indicative of future actual performance."
    )

def paper_full_analytics_report_to_text(
    report: PaperPerformanceReport,
    risk_report: Optional[PaperRiskReport] = None,
    drawdown_report: Optional[PaperDrawdownReport] = None,
    rolling_report: Optional[PaperRollingMetricsReport] = None
) -> str:
    blocks = [paper_performance_report_to_text(report)]

    if risk_report:
        blocks.append(paper_risk_report_to_text(risk_report))
    if drawdown_report:
        blocks.append(paper_drawdown_report_to_text(drawdown_report))
    if rolling_report:
        blocks.append(paper_rolling_metrics_report_to_text(rolling_report, limit=5))

    blocks.append(paper_analytics_limitations_text())

    return "\n\n".join(blocks)

def write_paper_analytics_report_json(
    path: Path,
    report: PaperPerformanceReport,
    risk_report: Optional[PaperRiskReport] = None,
    drawdown_report: Optional[PaperDrawdownReport] = None,
    rolling_report: Optional[PaperRollingMetricsReport] = None
) -> Path:
    from usa_signal_bot.paper.paper_analytics_models import paper_performance_report_to_dict
    from usa_signal_bot.paper.paper_risk_report import paper_risk_report_to_dict
    from usa_signal_bot.paper.paper_drawdown_monitor import paper_drawdown_report_to_dict
    from usa_signal_bot.paper.paper_rolling_metrics import paper_rolling_metrics_report_to_dict

    bundle = {
        "performance_report": paper_performance_report_to_dict(report)
    }
    if risk_report:
        bundle["risk_report"] = paper_risk_report_to_dict(risk_report)
    if drawdown_report:
        bundle["drawdown_report"] = paper_drawdown_report_to_dict(drawdown_report)
    if rolling_report:
        bundle["rolling_report"] = paper_rolling_metrics_report_to_dict(rolling_report)

    return write_paper_analytics_bundle_json(path, bundle)
