from dataclasses import dataclass
from typing import Optional, Any
from ..core.domain import BaseDomainModel
from ..core.enums import BacktestStatus

@dataclass
class BacktestRequest(BaseDomainModel):
    strategy_name: str = ""
    symbols: list[str] = None
    timeframe: str = ""
    start_date: str = ""
    end_date: str = ""
    initial_cash: float = 0.0
    benchmark: Optional[str] = "SPY"
    parameters: dict[str, Any] = None

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = []
        if self.parameters is None:
            self.parameters = {}

@dataclass
class BacktestMetrics(BaseDomainModel):
    total_return_pct: Optional[float] = None
    annualized_return_pct: Optional[float] = None
    max_drawdown_pct: Optional[float] = None
    win_rate: Optional[float] = None
    profit_factor: Optional[float] = None
    expectancy: Optional[float] = None
    sharpe: Optional[float] = None
    sortino: Optional[float] = None
    trade_count: int = 0

@dataclass
class BacktestResult(BaseDomainModel):
    backtest_id: str = ""
    request: BacktestRequest = None
    status: BacktestStatus = BacktestStatus.NOT_STARTED
    metrics: BacktestMetrics = None
    errors: list[str] = None
    created_at_utc: str = ""

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
