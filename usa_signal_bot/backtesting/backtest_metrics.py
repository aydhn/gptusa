"""Metrics for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import BacktestMetricStatus, BacktestOrderSide
from usa_signal_bot.backtesting.equity_curve import EquityCurve
from usa_signal_bot.backtesting.fill_models import BacktestFill

@dataclass
class BacktestMetrics:
    status: BacktestMetricStatus
    starting_cash: float
    ending_equity: float
    total_return: float
    total_return_pct: float
    max_drawdown: float
    max_drawdown_pct: float
    total_fills: int
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float | None
    average_trade_pnl: float | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def estimate_trades_from_fills(fills: list[BacktestFill]) -> list[dict[str, Any]]:
    trades = []
    open_buys: dict[str, list[BacktestFill]] = {}

    for fill in fills:
        if fill.side == BacktestOrderSide.BUY:
            if fill.symbol not in open_buys:
                open_buys[fill.symbol] = []
            open_buys[fill.symbol].append(fill)
        elif fill.side == BacktestOrderSide.SELL:
            buys = open_buys.get(fill.symbol, [])
            if buys:
                buy = buys.pop(0)
                matched_qty = min(buy.quantity, fill.quantity)
                buy_val = matched_qty * buy.fill_price
                sell_val = matched_qty * fill.fill_price
                fees = (buy.fees * (matched_qty / buy.quantity)) + (fill.fees * (matched_qty / fill.quantity))

                pnl = sell_val - buy_val - fees

                trades.append({
                    "symbol": fill.symbol,
                    "entry_time": buy.timestamp_utc,
                    "exit_time": fill.timestamp_utc,
                    "quantity": matched_qty,
                    "pnl": pnl,
                    "is_win": pnl > 0
                })
    return trades

def calculate_win_rate(trades: list[dict[str, Any]]) -> float | None:
    if not trades:
        return None
    wins = sum(1 for t in trades if t["is_win"])
    return wins / len(trades)

def calculate_basic_backtest_metrics(
    starting_cash: float,
    equity_curve: EquityCurve,
    fills: list[BacktestFill]
) -> BacktestMetrics:
    warnings = []
    errors = []
    status = BacktestMetricStatus.OK

    ending_equity = equity_curve.ending_equity if equity_curve.ending_equity is not None else starting_cash

    total_return = ending_equity - starting_cash
    total_return_pct = total_return / starting_cash if starting_cash > 0 else 0.0

    max_dd = equity_curve.max_drawdown or 0.0
    max_dd_pct = equity_curve.max_drawdown_pct or 0.0

    total_fills = len(fills)
    if total_fills == 0:
        warnings.append("No fills recorded. Backtest resulted in 0 trades.")
        status = BacktestMetricStatus.EMPTY

    trades = estimate_trades_from_fills(fills)
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t["is_win"])
    losing_trades = total_trades - winning_trades

    win_rate = calculate_win_rate(trades)
    average_pnl = sum(t["pnl"] for t in trades) / total_trades if total_trades > 0 else None

    return BacktestMetrics(
        status=status,
        starting_cash=starting_cash,
        ending_equity=ending_equity,
        total_return=total_return,
        total_return_pct=total_return_pct,
        max_drawdown=max_dd,
        max_drawdown_pct=max_dd_pct,
        total_fills=total_fills,
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        win_rate=win_rate,
        average_trade_pnl=average_pnl,
        warnings=warnings,
        errors=errors
    )

def backtest_metrics_to_dict(metrics: BacktestMetrics) -> dict:
    return {
        "status": metrics.status.value,
        "starting_cash": metrics.starting_cash,
        "ending_equity": metrics.ending_equity,
        "total_return": metrics.total_return,
        "total_return_pct": metrics.total_return_pct,
        "max_drawdown": metrics.max_drawdown,
        "max_drawdown_pct": metrics.max_drawdown_pct,
        "total_fills": metrics.total_fills,
        "total_trades": metrics.total_trades,
        "winning_trades": metrics.winning_trades,
        "losing_trades": metrics.losing_trades,
        "win_rate": metrics.win_rate,
        "average_trade_pnl": metrics.average_trade_pnl,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def backtest_metrics_to_text(metrics: BacktestMetrics) -> str:
    lines = [
        "=== Backtest Metrics ===",
        f"Status:             {metrics.status.value}",
        f"Starting Cash:      ${metrics.starting_cash:.2f}",
        f"Ending Equity:      ${metrics.ending_equity:.2f}",
        f"Total Return:       ${metrics.total_return:.2f}",
        f"Total Return %:     {(metrics.total_return_pct * 100):.2f}%",
        f"Max Drawdown:       ${metrics.max_drawdown:.2f}",
        f"Max Drawdown %:     {(metrics.max_drawdown_pct * 100):.2f}%",
        f"Total Fills:        {metrics.total_fills}",
        f"Estimated Trades:   {metrics.total_trades}",
        f"Winning Trades:     {metrics.winning_trades}",
        f"Losing Trades:      {metrics.losing_trades}",
    ]
    if metrics.win_rate is not None:
        lines.append(f"Win Rate:           {(metrics.win_rate * 100):.2f}%")
    if metrics.average_trade_pnl is not None:
        lines.append(f"Avg Trade PnL:      ${metrics.average_trade_pnl:.2f}")

    if metrics.warnings:
        lines.append("\nWarnings:")
        for w in metrics.warnings:
            lines.append(f"  - {w}")

    if metrics.errors:
        lines.append("\nErrors:")
        for e in metrics.errors:
            lines.append(f"  - {e}")

    return "\n".join(lines)
