from dataclasses import dataclass, field
from typing import Optional, List
from usa_signal_bot.core.exceptions import DrawdownAnalyticsError
from usa_signal_bot.backtesting.equity_curve import EquityCurve

@dataclass
class DrawdownPeriod:
    start_time_utc: str
    trough_time_utc: str
    recovery_time_utc: Optional[str]
    peak_equity: float
    trough_equity: float
    drawdown: float
    drawdown_pct: float
    duration_points: int
    recovered: bool

@dataclass
class DrawdownAnalytics:
    max_drawdown: Optional[float]
    max_drawdown_pct: Optional[float]
    average_drawdown_pct: Optional[float]
    drawdown_periods: List[DrawdownPeriod]
    longest_drawdown_duration: Optional[int]
    current_drawdown_pct: Optional[float]
    recovered_periods: int
    unrecovered_periods: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def calculate_drawdown_periods(curve: EquityCurve) -> List[DrawdownPeriod]:
    if not curve.points:
        return []

    periods = []
    current_peak_val = curve.points[0].equity
    current_peak_time = curve.points[0].timestamp_utc
    in_drawdown = False

    trough_val = current_peak_val
    trough_time = current_peak_time
    duration = 0

    for i, point in enumerate(curve.points):
        val = point.equity
        time = point.timestamp_utc

        if val >= current_peak_val:
            if in_drawdown:
                # Recovered!
                duration += 1
                periods.append(DrawdownPeriod(
                    start_time_utc=current_peak_time,
                    trough_time_utc=trough_time,
                    recovery_time_utc=time,
                    peak_equity=current_peak_val,
                    trough_equity=trough_val,
                    drawdown=current_peak_val - trough_val,
                    drawdown_pct=(current_peak_val - trough_val) / current_peak_val if current_peak_val > 0 else 0.0,
                    duration_points=duration,
                    recovered=True
                ))
                in_drawdown = False

            # New peak
            current_peak_val = val
            current_peak_time = time
            trough_val = val
            trough_time = time
            duration = 0
        else:
            if not in_drawdown:
                in_drawdown = True

            duration += 1
            if val < trough_val:
                trough_val = val
                trough_time = time

    if in_drawdown:
        periods.append(DrawdownPeriod(
            start_time_utc=current_peak_time,
            trough_time_utc=trough_time,
            recovery_time_utc=None,
            peak_equity=current_peak_val,
            trough_equity=trough_val,
            drawdown=current_peak_val - trough_val,
            drawdown_pct=(current_peak_val - trough_val) / current_peak_val if current_peak_val > 0 else 0.0,
            duration_points=duration,
            recovered=False
        ))

    return periods

def calculate_drawdown_analytics(curve: EquityCurve) -> DrawdownAnalytics:
    warnings = []
    if not curve.points:
        warnings.append("Empty equity curve, cannot calculate drawdown analytics.")
        return DrawdownAnalytics(
            max_drawdown=None, max_drawdown_pct=None, average_drawdown_pct=None,
            drawdown_periods=[], longest_drawdown_duration=None,
            current_drawdown_pct=None, recovered_periods=0, unrecovered_periods=0,
            warnings=warnings
        )

    periods = calculate_drawdown_periods(curve)

    max_dd = curve.max_drawdown
    max_dd_pct = curve.max_drawdown_pct

    avg_dd_pct = None
    if periods:
        avg_dd_pct = sum(p.drawdown_pct for p in periods) / len(periods)

    longest = max((p.duration_points for p in periods), default=None)

    current_dd_pct = curve.points[-1].drawdown_pct if curve.points else 0.0

    recovered = sum(1 for p in periods if p.recovered)
    unrecovered = sum(1 for p in periods if not p.recovered)

    return DrawdownAnalytics(
        max_drawdown=max_dd,
        max_drawdown_pct=max_dd_pct,
        average_drawdown_pct=avg_dd_pct,
        drawdown_periods=periods,
        longest_drawdown_duration=longest,
        current_drawdown_pct=current_dd_pct,
        recovered_periods=recovered,
        unrecovered_periods=unrecovered,
        warnings=warnings
    )

def drawdown_period_to_dict(period: DrawdownPeriod) -> dict:
    return {
        "start_time_utc": period.start_time_utc,
        "trough_time_utc": period.trough_time_utc,
        "recovery_time_utc": period.recovery_time_utc,
        "peak_equity": period.peak_equity,
        "trough_equity": period.trough_equity,
        "drawdown": period.drawdown,
        "drawdown_pct": period.drawdown_pct,
        "duration_points": period.duration_points,
        "recovered": period.recovered
    }

def drawdown_analytics_to_dict(analytics: DrawdownAnalytics) -> dict:
    return {
        "max_drawdown": analytics.max_drawdown,
        "max_drawdown_pct": analytics.max_drawdown_pct,
        "average_drawdown_pct": analytics.average_drawdown_pct,
        "drawdown_periods": [drawdown_period_to_dict(p) for p in analytics.drawdown_periods],
        "longest_drawdown_duration": analytics.longest_drawdown_duration,
        "current_drawdown_pct": analytics.current_drawdown_pct,
        "recovered_periods": analytics.recovered_periods,
        "unrecovered_periods": analytics.unrecovered_periods,
        "warnings": analytics.warnings,
        "errors": analytics.errors
    }

def drawdown_analytics_to_text(analytics: DrawdownAnalytics, limit: int = 10) -> str:
    lines = [
        "Drawdown Analytics",
        f"  Max Drawdown %:   {(analytics.max_drawdown_pct or 0)*100:.2f}%",
        f"  Avg Drawdown %:   {(analytics.average_drawdown_pct or 0)*100:.2f}%",
        f"  Longest Duration: {analytics.longest_drawdown_duration or 0} points",
        f"  Current DD %:     {(analytics.current_drawdown_pct or 0)*100:.2f}%",
        f"  Periods (R/U):    {analytics.recovered_periods} / {analytics.unrecovered_periods}"
    ]
    if analytics.drawdown_periods:
         lines.append("\n  Recent Periods:")
         for p in sorted(analytics.drawdown_periods, key=lambda x: x.start_time_utc, reverse=True)[:limit]:
             rec_str = p.recovery_time_utc if p.recovered else "Unrecovered"
             lines.append(f"    {p.start_time_utc} to {rec_str} | DD: {p.drawdown_pct*100:.2f}% | Dur: {p.duration_points}")

    if analytics.warnings:
         lines.append("  Warnings:")
         for w in analytics.warnings:
             lines.append(f"   - {w}")
    return "\n".join(lines)
