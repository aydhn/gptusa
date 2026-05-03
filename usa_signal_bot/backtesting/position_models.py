"""Position models for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import BacktestPositionSide, BacktestOrderSide
from usa_signal_bot.core.exceptions import BacktestPositionError
from usa_signal_bot.backtesting.fill_models import BacktestFill

@dataclass
class BacktestPosition:
    """A simulated position in the backtest engine."""
    symbol: str
    side: BacktestPositionSide
    quantity: float
    average_price: float
    opened_at_utc: str | None
    updated_at_utc: str | None
    realized_pnl: float
    unrealized_pnl: float
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PositionUpdateResult:
    """The result of updating a position."""
    position: BacktestPosition
    cash_delta: float
    realized_pnl_delta: float
    message: str

def create_flat_position(symbol: str) -> BacktestPosition:
    """Create a new flat position."""
    return BacktestPosition(
        symbol=symbol,
        side=BacktestPositionSide.FLAT,
        quantity=0.0,
        average_price=0.0,
        opened_at_utc=None,
        updated_at_utc=None,
        realized_pnl=0.0,
        unrealized_pnl=0.0
    )

def update_position_with_fill(
    position: BacktestPosition,
    fill: BacktestFill,
    current_price: float | None = None
) -> PositionUpdateResult:
    """Update a position with a new fill."""
    if fill.symbol != position.symbol:
        raise BacktestPositionError(f"Fill symbol {fill.symbol} does not match position symbol {position.symbol}")

    if fill.side == BacktestOrderSide.HOLD:
        return PositionUpdateResult(position, 0.0, 0.0, "Ignored HOLD fill")

    if position.side == BacktestPositionSide.SHORT:
        raise BacktestPositionError("Short positions are not supported in Phase 25")

    cash_delta = 0.0
    realized_pnl_delta = 0.0
    notional = fill.quantity * fill.fill_price
    total_cost = notional + fill.fees

    new_quantity = position.quantity
    new_average_price = position.average_price
    new_realized_pnl = position.realized_pnl
    new_opened_at = position.opened_at_utc
    message = ""

    if fill.side == BacktestOrderSide.BUY:
        if position.side == BacktestPositionSide.FLAT:
            new_opened_at = fill.timestamp_utc
            new_side = BacktestPositionSide.LONG
        else:
            new_side = position.side

        new_quantity = position.quantity + fill.quantity
        total_value = (position.quantity * position.average_price) + (fill.quantity * fill.fill_price)
        new_average_price = total_value / new_quantity
        cash_delta = -total_cost
        message = f"Increased {new_side.value} position by {fill.quantity}"

    elif fill.side == BacktestOrderSide.SELL:
        if position.side == BacktestPositionSide.FLAT:
            raise BacktestPositionError("Cannot sell a flat position (shorting not supported)")

        sell_quantity = min(fill.quantity, position.quantity)
        if fill.quantity > position.quantity:
            message = f"WARNING: Oversell of {fill.quantity} > {position.quantity}. Flattening position."
        else:
            message = f"Decreased LONG position by {sell_quantity}"

        new_quantity = position.quantity - sell_quantity
        gross_pnl = (fill.fill_price - position.average_price) * sell_quantity
        fee_portion = fill.fees * (sell_quantity / fill.quantity) if fill.quantity > 0 else 0.0

        realized_pnl_delta = gross_pnl - fee_portion
        new_realized_pnl += realized_pnl_delta
        cash_delta = (sell_quantity * fill.fill_price) - fee_portion

        if new_quantity <= 1e-8:
            new_side = BacktestPositionSide.FLAT
            new_quantity = 0.0
            new_average_price = 0.0
            new_opened_at = None
        else:
            new_side = BacktestPositionSide.LONG

    new_position = BacktestPosition(
        symbol=position.symbol,
        side=new_side,
        quantity=new_quantity,
        average_price=new_average_price,
        opened_at_utc=new_opened_at,
        updated_at_utc=fill.timestamp_utc,
        realized_pnl=new_realized_pnl,
        unrealized_pnl=position.unrealized_pnl
    )

    if current_price is not None:
        new_position = mark_position_to_market(new_position, current_price, fill.timestamp_utc)

    return PositionUpdateResult(new_position, cash_delta, realized_pnl_delta, message)

def mark_position_to_market(
    position: BacktestPosition,
    current_price: float,
    timestamp_utc: str
) -> BacktestPosition:
    """Update unrealized PnL based on current market price."""
    if position.side == BacktestPositionSide.FLAT:
        unrealized_pnl = 0.0
    elif position.side == BacktestPositionSide.LONG:
        unrealized_pnl = (current_price - position.average_price) * position.quantity
    else:
        unrealized_pnl = 0.0

    return BacktestPosition(
        symbol=position.symbol,
        side=position.side,
        quantity=position.quantity,
        average_price=position.average_price,
        opened_at_utc=position.opened_at_utc,
        updated_at_utc=timestamp_utc,
        realized_pnl=position.realized_pnl,
        unrealized_pnl=unrealized_pnl,
        metadata=position.metadata
    )

def position_market_value(position: BacktestPosition, current_price: float) -> float:
    """Calculate the market value of the position."""
    if position.side == BacktestPositionSide.FLAT:
        return 0.0
    return position.quantity * current_price

def position_to_dict(position: BacktestPosition) -> dict:
    """Convert a position to a dictionary."""
    return {
        "symbol": position.symbol,
        "side": position.side.value,
        "quantity": position.quantity,
        "average_price": position.average_price,
        "opened_at_utc": position.opened_at_utc,
        "updated_at_utc": position.updated_at_utc,
        "realized_pnl": position.realized_pnl,
        "unrealized_pnl": position.unrealized_pnl,
        "metadata": position.metadata
    }

def validate_position(position: BacktestPosition) -> None:
    """Validate a position."""
    if position.quantity < 0:
        raise BacktestPositionError("Quantity cannot be negative")
    if position.side == BacktestPositionSide.FLAT and position.quantity > 0:
        raise BacktestPositionError("Flat position cannot have quantity > 0")
    if position.side != BacktestPositionSide.FLAT and position.quantity <= 0:
        raise BacktestPositionError("Non-flat position must have quantity > 0")
