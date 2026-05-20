from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowPortfolioState, ShadowFill, ShadowPnLSnapshot, create_shadow_pnl_snapshot_id, get_utc_now_str
)

def build_shadow_pnl_snapshot(portfolio: ShadowPortfolioState, starting_equity_usd: float, trade_count: int = 0) -> ShadowPnLSnapshot:
    total_pnl = portfolio.equity_usd - starting_equity_usd
    return ShadowPnLSnapshot(
        snapshot_id=create_shadow_pnl_snapshot_id(),
        created_at_utc=get_utc_now_str(),
        equity_usd=portfolio.equity_usd,
        cash_usd=portfolio.cash_usd,
        realized_pnl_usd=portfolio.realized_pnl_usd,
        unrealized_pnl_usd=portfolio.unrealized_pnl_usd,
        total_pnl_usd=total_pnl,
        return_pct=calculate_shadow_return_pct(portfolio.equity_usd, starting_equity_usd),
        max_drawdown_pct=0.0, # Simplified
        trade_count=trade_count,
        warnings=[],
        errors=[]
    )

def update_shadow_pnl_after_fills(portfolio: ShadowPortfolioState, fills: List[ShadowFill], starting_equity_usd: float) -> ShadowPnLSnapshot:
    trade_count = sum(1 for f in fills if f.status == "SIMULATED_FILLED")
    return build_shadow_pnl_snapshot(portfolio, starting_equity_usd, trade_count)

def calculate_shadow_return_pct(equity_usd: float, starting_equity_usd: float) -> float | None:
    if starting_equity_usd <= 0:
        return None
    return ((equity_usd - starting_equity_usd) / starting_equity_usd) * 100.0

def calculate_shadow_drawdown_pct(snapshots: List[ShadowPnLSnapshot]) -> float | None:
    if not snapshots:
        return 0.0
    # Simplified mock calculation
    return 0.0

def shadow_pnl_summary(snapshots: List[ShadowPnLSnapshot]) -> Dict[str, Any]:
    if not snapshots:
        return {"count": 0}
    last = snapshots[-1]
    return {
        "count": len(snapshots),
        "latest_equity_usd": last.equity_usd,
        "total_pnl_usd": last.total_pnl_usd,
        "return_pct": last.return_pct
    }

def shadow_pnl_to_text(snapshots: List[ShadowPnLSnapshot], limit: int = 50) -> str:
    s = shadow_pnl_summary(snapshots)
    if s["count"] == 0:
        return "ShadowPnL(empty)"
    return f"ShadowPnL(count={s['count']}, eq={s['latest_equity_usd']:.2f}, ret={s['return_pct']:.2f}%)"
