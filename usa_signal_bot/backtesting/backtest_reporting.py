"""Reporting functions for backtest results."""
from pathlib import Path
from usa_signal_bot.backtesting.backtest_engine import BacktestRunResult
from usa_signal_bot.backtesting.backtest_validation import BacktestValidationReport, backtest_validation_report_to_text
from usa_signal_bot.backtesting.backtest_metrics import backtest_metrics_to_text
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolioSnapshot
import json

def save_json(data: dict, path: Path) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def backtest_summary_to_text(result: BacktestRunResult) -> str:
    lines = [
        "=== Backtest Run Summary ===",
        f"Run ID:           {result.run_id}",
        f"Run Name:         {result.run_name}",
        f"Status:           {result.status.value}",
        f"Created At:       {result.created_at_utc}",
        f"Symbols Tested:   {len(result.request.symbols)}",
        f"Timeframe:        {result.request.timeframe}",
    ]
    return "\n".join(lines)

def fills_to_text(fills: list[BacktestFill], limit: int = 20) -> str:
    if not fills:
        return "No fills recorded."

    lines = [f"=== Fills (Showing latest {min(limit, len(fills))}) ==="]
    for fill in fills[-limit:]:
        lines.append(f"{fill.timestamp_utc} | {fill.symbol} | {fill.side.value} | {fill.quantity:.4f} @ ${fill.fill_price:.2f} | Fees: ${fill.fees:.2f}")
    return "\n".join(lines)

def orders_to_text(orders: list[BacktestOrderIntent], limit: int = 20) -> str:
    if not orders:
        return "No orders recorded."

    lines = [f"=== Orders (Showing latest {min(limit, len(orders))}) ==="]
    for order in orders[-limit:]:
        lines.append(f"{order.timestamp_utc} | {order.symbol} | {order.side.value} | {order.quantity:.4f} | Type: {order.order_type.value}")
    return "\n".join(lines)

def snapshots_to_text(snapshots: list[BacktestPortfolioSnapshot], limit: int = 10) -> str:
    if not snapshots:
        return "No snapshots recorded."

    if len(snapshots) > limit:
        step = len(snapshots) / limit
        indices = [int(i * step) for i in range(limit)]
        if len(snapshots) - 1 not in indices:
            indices[-1] = len(snapshots) - 1
        sampled = [snapshots[i] for i in indices]
    else:
        sampled = snapshots

    lines = [f"=== Portfolio Progression (Showing {len(sampled)} points) ==="]
    for s in sampled:
        lines.append(f"{s.timestamp_utc} | Eq: ${s.equity:.2f} | Cash: ${s.cash:.2f} | Gross Exp: ${s.gross_exposure:.2f} | Open: {s.open_positions}")
    return "\n".join(lines)

def backtest_run_result_to_text(result: BacktestRunResult) -> str:
    sections = [
        backtest_summary_to_text(result),
        backtest_metrics_to_text(result.metrics),
        fills_to_text(result.fills, 10),
        snapshots_to_text(result.snapshots, 10),
        "*** NOTE: Backtest results are not a guarantee of future performance. ***",
        "*** Phase 25 runs use simple NEXT_OPEN fills and exclude slippage/market impact. ***"
    ]
    return "\n\n".join(sections)

def write_backtest_report_json(
    path: Path,
    result: BacktestRunResult,
    validation_report: BacktestValidationReport | None = None
) -> Path:
    d = {
        "run_id": result.run_id,
        "run_name": result.run_name,
        "status": result.status.value,
        "metrics": result.metrics.__dict__,
        "validation_passed": validation_report.valid if validation_report else None,
        "validation_issues": [i.__dict__ for i in validation_report.issues] if validation_report else []
    }
    d["metrics"]["status"] = d["metrics"]["status"].value

    save_json(d, path)
    return path
