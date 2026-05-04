from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from usa_signal_bot.core.enums import AttributionDimension, AttributionStatus
from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade

@dataclass
class AttributionRow:
    dimension: AttributionDimension
    key: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: Optional[float]
    gross_pnl: float
    net_pnl: float
    total_fees: float
    average_trade_pnl: Optional[float]
    contribution_pct: Optional[float]
    best_trade: Optional[float]
    worst_trade: Optional[float]
    warnings: list[str] = field(default_factory=list)

@dataclass
class AttributionReport:
    report_id: str
    created_at_utc: str
    status: AttributionStatus
    strategy_run_id: Optional[str]
    rows: list[AttributionRow]
    total_net_pnl: float
    dimensions: list[AttributionDimension]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def attribution_key_for_trade(trade: BacktestTrade, dimension: AttributionDimension) -> str:
    if dimension == AttributionDimension.STRATEGY:
        parts = trade.trade_id.split('_')
        return parts[0] if len(parts) > 0 else "UNKNOWN"
    elif dimension == AttributionDimension.SYMBOL:
        return trade.symbol
    elif dimension == AttributionDimension.TIMEFRAME:
        return trade.timeframe
    elif dimension == AttributionDimension.ACTION:
        return trade.direction.value if hasattr(trade.direction, 'value') else str(trade.direction)
    elif dimension == AttributionDimension.MONTH:
        ts = trade.exit_time_utc or trade.entry_time_utc
        return ts[:7] if ts and len(ts) >= 7 else "UNKNOWN"
    elif dimension == AttributionDimension.YEAR:
        ts = trade.exit_time_utc or trade.entry_time_utc
        return ts[:4] if ts and len(ts) >= 4 else "UNKNOWN"
    elif dimension == AttributionDimension.HOLDING_PERIOD:
        bars = trade.holding_bars
        if bars is None:
            return "UNKNOWN"
        if bars <= 1:
            return "0-1"
        elif bars <= 5:
            return "2-5"
        elif bars <= 20:
            return "6-20"
        else:
            return "21+"
    return "UNKNOWN"

def build_attribution_by_dimension(ledger: TradeLedger, dimension: AttributionDimension) -> list[AttributionRow]:
    if not ledger.trades:
        return []

    grouped = {}
    for t in ledger.trades:
        # TradeStatus string comparisons in a safe manner
        status_val = t.status.value if hasattr(t.status, "value") else t.status
        if status_val != "CLOSED" and status_val != "PARTIAL":
            continue

        key = attribution_key_for_trade(t, dimension)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(t)

    rows = []
    for key, trades in grouped.items():
        total = len(trades)
        wins = sum(1 for t in trades if t.net_pnl > 0)
        losses = sum(1 for t in trades if t.net_pnl < 0)
        win_rate = (wins / total) * 100.0 if total > 0 else 0.0

        gross = sum(t.gross_pnl for t in trades)
        net = sum(t.net_pnl for t in trades)
        fees = sum(t.total_fees + t.total_slippage_cost for t in trades)

        avg_pnl = net / total if total > 0 else 0.0

        best = max(t.net_pnl for t in trades) if trades else 0.0
        worst = min(t.net_pnl for t in trades) if trades else 0.0

        rows.append(AttributionRow(
            dimension=dimension,
            key=key,
            total_trades=total,
            winning_trades=wins,
            losing_trades=losses,
            win_rate=win_rate,
            gross_pnl=gross,
            net_pnl=net,
            total_fees=fees,
            average_trade_pnl=avg_pnl,
            contribution_pct=None,
            best_trade=best,
            worst_trade=worst
        ))

    return rows

def calculate_attribution_contribution(rows: list[AttributionRow], total_net_pnl: float) -> list[AttributionRow]:
    for r in rows:
        if total_net_pnl != 0:
            r.contribution_pct = (r.net_pnl / abs(total_net_pnl)) * 100.0
        else:
            r.contribution_pct = 0.0 if r.net_pnl == 0 else None
    return rows

