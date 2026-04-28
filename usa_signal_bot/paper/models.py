from dataclasses import dataclass
from typing import Optional
from ..core.domain import BaseDomainModel
from ..core.enums import OrderSide, OrderType, OrderStatus, PositionSide, TradeStatus
from ..core.model_validation import ensure_non_empty_string, ensure_positive_number

@dataclass
class PaperOrder(BaseDomainModel):
    order_id: str = ""
    symbol: str = ""
    side: OrderSide = OrderSide.BUY
    order_type: OrderType = OrderType.MARKET
    quantity: float = 0.0
    created_at_utc: str = ""
    status: OrderStatus = OrderStatus.CREATED
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    reason: Optional[str] = None
    signal_id: Optional[str] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_non_empty_string(self.symbol, "symbol")
        ensure_positive_number(self.quantity, "quantity")

@dataclass
class PaperFill(BaseDomainModel):
    fill_id: str = ""
    order_id: str = ""
    symbol: str = ""
    side: OrderSide = OrderSide.BUY
    quantity: float = 0.0
    fill_price: float = 0.0
    filled_at_utc: str = ""
    commission: float = 0.0
    slippage_bps: float = 0.0

@dataclass
class PaperTrade(BaseDomainModel):
    trade_id: str = ""
    symbol: str = ""
    side: PositionSide = PositionSide.LONG
    quantity: float = 0.0
    entry_price: float = 0.0
    entry_time_utc: str = ""
    status: TradeStatus = TradeStatus.OPEN
    exit_price: Optional[float] = None
    exit_time_utc: Optional[str] = None
    realized_pnl: Optional[float] = None
    signal_id: Optional[str] = None
