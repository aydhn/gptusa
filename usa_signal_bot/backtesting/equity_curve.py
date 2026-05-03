"""Equity curve models for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolioSnapshot
from usa_signal_bot.core.exceptions import BacktestMetricError

@dataclass
class EquityCurvePoint:
    """A point on the equity curve."""
    timestamp_utc: str
    equity: float
    cash: float
    realized_pnl: float
    unrealized_pnl: float
    drawdown: float
    drawdown_pct: float

@dataclass
class EquityCurve:
    """The equity curve of a backtest run."""
    points: list[EquityCurvePoint]
    starting_cash: float
    ending_equity: float | None
    max_drawdown: float | None
    max_drawdown_pct: float | None

def calculate_drawdowns(equity_values: list[float]) -> list[tuple[float, float]]:
    drawdowns = []
    peak = 0.0
    for value in equity_values:
        if value > peak:
            peak = value

        if peak > 0:
            dd = peak - value
            dd_pct = dd / peak
        else:
            dd = 0.0
            dd_pct = 0.0

        drawdowns.append((dd, dd_pct))
    return drawdowns

def build_equity_curve_from_snapshots(snapshots: list[BacktestPortfolioSnapshot], starting_cash: float) -> EquityCurve:
    if not snapshots:
        return EquityCurve(
            points=[],
            starting_cash=starting_cash,
            ending_equity=starting_cash,
            max_drawdown=0.0,
            max_drawdown_pct=0.0
        )

    equity_values = [s.equity for s in snapshots]
    drawdowns = calculate_drawdowns(equity_values)

    points = []
    max_dd = 0.0
    max_dd_pct = 0.0

    for snapshot, (dd, dd_pct) in zip(snapshots, drawdowns):
        points.append(
            EquityCurvePoint(
                timestamp_utc=snapshot.timestamp_utc,
                equity=snapshot.equity,
                cash=snapshot.cash,
                realized_pnl=snapshot.realized_pnl,
                unrealized_pnl=snapshot.unrealized_pnl,
                drawdown=dd,
                drawdown_pct=dd_pct
            )
        )
        if dd > max_dd:
            max_dd = dd
        if dd_pct > max_dd_pct:
            max_dd_pct = dd_pct

    return EquityCurve(
        points=points,
        starting_cash=starting_cash,
        ending_equity=snapshots[-1].equity,
        max_drawdown=max_dd,
        max_drawdown_pct=max_dd_pct
    )

def equity_curve_to_dict(curve: EquityCurve) -> dict:
    return {
        "starting_cash": curve.starting_cash,
        "ending_equity": curve.ending_equity,
        "max_drawdown": curve.max_drawdown,
        "max_drawdown_pct": curve.max_drawdown_pct,
        "points": [
            {
                "timestamp_utc": p.timestamp_utc,
                "equity": p.equity,
                "cash": p.cash,
                "realized_pnl": p.realized_pnl,
                "unrealized_pnl": p.unrealized_pnl,
                "drawdown": p.drawdown,
                "drawdown_pct": p.drawdown_pct
            }
            for p in curve.points
        ]
    }

def equity_curve_to_text(curve: EquityCurve) -> str:
    lines = [
        "=== Equity Curve Summary ===",
        f"Starting Cash:    ${curve.starting_cash:.2f}",
        f"Ending Equity:    ${curve.ending_equity:.2f}" if curve.ending_equity else "Ending Equity:    N/A",
        f"Max Drawdown:     ${curve.max_drawdown:.2f}" if curve.max_drawdown else "Max Drawdown:     N/A",
        f"Max Drawdown %:   {(curve.max_drawdown_pct * 100):.2f}%" if curve.max_drawdown_pct is not None else "Max Drawdown %:   N/A",
        f"Points Recorded:  {len(curve.points)}"
    ]
    return "\n".join(lines)

def validate_equity_curve(curve: EquityCurve) -> None:
    if curve.starting_cash < 0:
        raise BacktestMetricError("starting_cash cannot be negative")
    if curve.max_drawdown is not None and curve.max_drawdown < 0:
        raise BacktestMetricError("max_drawdown cannot be negative")
    if curve.max_drawdown_pct is not None and (curve.max_drawdown_pct < 0 or curve.max_drawdown_pct > 1):
        raise BacktestMetricError("max_drawdown_pct must be between 0.0 and 1.0")
