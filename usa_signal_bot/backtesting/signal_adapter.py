"""Adapter to convert signals to backtest orders."""
from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import BacktestSignalMode, BacktestOrderType, BacktestOrderSide
from usa_signal_bot.core.exceptions import BacktestValidationError
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent, create_order_intent_from_signal
from usa_signal_bot.backtesting.position_models import BacktestPosition

@dataclass
class SignalToOrderConfig:
    signal_mode: BacktestSignalMode
    fixed_quantity: float | None
    fixed_notional: float | None
    allow_short: bool
    min_confidence: float
    min_score: float
    order_type: BacktestOrderType
    hold_bars: int

def default_signal_to_order_config() -> SignalToOrderConfig:
    return SignalToOrderConfig(
        signal_mode=BacktestSignalMode.WATCH_AS_LONG_CANDIDATE,
        fixed_quantity=None,
        fixed_notional=10000.0,
        allow_short=False,
        min_confidence=0.0,
        min_score=0.0,
        order_type=BacktestOrderType.NEXT_OPEN,
        hold_bars=5
    )

def validate_signal_to_order_config(config: SignalToOrderConfig) -> None:
    if config.fixed_quantity is None and config.fixed_notional is None:
        raise BacktestValidationError("Must provide either fixed_quantity or fixed_notional")
    if config.fixed_quantity is not None and config.fixed_notional is not None:
        raise BacktestValidationError("Provide only one of fixed_quantity or fixed_notional")

    if config.fixed_quantity is not None and config.fixed_quantity <= 0:
        raise BacktestValidationError("fixed_quantity must be positive")
    if config.fixed_notional is not None and config.fixed_notional <= 0:
        raise BacktestValidationError("fixed_notional must be positive")

    if config.min_confidence < 0 or config.min_confidence > 1:
        raise BacktestValidationError("min_confidence must be between 0 and 1")
    if config.min_score < 0 or config.min_score > 100:
        raise BacktestValidationError("min_score must be between 0 and 100")
    if config.hold_bars <= 0:
        raise BacktestValidationError("hold_bars must be positive")

def should_signal_create_order(signal: StrategySignal, config: SignalToOrderConfig) -> tuple[bool, str]:
    if config.signal_mode == BacktestSignalMode.WATCH_ONLY_NO_TRADES:
        return False, "Mode is WATCH_ONLY_NO_TRADES"

    if signal.confidence < config.min_confidence:
        return False, f"Confidence {signal.confidence} < {config.min_confidence}"

    if signal.score < config.min_score:
        return False, f"Score {signal.score} < {config.min_score}"

    action_str = signal.action.value

    if action_str == "SHORT" and not config.allow_short:
        return False, "Shorting is not allowed"

    if action_str == "WATCH":
        if config.signal_mode == BacktestSignalMode.WATCH_AS_LONG_CANDIDATE:
            pass
        else:
            return False, "Signal action is WATCH, but mode is not WATCH_AS_LONG_CANDIDATE"

    return True, "Passed"

def calculate_order_quantity_from_notional(notional: float, price: float) -> float:
    if price <= 0:
        return 0.0
    return notional / price

def signal_to_order_intent(
    signal: StrategySignal,
    bar: OHLCVBar,
    config: SignalToOrderConfig
) -> BacktestOrderIntent | None:
    should_create, reason = should_signal_create_order(signal, config)
    if not should_create:
        return None

    if config.fixed_quantity is not None:
        quantity = config.fixed_quantity
    else:
        quantity = calculate_order_quantity_from_notional(config.fixed_notional or 0.0, bar.close)

    if quantity <= 0:
        return None

    intent = create_order_intent_from_signal(signal, quantity, config.order_type)

    if signal.action.value == "WATCH" and config.signal_mode == BacktestSignalMode.WATCH_AS_LONG_CANDIDATE:
        intent.side = BacktestOrderSide.BUY

    intent.metadata["original_signal_action"] = signal.action.value

    return intent

def build_exit_order_for_position(
    position: BacktestPosition,
    timestamp_utc: str,
    timeframe: str,
    reason: str
) -> BacktestOrderIntent | None:
    if position.side.value == "FLAT" or position.quantity <= 0:
        return None

    side = BacktestOrderSide.SELL if position.side.value == "LONG" else BacktestOrderSide.BUY

    return BacktestOrderIntent(
        order_id=str(uuid.uuid4()),
        signal_id=None,
        symbol=position.symbol,
        timeframe=timeframe,
        timestamp_utc=timestamp_utc,
        side=side,
        order_type=BacktestOrderType.NEXT_OPEN,
        quantity=position.quantity,
        reason=reason
    )

def allocation_to_backtest_order_quantity(signal: 'StrategySignal', allocation: 'AllocationResult', fallback_quantity: float) -> float:
    from usa_signal_bot.core.enums import AllocationStatus
    if allocation is None:
        return fallback_quantity
    if allocation.status in [AllocationStatus.ALLOCATED, AllocationStatus.CAPPED, AllocationStatus.REDUCED]:
        return allocation.target_quantity
    if allocation.status in [AllocationStatus.REJECTED, AllocationStatus.ZERO, AllocationStatus.ERROR]:
        return 0.0
    return fallback_quantity

def signal_to_order_intent_with_allocation(signal: 'StrategySignal', bar: 'OHLCVBar', config: 'SignalToOrderConfig', allocation: 'AllocationResult' = None) -> 'BacktestOrderIntent':
    from usa_signal_bot.core.enums import BacktestOrderSide
    intent = signal_to_order_intent(signal, bar, config)
    if not intent:
        return None

    if allocation:
        qty = allocation_to_backtest_order_quantity(signal, allocation, intent.quantity)
        if qty <= 0:
            return None
        intent.quantity = qty

    return intent
