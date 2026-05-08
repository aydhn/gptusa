from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import uuid

from usa_signal_bot.core.enums import MatchStatus

@dataclass
class MatchedOrderFillPair:
    match_id: str
    symbol: str
    paper_order_id: Optional[str]
    backtest_order_id: Optional[str]
    paper_fill_id: Optional[str]
    backtest_fill_id: Optional[str]
    match_status: MatchStatus
    paper_quantity: Optional[float]
    backtest_quantity: Optional[float]
    quantity_gap: Optional[float]
    paper_fill_price: Optional[float]
    backtest_fill_price: Optional[float]
    fill_price_gap_pct: Optional[float]
    paper_fees: Optional[float]
    backtest_fees: Optional[float]
    fee_gap: Optional[float]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def match_order_fills(paper_orders: List[Dict[str, Any]], paper_fills: List[Dict[str, Any]], backtest_orders: List[Dict[str, Any]], backtest_fills: List[Dict[str, Any]]) -> List[MatchedOrderFillPair]:
    pairs = []
    # This is a stub for complex fill matching which might involve comparing quantities,
    # exact fill times, sides, etc. For this basic implementation we just build unmatched pairs.
    for p_fill in paper_fills:
        pairs.append(build_order_fill_pair(None, p_fill, None, None, MatchStatus.PAPER_ONLY))
    for b_fill in backtest_fills:
        pairs.append(build_order_fill_pair(None, None, None, b_fill, MatchStatus.BACKTEST_ONLY))
    return pairs

def build_order_fill_pair(paper_order: Optional[Dict[str, Any]], paper_fill: Optional[Dict[str, Any]], backtest_order: Optional[Dict[str, Any]], backtest_fill: Optional[Dict[str, Any]], status: MatchStatus) -> MatchedOrderFillPair:
    symbol = "unknown"
    if paper_fill: symbol = paper_fill.get("symbol", symbol)
    elif backtest_fill: symbol = backtest_fill.get("symbol", symbol)

    p_price = paper_fill.get("fill_price") if paper_fill else None
    b_price = backtest_fill.get("fill_price") if backtest_fill else None

    p_qty = paper_fill.get("quantity") if paper_fill else None
    b_qty = backtest_fill.get("quantity") if backtest_fill else None

    p_fee = paper_fill.get("fees") if paper_fill else None
    b_fee = backtest_fill.get("fees") if backtest_fill else None

    return MatchedOrderFillPair(
        match_id=f"fill_match_{uuid.uuid4().hex[:8]}",
        symbol=symbol,
        paper_order_id=paper_order.get("order_id") if paper_order else None,
        backtest_order_id=backtest_order.get("order_id") if backtest_order else None,
        paper_fill_id=paper_fill.get("fill_id") if paper_fill else None,
        backtest_fill_id=backtest_fill.get("fill_id") if backtest_fill else None,
        match_status=status,
        paper_quantity=p_qty,
        backtest_quantity=b_qty,
        quantity_gap=calculate_quantity_gap(p_qty, b_qty),
        paper_fill_price=p_price,
        backtest_fill_price=b_price,
        fill_price_gap_pct=calculate_fill_price_gap_pct(p_price, b_price),
        paper_fees=p_fee,
        backtest_fees=b_fee,
        fee_gap=(p_fee - b_fee) if p_fee is not None and b_fee is not None else None,
        warnings=[],
        errors=[]
    )

def calculate_fill_price_gap_pct(paper_price: Optional[float], backtest_price: Optional[float]) -> Optional[float]:
    if paper_price is None or backtest_price is None or backtest_price == 0:
        return None
    return ((paper_price - backtest_price) / backtest_price) * 100.0

def calculate_quantity_gap(paper_quantity: Optional[float], backtest_quantity: Optional[float]) -> Optional[float]:
    if paper_quantity is None or backtest_quantity is None:
        return None
    return paper_quantity - backtest_quantity

def matched_order_fill_pair_to_dict(pair: MatchedOrderFillPair) -> dict:
    from dataclasses import asdict
    d = asdict(pair)
    if isinstance(d.get("match_status"), MatchStatus):
        d["match_status"] = d["match_status"].value
    return d

def matched_order_fills_to_text(pairs: List[MatchedOrderFillPair], limit: int = 30) -> str:
    lines = [f"Matched Fills (Showing up to {limit}):"]
    for p in pairs[:limit]:
        lines.append(f"  [{p.match_status.value}] {p.symbol}")
        if p.fill_price_gap_pct is not None:
            lines.append(f"    Price Gap: {p.fill_price_gap_pct:.2f}%")
    return "\n".join(lines)
