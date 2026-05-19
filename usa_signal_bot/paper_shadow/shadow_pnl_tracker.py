from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowPnLSnapshot,
    ShadowPortfolioState,
    ShadowFill,
    create_shadow_pnl_snapshot_id
)

def build_shadow_pnl_snapshot(portfolio: ShadowPortfolioState, starting_equity_usd: float, trade_count: int = 0) -> ShadowPnLSnapshot:
    ret_pct = calculate_shadow_return_pct(portfolio.equity_usd, starting_equity_usd)
    return ShadowPnLSnapshot(
        snapshot_id=create_shadow_pnl_snapshot_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        equity_usd=portfolio.equity_usd,
        cash_usd=portfolio.cash_usd,
        realized_pnl_usd=portfolio.realized_pnl_usd,
        unrealized_pnl_usd=portfolio.unrealized_pnl_usd,
        total_pnl_usd=portfolio.equity_usd - starting_equity_usd,
        trade_count=trade_count,
        warnings=[],
        errors=[],
        return_pct=ret_pct,
        max_drawdown_pct=None
    )

def update_shadow_pnl_after_fills(portfolio: ShadowPortfolioState, fills: list[ShadowFill], starting_equity_usd: float) -> ShadowPnLSnapshot:
    trades = sum(1 for f in fills if f.filled_quantity > 0)
    return build_shadow_pnl_snapshot(portfolio, starting_equity_usd, trades)

def calculate_shadow_return_pct(equity_usd: float, starting_equity_usd: float) -> float | None:
    if starting_equity_usd <= 0:
        return None
    return ((equity_usd - starting_equity_usd) / starting_equity_usd) * 100

def calculate_shadow_drawdown_pct(snapshots: list[ShadowPnLSnapshot]) -> float | None:
    if not snapshots:
        return None
    peak = max((s.equity_usd for s in snapshots), default=0.0)
    current = snapshots[-1].equity_usd
    if peak <= 0:
        return None
    return ((peak - current) / peak) * 100

def shadow_pnl_summary(snapshots: list[ShadowPnLSnapshot]) -> dict[str, Any]:
    if not snapshots:
        return {"count": 0}
    last = snapshots[-1]
    return {
        "count": len(snapshots),
        "current_equity": last.equity_usd,
        "total_pnl": last.total_pnl_usd,
        "return_pct": last.return_pct
    }

def shadow_pnl_to_text(snapshots: list[ShadowPnLSnapshot], limit: int = 50) -> str:
    summary = shadow_pnl_summary(snapshots)
    if summary["count"] == 0:
        return "No Shadow PnL snapshots."
    text = "Shadow PnL Summary\n"
    text += f"Equity: ${summary['current_equity']:.2f}\n"
    text += f"Total PnL: ${summary['total_pnl']:.2f}\n"
    text += f"Return: {summary['return_pct']:.2f}%\n"
    text += "Note: Simulated performance is not a guarantee of future results."
    return text
