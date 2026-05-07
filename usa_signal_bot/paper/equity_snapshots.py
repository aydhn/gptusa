from typing import Any, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.paper.paper_models import (
    VirtualAccount,
    PaperPosition,
    PaperEquitySnapshot,
    create_paper_snapshot_id
)
from usa_signal_bot.core.enums import PaperPositionSide

def create_paper_equity_snapshot(
    account: VirtualAccount,
    positions: List[PaperPosition],
    prices: Dict[str, float],
    timestamp_utc: str
) -> PaperEquitySnapshot:

    gross_exposure = calculate_paper_gross_exposure(positions, prices)
    net_exposure = calculate_paper_net_exposure(positions, prices)
    unrealized_pnl = calculate_paper_unrealized_pnl_total(positions, prices)

    total_market_value = sum([p.quantity * prices.get(p.symbol, p.market_price or p.average_price) for p in positions if p.side != PaperPositionSide.FLAT])
    equity = account.cash + total_market_value

    open_positions_count = sum(1 for p in positions if p.side != PaperPositionSide.FLAT and p.quantity > 0)

    return PaperEquitySnapshot(
        snapshot_id=create_paper_snapshot_id(),
        account_id=account.account_id,
        timestamp_utc=timestamp_utc,
        cash=account.cash,
        equity=equity,
        realized_pnl=account.realized_pnl,
        unrealized_pnl=unrealized_pnl,
        gross_exposure=gross_exposure,
        net_exposure=net_exposure,
        open_positions=open_positions_count
    )

def calculate_paper_gross_exposure(positions: List[PaperPosition], prices: Dict[str, float]) -> float:
    exposure = 0.0
    for p in positions:
        if p.side == PaperPositionSide.FLAT or p.quantity <= 0:
            continue
        price = prices.get(p.symbol, p.market_price)
        if price is None:
            price = p.average_price
        exposure += abs(p.quantity * price)
    return exposure

def calculate_paper_net_exposure(positions: List[PaperPosition], prices: Dict[str, float]) -> float:
    exposure = 0.0
    for p in positions:
        if p.side == PaperPositionSide.FLAT or p.quantity <= 0:
            continue
        price = prices.get(p.symbol, p.market_price)
        if price is None:
            price = p.average_price
        val = p.quantity * price
        if p.side == PaperPositionSide.LONG:
            exposure += val
        elif p.side == PaperPositionSide.SHORT_RESERVED:
            exposure -= val
    return exposure

def calculate_paper_unrealized_pnl_total(positions: List[PaperPosition], prices: Dict[str, float]) -> float:
    pnl = 0.0
    for p in positions:
        if p.side == PaperPositionSide.FLAT or p.quantity <= 0:
            continue
        price = prices.get(p.symbol, p.market_price)
        if price is None:
            continue
        if p.side == PaperPositionSide.LONG:
            pnl += (price - p.average_price) * p.quantity
    return pnl

def paper_equity_snapshots_to_text(snapshots: List[PaperEquitySnapshot], limit: int = 20) -> str:
    lines = ["--- EQUITY SNAPSHOTS ---"]
    if not snapshots:
        lines.append("No snapshots.")
        return "\n".join(lines)
    sorted_snaps = sorted(snapshots, key=lambda x: x.timestamp_utc)
    display_snaps = sorted_snaps[-limit:] if len(sorted_snaps) > limit else sorted_snaps
    if len(sorted_snaps) > limit:
        lines.append(f"... {len(sorted_snaps) - limit} earlier snapshots hidden")
    for s in display_snaps:
        lines.append(
            f"{s.timestamp_utc} | Eq: ${s.equity:,.2f} | Cash: ${s.cash:,.2f} | "
            f"rPnL: ${s.realized_pnl:,.2f} | uPnL: ${s.unrealized_pnl:,.2f} | "
            f"Exp: ${s.gross_exposure:,.2f} | Pos: {s.open_positions}"
        )
    return "\n".join(lines)

def paper_equity_curve_from_snapshots(snapshots: List[PaperEquitySnapshot]) -> List[Dict[str, Any]]:
    sorted_snaps = sorted(snapshots, key=lambda x: x.timestamp_utc)
    return [
        {
            "timestamp_utc": s.timestamp_utc,
            "equity": s.equity,
            "cash": s.cash
        }
        for s in sorted_snaps
    ]
