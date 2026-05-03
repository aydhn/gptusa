"""Fill models for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import BacktestOrderSide, BacktestFillStatus
from usa_signal_bot.core.exceptions import BacktestFillError
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent

@dataclass
class BacktestFill:
    """A simulated fill for a backtest order."""
    fill_id: str
    order_id: str
    signal_id: str | None
    symbol: str
    timeframe: str
    timestamp_utc: str
    side: BacktestOrderSide
    quantity: float
    fill_price: float
    fill_status: BacktestFillStatus
    fees: float = 0.0
    slippage: float = 0.0
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

def apply_slippage(price: float, side: BacktestOrderSide, slippage_bps: float) -> float:
    """Apply slippage to a price based on order side."""
    if slippage_bps <= 0:
        return price

    slippage_ratio = slippage_bps / 10000.0
    if side == BacktestOrderSide.BUY:
        return price * (1.0 + slippage_ratio)
    elif side == BacktestOrderSide.SELL:
        return price * (1.0 - slippage_ratio)
    return price

def calculate_fee(notional: float, fee_rate: float) -> float:
    """Calculate the fee for a trade."""
    if fee_rate <= 0:
        return 0.0
    return notional * fee_rate

def simulate_market_fill(
    order: BacktestOrderIntent,
    bar: OHLCVBar,
    fee_rate: float = 0.0,
    slippage_bps: float = 0.0
) -> BacktestFill:
    """Simulate a fill using the current bar's close price."""
    base_price = bar.close
    fill_price = apply_slippage(base_price, order.side, slippage_bps)
    notional = fill_price * order.quantity
    fees = calculate_fee(notional, fee_rate)

    return BacktestFill(
        fill_id=str(uuid.uuid4()),
        order_id=order.order_id,
        signal_id=order.signal_id,
        symbol=order.symbol,
        timeframe=order.timeframe,
        timestamp_utc=bar.timestamp_utc,
        side=order.side,
        quantity=order.quantity,
        fill_price=fill_price,
        fill_status=BacktestFillStatus.FILLED,
        fees=fees,
        slippage=slippage_bps,
        reason=f"Simulated market fill on {bar.timestamp_utc}",
        metadata={"base_price": base_price}
    )

def simulate_next_open_fill(
    order: BacktestOrderIntent,
    next_bar: OHLCVBar,
    fee_rate: float = 0.0,
    slippage_bps: float = 0.0
) -> BacktestFill:
    """Simulate a fill using the next bar's open price."""
    base_price = next_bar.open
    fill_price = apply_slippage(base_price, order.side, slippage_bps)
    notional = fill_price * order.quantity
    fees = calculate_fee(notional, fee_rate)

    return BacktestFill(
        fill_id=str(uuid.uuid4()),
        order_id=order.order_id,
        signal_id=order.signal_id,
        symbol=order.symbol,
        timeframe=order.timeframe,
        timestamp_utc=next_bar.timestamp_utc,
        side=order.side,
        quantity=order.quantity,
        fill_price=fill_price,
        fill_status=BacktestFillStatus.FILLED,
        fees=fees,
        slippage=slippage_bps,
        reason=f"Simulated next open fill on {next_bar.timestamp_utc}",
        metadata={"base_price": base_price}
    )

def fill_to_dict(fill: BacktestFill) -> dict:
    """Convert a fill to a dictionary for serialization."""
    return {
        "fill_id": fill.fill_id,
        "order_id": fill.order_id,
        "signal_id": fill.signal_id,
        "symbol": fill.symbol,
        "timeframe": fill.timeframe,
        "timestamp_utc": fill.timestamp_utc,
        "side": fill.side.value,
        "quantity": fill.quantity,
        "fill_price": fill.fill_price,
        "fill_status": fill.fill_status.value,
        "fees": fill.fees,
        "slippage": fill.slippage,
        "reason": fill.reason,
        "metadata": fill.metadata
    }

def validate_fill(fill: BacktestFill) -> None:
    """Validate a backtest fill.

    Raises:
        BacktestFillError: If the fill is invalid.
    """
    if fill.fill_price <= 0:
        raise BacktestFillError("fill_price must be positive")
    if fill.quantity < 0:
        raise BacktestFillError("quantity cannot be negative")
    if fill.fees < 0:
        raise BacktestFillError("fees cannot be negative")
    if fill.slippage < 0:
        raise BacktestFillError("slippage cannot be negative")
