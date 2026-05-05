import uuid
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import (
    BasketReplaySource, BasketSimulationStatus, BasketEntryMode, BasketExitMode,
    AllocationReplayMode, BasketReviewStatus, BasketMetricStatus, SignalAction
)
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent, BacktestOrderType
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolio, BacktestPortfolioSnapshot
from usa_signal_bot.backtesting.trade_ledger import TradeLedger

@dataclass
class BasketReplayRequest:
    request_id: str
    source: BasketReplaySource
    basket_file: str | None = None
    allocations_file: str | None = None
    risk_decisions_file: str | None = None
    selected_candidates_file: str | None = None
    signal_file: str | None = None
    symbols: list[str] | None = None
    timeframe: str = "1d"
    provider_name: str = "yfinance"
    start_date: str | None = None
    end_date: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BasketSimulationConfig:
    starting_cash: float
    entry_mode: BasketEntryMode
    exit_mode: BasketExitMode
    allocation_replay_mode: AllocationReplayMode
    hold_bars: int
    allow_fractional_quantity: bool
    prevent_same_bar_fill: bool
    max_positions: int
    max_total_allocation_pct: float
    rebalance_reserved: bool = False
    enable_transaction_costs: bool = True
    enable_slippage: bool = True
    enable_benchmark_comparison: bool = False
    benchmark_set_name: str = "default"

@dataclass
class BasketReplayItem:
    item_id: str
    candidate_id: str | None
    signal_id: str | None
    symbol: str
    timeframe: str
    strategy_name: str | None
    action: SignalAction
    target_weight: float | None
    target_notional: float | None
    target_quantity: float | None
    rank_score: float | None
    risk_score: float | None
    confidence: float | None
    timestamp_utc: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BasketReplayData:
    request: BasketReplayRequest
    items: list[BasketReplayItem]
    symbols: list[str]
    timeframe: str
    warnings: list[str]
    errors: list[str]

@dataclass
class BasketExposureSnapshot:
    timestamp_utc: str
    equity: float
    cash: float
    gross_exposure: float
    net_exposure: float
    target_total_weight: float
    actual_total_weight: float
    weight_by_symbol: dict[str, float]
    target_weight_by_symbol: dict[str, float]
    drift_by_symbol: dict[str, float]
    open_positions: int
    warnings: list[str] = field(default_factory=list)

@dataclass
class BasketSimulationResult:
    run_id: str
    created_at_utc: str
    status: BasketSimulationStatus
    request: BasketReplayRequest
    config: BasketSimulationConfig
    replay_data: BasketReplayData
    portfolio: BacktestPortfolio
    snapshots: list[BacktestPortfolioSnapshot]
    basket_exposure_snapshots: list[BasketExposureSnapshot]
    order_intents: list[BacktestOrderIntent]
    fills: list[BacktestFill]
    trade_ledger: TradeLedger | None
    basket_metrics: dict[str, Any]
    benchmark_summary: dict[str, Any]
    review_status: BasketReviewStatus
    warnings: list[str]
    errors: list[str]
    output_paths: dict[str, str] = field(default_factory=dict)

def create_basket_replay_request_id(prefix: str = "basket_replay") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_basket_simulation_run_id(prefix: str = "basket_sim") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def basket_replay_request_to_dict(request: BasketReplayRequest) -> dict:
    from dataclasses import asdict
    return asdict(request)

def basket_simulation_config_to_dict(config: BasketSimulationConfig) -> dict:
    from dataclasses import asdict
    return asdict(config)

def basket_replay_item_to_dict(item: BasketReplayItem) -> dict:
    from dataclasses import asdict
    return asdict(item)

def basket_replay_data_to_dict(data: BasketReplayData) -> dict:
    from dataclasses import asdict
    return asdict(data)

def basket_exposure_snapshot_to_dict(snapshot: BasketExposureSnapshot) -> dict:
    from dataclasses import asdict
    return asdict(snapshot)

def basket_simulation_result_to_dict(result: BasketSimulationResult) -> dict:
    from dataclasses import asdict
    return asdict(result)

def validate_basket_replay_request(request: BasketReplayRequest) -> None:
    from usa_signal_bot.core.exceptions import BasketValidationError
    if not request.timeframe:
        raise BasketValidationError("BasketReplayRequest timeframe cannot be empty")
    if request.source == BasketReplaySource.PORTFOLIO_BASKET and not request.basket_file:
        raise BasketValidationError("basket_file required for PORTFOLIO_BASKET source")

def validate_basket_simulation_config(config: BasketSimulationConfig) -> None:
    from usa_signal_bot.core.exceptions import BasketValidationError
    if config.starting_cash <= 0:
        raise BasketValidationError("starting_cash must be positive")

def validate_basket_replay_item(item: BasketReplayItem) -> None:
    from usa_signal_bot.core.exceptions import BasketValidationError
    if item.target_weight is not None and not (0 <= item.target_weight <= 1.0):
        raise BasketValidationError(f"target_weight for {item.symbol} must be between 0 and 1, got {item.target_weight}")
