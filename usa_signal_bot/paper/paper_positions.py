from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from usa_signal_bot.core.enums import PaperPositionSide, PaperOrderSide
from usa_signal_bot.paper.paper_models import PaperPosition, PaperFill

def create_flat_paper_position(symbol: str) -> PaperPosition:
    return PaperPosition(
        symbol=symbol,
        side=PaperPositionSide.FLAT,
        quantity=0.0,
        average_price=0.0,
        market_price=None,
        market_value=0.0,
        realized_pnl=0.0,
        unrealized_pnl=0.0,
        opened_at_utc=None,
        updated_at_utc=datetime.now(timezone.utc).isoformat()
    )

def update_paper_position_with_fill(position: Optional[PaperPosition], fill: PaperFill) -> PaperPosition:
    if not position:
        position = create_flat_paper_position(fill.symbol)

    now_utc = fill.filled_at_utc or datetime.now(timezone.utc).isoformat()

    if fill.side == PaperOrderSide.BUY:
        if position.side in [PaperPositionSide.FLAT, PaperPositionSide.LONG]:
            new_qty = position.quantity + fill.quantity
            if new_qty > 0:
                current_cost = position.quantity * position.average_price
                new_cost = fill.quantity * fill.fill_price
                position.average_price = (current_cost + new_cost) / new_qty

            position.quantity = new_qty
            position.side = PaperPositionSide.LONG
            if not position.opened_at_utc:
                position.opened_at_utc = now_utc
        else:
            pass

    elif fill.side == PaperOrderSide.SELL:
        if position.side == PaperPositionSide.LONG:
            pnl = (fill.fill_price - position.average_price) * fill.quantity
            position.realized_pnl += pnl

            new_qty = position.quantity - fill.quantity
            if new_qty <= 1e-6:
                position.quantity = 0.0
                position.side = PaperPositionSide.FLAT
                position.opened_at_utc = None
            else:
                position.quantity = new_qty
        else:
            pass

    position.updated_at_utc = now_utc
    position.market_price = fill.fill_price
    position.market_value = position.quantity * fill.fill_price

    if position.side == PaperPositionSide.LONG:
        position.unrealized_pnl = (position.market_price - position.average_price) * position.quantity
    else:
        position.unrealized_pnl = 0.0

    return position

def mark_paper_position_to_market(position: PaperPosition, market_price: float, timestamp_utc: Optional[str] = None) -> PaperPosition:
    position.market_price = market_price
    position.market_value = position.quantity * market_price

    if position.side == PaperPositionSide.LONG:
        position.unrealized_pnl = (market_price - position.average_price) * position.quantity
    elif position.side == PaperPositionSide.FLAT:
        position.unrealized_pnl = 0.0

    position.updated_at_utc = timestamp_utc or datetime.now(timezone.utc).isoformat()
    return position

def paper_position_market_value(position: PaperPosition, market_price: Optional[float] = None) -> float:
    price = market_price if market_price is not None else position.market_price
    if price is None:
        return 0.0
    return position.quantity * price

def calculate_paper_unrealized_pnl(position: PaperPosition, market_price: float) -> float:
    if position.side == PaperPositionSide.LONG:
        return (market_price - position.average_price) * position.quantity
    return 0.0

def close_paper_position_with_sell(position: PaperPosition, fill: PaperFill) -> Tuple[PaperPosition, float]:
    if position.side != PaperPositionSide.LONG:
        return position, 0.0

    pnl = (fill.fill_price - position.average_price) * fill.quantity
    updated_pos = update_paper_position_with_fill(position, fill)
    return updated_pos, pnl

def paper_positions_to_dict(positions: List[PaperPosition]) -> List[Dict[str, Any]]:
    from dataclasses import asdict
    return [asdict(p) for p in positions]

def paper_positions_to_text(positions: List[PaperPosition], limit: int = 30) -> str:
    lines = ["--- PAPER POSITIONS ---"]
    open_pos = [p for p in positions if p.side != PaperPositionSide.FLAT and p.quantity > 0]

    if not open_pos:
        lines.append("No open positions.")
        return "\n".join(lines)

    lines.append(f"Total Open: {len(open_pos)}")

    for p in open_pos[:limit]:
        side = p.side.value if hasattr(p.side, 'value') else p.side
        market = f"${p.market_price:,.2f}" if p.market_price else "Unknown"
        lines.append(
            f"{p.symbol} | {side} | Qty: {p.quantity:.4f} | "
            f"Avg: ${p.average_price:,.2f} | Mkt: {market} | "
            f"Value: ${p.market_value:,.2f} | uPnL: ${p.unrealized_pnl:,.2f}"
        )

    if len(open_pos) > limit:
        lines.append(f"... and {len(open_pos) - limit} more")

    return "\n".join(lines)
