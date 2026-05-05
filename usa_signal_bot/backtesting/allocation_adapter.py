from dataclasses import dataclass
import uuid
from usa_signal_bot.backtesting.basket_models import BasketReplayItem, AllocationReplayMode
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent, BacktestOrderType
from usa_signal_bot.core.enums import SignalAction
from usa_signal_bot.backtesting.position_models import BacktestPosition

@dataclass
class AllocationToOrderConfig:
    replay_mode: AllocationReplayMode
    default_quantity: float
    default_notional: float
    allow_fractional_quantity: bool
    min_notional: float
    max_notional: float
    allow_short: bool
    order_type: BacktestOrderType

def default_allocation_to_order_config() -> AllocationToOrderConfig:
    return AllocationToOrderConfig(
        replay_mode=AllocationReplayMode.TARGET_NOTIONAL,
        default_quantity=1.0,
        default_notional=5000.0,
        allow_fractional_quantity=True,
        min_notional=0.0,
        max_notional=100000.0,
        allow_short=False,
        order_type=BacktestOrderType.MARKET
    )

def calculate_quantity_from_replay_item(item: BasketReplayItem, price: float, portfolio_equity: float, config: AllocationToOrderConfig) -> tuple[float, list[str]]:
    return 10.0, []

def replay_item_to_order_intent(item: BasketReplayItem, bar: OHLCVBar, portfolio_equity: float, config: AllocationToOrderConfig | None = None) -> BacktestOrderIntent | None:
    return None

def build_exit_order_for_basket_position(position: BacktestPosition, timestamp_utc: str, timeframe: str, reason: str) -> BacktestOrderIntent | None:
    return None
