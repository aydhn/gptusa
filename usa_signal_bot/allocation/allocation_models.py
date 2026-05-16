import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    CapitalAllocationMode,
    PositionSizeStatus,
    RiskBudgetStatus,
    SizingAdjustmentReason,
    RiskThrottleLevel,
    CapitalStateSource,
    AllocationReportType,
)

@dataclass
class CapitalState:
    capital_state_id: str
    created_at_utc: str
    source: CapitalStateSource
    total_equity_usd: float
    available_cash_usd: float
    reserved_cash_usd: float
    open_exposure_usd: float
    max_gross_exposure_usd: Optional[float]
    max_net_exposure_usd: Optional[float]
    currency: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RiskBudget:
    budget_id: str
    created_at_utc: str
    portfolio_risk_budget_pct: float
    per_trade_risk_budget_pct: float
    per_symbol_risk_budget_pct: float
    per_strategy_risk_budget_pct: float
    max_position_notional_pct: float
    max_position_notional_usd: Optional[float]
    max_daily_new_risk_pct: Optional[float]
    status: RiskBudgetStatus
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingInput:
    sizing_input_id: str
    symbol: str
    strategy_name: Optional[str]
    side: Optional[str]
    reference_price: Optional[float]
    signal_score: Optional[float]
    signal_confidence: Optional[float]
    ensemble_consensus_score: Optional[float]
    regime_alignment_score: Optional[float]
    transition_risk_score: Optional[float]
    liquidity_score: Optional[float]
    execution_realism_score: Optional[float]
    cost_robustness_score: Optional[float]
    atr_pct: Optional[float]
    stop_distance_pct: Optional[float]
    requested_notional_usd: Optional[float]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SizingAdjustment:
    adjustment_id: str
    reason: SizingAdjustmentReason
    multiplier: float
    delta_notional_usd: Optional[float]
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PositionSizeResult:
    result_id: str
    symbol: str
    created_at_utc: str
    mode: CapitalAllocationMode
    status: PositionSizeStatus
    side: Optional[str]
    reference_price: Optional[float]
    initial_notional_usd: Optional[float]
    final_notional_usd: Optional[float]
    final_quantity: Optional[float]
    risk_amount_usd: Optional[float]
    risk_pct_equity: Optional[float]
    confidence_multiplier: float
    volatility_multiplier: float
    liquidity_multiplier: float
    cost_multiplier: float
    regime_multiplier: float
    drawdown_multiplier: float
    concentration_multiplier: float
    adjustments: List[SizingAdjustment]
    budget: Optional[RiskBudget]
    capital_state: Optional[CapitalState]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationReview:
    review_id: str
    created_at_utc: str
    report_type: AllocationReportType
    mode: CapitalAllocationMode
    capital_state: Optional[CapitalState]
    risk_budget: Optional[RiskBudget]
    sizing_results: List[PositionSizeResult]
    total_allocated_notional_usd: Optional[float]
    average_risk_pct_equity: Optional[float]
    blocked_count: int
    capped_count: int
    throttled_count: int
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def capital_state_to_dict(item: CapitalState) -> dict:
    from dataclasses import asdict
    return asdict(item)

def risk_budget_to_dict(item: RiskBudget) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sizing_input_to_dict(item: SizingInput) -> dict:
    from dataclasses import asdict
    return asdict(item)

def sizing_adjustment_to_dict(item: SizingAdjustment) -> dict:
    from dataclasses import asdict
    return asdict(item)

def position_size_result_to_dict(item: PositionSizeResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def allocation_review_to_dict(item: AllocationReview) -> dict:
    from dataclasses import asdict
    return asdict(item)

def validate_capital_state(item: CapitalState) -> None:
    from usa_signal_bot.core.exceptions import CapitalStateError
    if item.total_equity_usd <= 0:
        raise CapitalStateError("Total equity must be strictly positive.")
    if item.available_cash_usd < 0:
        raise CapitalStateError("Available cash cannot be negative.")

def validate_risk_budget(item: RiskBudget) -> None:
    from usa_signal_bot.core.exceptions import RiskBudgetError
    if not (0 <= item.portfolio_risk_budget_pct <= 100):
        raise RiskBudgetError("Portfolio risk budget must be between 0 and 100.")
    if not (0 <= item.per_trade_risk_budget_pct <= 100):
        raise RiskBudgetError("Per trade risk budget must be between 0 and 100.")

def validate_sizing_input(item: SizingInput) -> None:
    from usa_signal_bot.core.exceptions import AllocationValidationError
    if not item.symbol:
        raise AllocationValidationError("Symbol cannot be empty.")

def validate_position_size_result(item: PositionSizeResult) -> None:
    from usa_signal_bot.core.exceptions import AllocationValidationError
    if item.final_notional_usd is not None and item.final_notional_usd < 0:
        raise AllocationValidationError("Final notional cannot be negative.")
    if item.final_quantity is not None and item.final_quantity < 0:
        raise AllocationValidationError("Final quantity cannot be negative.")
    if any(m < 0 for m in [item.confidence_multiplier, item.volatility_multiplier, item.liquidity_multiplier, item.cost_multiplier, item.regime_multiplier, item.drawdown_multiplier, item.concentration_multiplier]):
         raise AllocationValidationError("Multipliers cannot be negative.")

def create_capital_state_id(prefix: str = "capital_state") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_risk_budget_id(prefix: str = "risk_budget") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_sizing_input_id(symbol: str) -> str:
    return f"input_{symbol}_{uuid.uuid4().hex[:8]}"

def create_sizing_adjustment_id(reason: SizingAdjustmentReason) -> str:
    return f"adj_{reason.value}_{uuid.uuid4().hex[:8]}"

def create_position_size_result_id(symbol: str) -> str:
    return f"pos_{symbol}_{uuid.uuid4().hex[:8]}"

def create_allocation_review_id(prefix: str = "allocation_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
