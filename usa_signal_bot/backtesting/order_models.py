"""Order models for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import BacktestOrderSide, BacktestOrderType
from usa_signal_bot.core.exceptions import BacktestOrderError
from usa_signal_bot.strategies.signal_contract import StrategySignal

@dataclass
class BacktestOrderIntent:
    """An intent to execute an order in the backtest engine."""
    order_id: str
    signal_id: str | None
    symbol: str
    timeframe: str
    timestamp_utc: str
    side: BacktestOrderSide
    order_type: BacktestOrderType
    quantity: float
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_order_intent_from_signal(
    signal: StrategySignal,
    quantity: float,
    order_type: BacktestOrderType = BacktestOrderType.NEXT_OPEN
) -> BacktestOrderIntent:
    """Create a new BacktestOrderIntent from a StrategySignal."""
    side = BacktestOrderSide.BUY if signal.action.value == "LONG" else BacktestOrderSide.HOLD
    return BacktestOrderIntent(
        order_id=str(uuid.uuid4()),
        signal_id=signal.signal_id,
        symbol=signal.symbol,
        timeframe=signal.timeframe,
        timestamp_utc=signal.timestamp_utc,
        side=side,
        order_type=order_type,
        quantity=quantity,
        reason=f"Generated from signal {signal.signal_id}"
    )

def order_intent_to_dict(order: BacktestOrderIntent) -> dict:
    """Convert an order intent to a dictionary for serialization."""
    return {
        "order_id": order.order_id,
        "signal_id": order.signal_id,
        "symbol": order.symbol,
        "timeframe": order.timeframe,
        "timestamp_utc": order.timestamp_utc,
        "side": order.side.value,
        "order_type": order.order_type.value,
        "quantity": order.quantity,
        "reason": order.reason,
        "metadata": order.metadata
    }

def validate_order_intent(order: BacktestOrderIntent) -> None:
    """Validate a backtest order intent.

    Raises:
        BacktestOrderError: If the order is invalid.
    """
    if not order.order_id:
        raise BacktestOrderError("order_id cannot be empty")
    if not order.symbol:
        raise BacktestOrderError("symbol cannot be empty")
    if order.quantity < 0:
        raise BacktestOrderError("quantity cannot be negative")

    if order.side == BacktestOrderSide.HOLD:
        pass # quantity can be 0
    else:
        if order.quantity <= 0:
            raise BacktestOrderError(f"quantity must be positive for {order.side.value} side")

def is_trade_order(order: BacktestOrderIntent) -> bool:
    """Return True if the order is a BUY or SELL order."""
    return order.side in (BacktestOrderSide.BUY, BacktestOrderSide.SELL)

@dataclass
class SignalToOrderIntentConfig:
    allow_short: bool = False

def signal_to_order_intent(signal: StrategySignal, mock_bar: Any, config: SignalToOrderIntentConfig) -> BacktestOrderIntent | None:
    from usa_signal_bot.core.enums import SignalAction
    side = BacktestOrderSide.HOLD
    if signal.action.value == "LONG" or signal.action.value == "BUY":
         side = BacktestOrderSide.BUY
    elif signal.action.value == "SHORT" or signal.action.value == "SELL":
         if not config.allow_short:
              return None
         side = BacktestOrderSide.SELL

    if side == BacktestOrderSide.HOLD:
         return None

    return BacktestOrderIntent(
        order_id=str(uuid.uuid4()),
        signal_id=signal.signal_id,
        symbol=signal.symbol,
        timeframe=signal.timeframe,
        timestamp_utc=signal.timestamp_utc,
        side=side,
        order_type=BacktestOrderType.MARKET,
        quantity=1.0,
        reason=f"Generated from signal {signal.signal_id}"
    )

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from usa_signal_bot.backtesting.position_models import BacktestPosition

def build_exit_order_for_position(position: 'BacktestPosition', timestamp_utc: str, timeframe: str, reason: str) -> BacktestOrderIntent | None:
    if position.side.value == "LONG":
         side = BacktestOrderSide.SELL
    elif position.side.value == "SHORT":
         side = BacktestOrderSide.BUY
    else:
         return None

    return BacktestOrderIntent(
        order_id=str(uuid.uuid4()),
        signal_id=None,
        symbol=position.symbol,
        timeframe=timeframe,
        timestamp_utc=timestamp_utc,
        side=side,
        order_type=BacktestOrderType.MARKET,
        quantity=position.quantity,
        reason=reason
    )
