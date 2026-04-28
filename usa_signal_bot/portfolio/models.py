from dataclasses import dataclass
from typing import Optional
from ..core.domain import BaseDomainModel
from ..core.enums import PositionSide

@dataclass
class Position(BaseDomainModel):
    position_id: str = ""
    symbol: str = ""
    side: PositionSide = PositionSide.LONG
    quantity: float = 0.0
    average_price: float = 0.0
    market_price: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    realized_pnl: float = 0.0
    opened_at_utc: Optional[str] = None
    updated_at_utc: Optional[str] = None

@dataclass
class PortfolioSnapshot(BaseDomainModel):
    portfolio_id: str = ""
    timestamp_utc: str = ""
    cash: float = 0.0
    equity: float = 0.0
    positions: list[Position] = None
    currency: str = "USD"

    def __post_init__(self):
        if self.positions is None:
            self.positions = []

    def gross_exposure(self) -> float:
        return sum(abs(p.quantity * (p.market_price if p.market_price is not None else p.average_price)) for p in self.positions)

    def net_exposure(self) -> float:
        total = 0.0
        for p in self.positions:
            val = p.quantity * (p.market_price if p.market_price is not None else p.average_price)
            if p.side == PositionSide.SHORT:
                total -= val
            else:
                total += val
        return total

    def open_position_count(self) -> int:
        return len(self.positions)

@dataclass
class PortfolioLedgerEntry(BaseDomainModel):
    entry_id: str = ""
    timestamp_utc: str = ""
    event_type: str = ""
    symbol: Optional[str] = None
    amount: float = 0.0
    cash_after: float = 0.0
    note: Optional[str] = None