def build_full_attribution_report(
    ledger: TradeLedger,
    strategy_run_id: Optional[str] = None,
    dimensions: Optional[list[AttributionDimension]] = None
) -> AttributionReport:
    if dimensions is None:
        dimensions = [
            AttributionDimension.STRATEGY,
            AttributionDimension.SYMBOL,
            AttributionDimension.TIMEFRAME,
            AttributionDimension.MONTH
        ]

    if not ledger.trades:
        return AttributionReport(
            report_id=f"attr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            created_at_utc=datetime.now().isoformat(),
            status=AttributionStatus.EMPTY,
            strategy_run_id=strategy_run_id,
            rows=[],
            total_net_pnl=0.0,
            dimensions=dimensions,
            warnings=["Ledger is empty"],
            errors=[]
        )

    total_net = sum(t.net_pnl for t in ledger.trades if (t.status.value if hasattr(t.status, "value") else t.status) in ["CLOSED", "PARTIAL"])
    all_rows = []

    for dim in dimensions:
        dim_rows = build_attribution_by_dimension(ledger, dim)
        dim_rows = calculate_attribution_contribution(dim_rows, total_net)
        all_rows.extend(dim_rows)

    status = AttributionStatus.OK if all_rows else AttributionStatus.EMPTY

    return AttributionReport(
        report_id=f"attr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        created_at_utc=datetime.now().isoformat(),
        status=status,
        strategy_run_id=strategy_run_id,
        rows=all_rows,
        total_net_pnl=total_net,
        dimensions=dimensions
    )

def attribution_row_to_dict(row: AttributionRow) -> dict:
    return {
        "dimension": row.dimension.value if hasattr(row.dimension, "value") else row.dimension,
        "key": row.key,
        "total_trades": row.total_trades,
        "winning_trades": row.winning_trades,
        "losing_trades": row.losing_trades,
        "win_rate": row.win_rate,
        "gross_pnl": row.gross_pnl,
        "net_pnl": row.net_pnl,
        "total_fees": row.total_fees,
        "average_trade_pnl": row.average_trade_pnl,
        "contribution_pct": row.contribution_pct,
        "best_trade": row.best_trade,
        "worst_trade": row.worst_trade,
        "warnings": row.warnings
    }

def attribution_report_to_dict(report: AttributionReport) -> dict:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "status": report.status.value if hasattr(report.status, "value") else report.status,
        "strategy_run_id": report.strategy_run_id,
        "rows": [attribution_row_to_dict(r) for r in report.rows],
        "total_net_pnl": report.total_net_pnl,
        "dimensions": [d.value if hasattr(d, "value") else d for d in report.dimensions],
        "warnings": report.warnings,
        "errors": report.errors
    }

def attribution_report_to_text(report: AttributionReport, limit: int = 30) -> str:
    if not report.rows:
        return "Performance Attribution Report (EMPTY)"

    lines = [f"Performance Attribution Report (Total PnL: ${report.total_net_pnl:.2f})"]

    for dim in report.dimensions:
        dim_rows = [r for r in report.rows if r.dimension == dim]
        if not dim_rows:
            continue

        dim_name = dim.value if hasattr(dim, "value") else dim
        lines.append(f"\n--- Dimension: {dim_name} ---")
        lines.append(f"{'Key':<15} | {'Trades':<6} | {'Win%':<6} | {'NetPnL':<10} | {'Contrib%':<8}")
        lines.append("-" * 55)

        dim_rows.sort(key=lambda x: x.net_pnl, reverse=True)

        for r in dim_rows[:limit]:
            win_r = f"{r.win_rate:.1f}" if r.win_rate is not None else "N/A"
            cont = f"{r.contribution_pct:.1f}" if r.contribution_pct is not None else "N/A"
            lines.append(f"{r.key:<15} | {r.total_trades:<6} | {win_r:<6} | {r.net_pnl:<10.2f} | {cont:<8}")

    return "\n".join(lines)
