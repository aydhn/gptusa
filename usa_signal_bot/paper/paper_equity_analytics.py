from typing import List, Dict, Tuple, Optional
from usa_signal_bot.paper.paper_models import PaperEquitySnapshot
from usa_signal_bot.paper.paper_analytics_models import PaperEquityMetrics
from usa_signal_bot.core.enums import PaperMetricStatus

def extract_equity_values(snapshots: List[PaperEquitySnapshot]) -> List[float]:
    return [snapshot.equity for snapshot in snapshots]

def extract_snapshot_timestamps(snapshots: List[PaperEquitySnapshot]) -> List[str]:
    return [snapshot.timestamp_utc for snapshot in snapshots]

def calculate_equity_total_return_pct(values: List[float]) -> Optional[float]:
    if not values or len(values) < 2:
        return None
    start = values[0]
    end = values[-1]
    if start == 0:
        return None
    return ((end - start) / start) * 100.0

def calculate_equity_peak(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return max(values)

def calculate_equity_trough(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return min(values)

def calculate_paper_drawdown_series(values: List[float]) -> List[Dict[str, float]]:
    if not values:
        return []
    series = []
    peak = values[0]
    for val in values:
        if val > peak:
            peak = val
        dd = peak - val
        dd_pct = (dd / peak * 100.0) if peak > 0 else 0.0
        series.append({"drawdown": dd, "drawdown_pct": dd_pct})
    return series

def calculate_max_paper_drawdown(values: List[float]) -> Tuple[Optional[float], Optional[float]]:
    if not values:
        return None, None
    series = calculate_paper_drawdown_series(values)
    max_dd = max([item["drawdown"] for item in series])
    max_dd_pct = max([item["drawdown_pct"] for item in series])
    return max_dd, max_dd_pct

def calculate_current_paper_drawdown(values: List[float]) -> Tuple[Optional[float], Optional[float]]:
    if not values:
        return None, None
    series = calculate_paper_drawdown_series(values)
    return series[-1]["drawdown"], series[-1]["drawdown_pct"]

def calculate_paper_equity_metrics(snapshots: List[PaperEquitySnapshot]) -> PaperEquityMetrics:
    if not snapshots:
        return PaperEquityMetrics(
            status=PaperMetricStatus.EMPTY,
            starting_equity=None,
            ending_equity=None,
            absolute_return=None,
            total_return_pct=None,
            peak_equity=None,
            trough_equity=None,
            max_drawdown=None,
            max_drawdown_pct=None,
            current_drawdown=None,
            current_drawdown_pct=None,
            equity_points=0,
            warnings=["No equity snapshots provided."],
            errors=[]
        )

    values = extract_equity_values(snapshots)
    if len(values) == 1:
        return PaperEquityMetrics(
            status=PaperMetricStatus.INSUFFICIENT_DATA,
            starting_equity=values[0],
            ending_equity=values[0],
            absolute_return=0.0,
            total_return_pct=0.0,
            peak_equity=values[0],
            trough_equity=values[0],
            max_drawdown=0.0,
            max_drawdown_pct=0.0,
            current_drawdown=0.0,
            current_drawdown_pct=0.0,
            equity_points=1,
            warnings=["Only one equity snapshot provided."],
            errors=[]
        )

    start = values[0]
    end = values[-1]
    absolute_return = end - start
    total_return_pct = calculate_equity_total_return_pct(values)
    peak = calculate_equity_peak(values)
    trough = calculate_equity_trough(values)
    max_dd, max_dd_pct = calculate_max_paper_drawdown(values)
    curr_dd, curr_dd_pct = calculate_current_paper_drawdown(values)

    warnings = []
    if trough is not None and trough < 0:
        warnings.append("Equity dipped below zero.")

    return PaperEquityMetrics(
        status=PaperMetricStatus.OK,
        starting_equity=start,
        ending_equity=end,
        absolute_return=absolute_return,
        total_return_pct=total_return_pct,
        peak_equity=peak,
        trough_equity=trough,
        max_drawdown=max_dd,
        max_drawdown_pct=max_dd_pct,
        current_drawdown=curr_dd,
        current_drawdown_pct=curr_dd_pct,
        equity_points=len(values),
        warnings=warnings,
        errors=[]
    )

def paper_equity_metrics_to_text(metrics: PaperEquityMetrics) -> str:
    lines = [
        "--- Paper Equity Metrics ---",
        f"Status: {metrics.status.value}",
        f"Equity Points: {metrics.equity_points}",
    ]
    if metrics.starting_equity is not None:
        lines.append(f"Starting Equity: {metrics.starting_equity:.2f}")
    if metrics.ending_equity is not None:
        lines.append(f"Ending Equity: {metrics.ending_equity:.2f}")
    if metrics.absolute_return is not None:
        lines.append(f"Absolute Return: {metrics.absolute_return:.2f}")
    if metrics.total_return_pct is not None:
        lines.append(f"Total Return %: {metrics.total_return_pct:.2f}%")
    if metrics.peak_equity is not None:
        lines.append(f"Peak Equity: {metrics.peak_equity:.2f}")
    if metrics.trough_equity is not None:
        lines.append(f"Trough Equity: {metrics.trough_equity:.2f}")
    if metrics.max_drawdown_pct is not None:
        lines.append(f"Max Drawdown %: {metrics.max_drawdown_pct:.2f}%")
    if metrics.current_drawdown_pct is not None:
        lines.append(f"Current Drawdown %: {metrics.current_drawdown_pct:.2f}%")

    if metrics.warnings:
        lines.append("Warnings: " + ", ".join(metrics.warnings))
    if metrics.errors:
        lines.append("Errors: " + ", ".join(metrics.errors))

    lines.append("")
    return "\n".join(lines)
