from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import PaperOrderSide, PaperFillStatus
from usa_signal_bot.paper.paper_models import PaperOrder, PaperFill, create_paper_fill_id
from usa_signal_bot.data.models import OHLCVBar

@dataclass
class PaperFillConfig:
    fee_bps: float
    slippage_bps: float
    allow_partial_fills: bool
    max_fill_quantity_per_order: Optional[float] = None

def default_paper_fill_config() -> PaperFillConfig:
    return PaperFillConfig(
        fee_bps=1.0,
        slippage_bps=2.0,
        allow_partial_fills=False
    )

def validate_paper_fill_config(config: PaperFillConfig) -> None:
    if config.fee_bps < 0:
        raise ValueError("fee_bps cannot be negative")
    if config.slippage_bps < 0:
        raise ValueError("slippage_bps cannot be negative")

def calculate_paper_fill_price(side: PaperOrderSide, base_price: float, slippage_bps: float) -> float:
    # Slippage is against our favor
    # If we buy, price goes up. If we sell, price goes down.
    slippage_factor = slippage_bps / 10000.0
    if side == PaperOrderSide.BUY:
        return base_price * (1.0 + slippage_factor)
    elif side == PaperOrderSide.SELL:
        return base_price * (1.0 - slippage_factor)
    return base_price

def calculate_paper_fill_fees(gross_notional: float, fee_bps: float) -> float:
    return gross_notional * (fee_bps / 10000.0)

def calculate_paper_net_cash_impact(side: PaperOrderSide, gross_notional: float, fees: float) -> float:
    # BUY means we spend cash (negative impact)
    # SELL means we receive cash (positive impact)
    # Fees always reduce cash
    if side == PaperOrderSide.BUY:
        return -gross_notional - fees
    elif side == PaperOrderSide.SELL:
        return gross_notional - fees
    return 0.0

def simulate_paper_fill(order: PaperOrder, price: float, config: Optional[PaperFillConfig] = None) -> PaperFill:
    config = config or default_paper_fill_config()
    validate_paper_fill_config(config)

    intent = order.intent

    fill_price = calculate_paper_fill_price(intent.side, price, config.slippage_bps)
    gross_notional = intent.quantity * fill_price
    fees = calculate_paper_fill_fees(gross_notional, config.fee_bps)
    net_cash_impact = calculate_paper_net_cash_impact(intent.side, gross_notional, fees)

    # Calculate slippage cost explicitly for reporting
    base_notional = intent.quantity * price
    slippage_cost = abs(gross_notional - base_notional)

    return PaperFill(
        fill_id=create_paper_fill_id(),
        order_id=order.order_id,
        account_id=order.account_id,
        symbol=intent.symbol,
        timeframe=intent.timeframe,
        side=intent.side,
        quantity=intent.quantity,
        fill_price=fill_price,
        gross_notional=gross_notional,
        fees=fees,
        slippage_cost=slippage_cost,
        net_cash_impact=net_cash_impact,
        status=PaperFillStatus.FILLED,
        filled_at_utc=datetime.now(timezone.utc).isoformat()
    )

def simulate_paper_fill_from_bar(order: PaperOrder, bar: OHLCVBar, config: Optional[PaperFillConfig] = None) -> PaperFill:
    intent = order.intent

    # Determine the base price based on order type
    if intent.order_type.value == "NEXT_OPEN" or intent.order_type == "NEXT_OPEN":
        base_price = bar.open
    elif intent.order_type.value == "NEXT_CLOSE" or intent.order_type == "NEXT_CLOSE":
        base_price = bar.close
    else:
        # Fallback to close for MARKET
        base_price = bar.close

    return simulate_paper_fill(order, base_price, config)

def paper_fill_summary(fill: PaperFill) -> Dict[str, Any]:
    return {
        "fill_id": fill.fill_id,
        "symbol": fill.symbol,
        "side": fill.side.value if hasattr(fill.side, 'value') else fill.side,
        "quantity": fill.quantity,
        "fill_price": round(fill.fill_price, 2),
        "gross_notional": round(fill.gross_notional, 2),
        "fees": round(fill.fees, 2),
        "net_cash_impact": round(fill.net_cash_impact, 2)
    }

def paper_fill_to_text(fill: PaperFill) -> str:
    side_str = fill.side.value if hasattr(fill.side, 'value') else fill.side
    return f"FILL {fill.fill_id} | {side_str} {fill.quantity} {fill.symbol} @ ${fill.fill_price:,.2f} | Net Cash: ${fill.net_cash_impact:,.2f} | Fees: ${fill.fees:,.2f}"
