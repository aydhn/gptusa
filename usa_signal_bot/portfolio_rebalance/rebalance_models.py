import uuid
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    RebalanceMode,
    RebalanceActionType,
    RebalanceStatus,
    DriftType,
    DriftSeverity,
    TurnoverStatus,
    RebalanceThrottleReason,
    RebalanceReportType
)
from usa_signal_bot.core.exceptions import DataValidationError

@dataclass
class PortfolioPosition:
    position_id: str
    symbol: str
    quantity: float
    market_value_usd: float
    side: Optional[str] = None
    market_price: Optional[float] = None
    weight_pct_equity: Optional[float] = None
    strategy_name: Optional[str] = None
    sector: Optional[str] = None
    cluster: Optional[str] = None
    regime_label: Optional[str] = None
    liquidity_bucket: Optional[str] = None
    cost_bucket: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CurrentPortfolioState:
    state_id: str
    created_at_utc: str
    gross_exposure_usd: float
    net_exposure_usd: float
    positions: List[PortfolioPosition] = field(default_factory=list)
    total_equity_usd: Optional[float] = None
    cash_usd: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TargetPortfolioState:
    target_id: str
    created_at_utc: str
    target_gross_exposure_usd: float
    target_net_exposure_usd: float
    target_positions: List[PortfolioPosition] = field(default_factory=list)
    source_plan_id: Optional[str] = None
    total_equity_usd: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DriftMeasurement:
    drift_id: str
    created_at_utc: str
    drift_type: DriftType
    name: str
    severity: DriftSeverity
    current_value: Optional[float] = None
    target_value: Optional[float] = None
    absolute_drift: Optional[float] = None
    pct_drift: Optional[float] = None
    threshold: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RebalanceAction:
    action_id: str
    symbol: str
    action_type: RebalanceActionType
    status: RebalanceStatus
    current_notional_usd: Optional[float] = None
    target_notional_usd: Optional[float] = None
    delta_notional_usd: Optional[float] = None
    estimated_quantity_delta: Optional[float] = None
    estimated_turnover_usd: Optional[float] = None
    estimated_cost_usd: Optional[float] = None
    estimated_cost_bps: Optional[float] = None
    throttle_reasons: List[RebalanceThrottleReason] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TurnoverAssessment:
    assessment_id: str
    created_at_utc: str
    estimated_turnover_usd: float
    status: TurnoverStatus
    action_count: int
    suppressed_action_count: int
    estimated_turnover_pct_equity: Optional[float] = None
    max_turnover_pct_equity: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RebalancePlan:
    plan_id: str
    created_at_utc: str
    mode: RebalanceMode
    status: RebalanceStatus
    proposed_action_count: int
    suppressed_action_count: int
    blocked_action_count: int
    current_state: Optional[CurrentPortfolioState] = None
    target_state: Optional[TargetPortfolioState] = None
    drift_measurements: List[DriftMeasurement] = field(default_factory=list)
    actions: List[RebalanceAction] = field(default_factory=list)
    turnover_assessment: Optional[TurnoverAssessment] = None
    total_delta_notional_usd: Optional[float] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RebalanceReview:
    review_id: str
    created_at_utc: str
    report_type: RebalanceReportType
    plan: Optional[RebalancePlan] = None
    current_state: Optional[CurrentPortfolioState] = None
    target_state: Optional[TargetPortfolioState] = None
    drift_measurements: List[DriftMeasurement] = field(default_factory=list)
    turnover_assessment: Optional[TurnoverAssessment] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def validate_portfolio_position(item: PortfolioPosition) -> None:
    if not item.symbol:
        raise DataValidationError("symbol cannot be empty")
    if item.quantity < 0:
        raise DataValidationError("quantity cannot be negative")
    if item.market_value_usd < 0:
        raise DataValidationError("market_value_usd cannot be negative")

def validate_current_portfolio_state(item: CurrentPortfolioState) -> None:
    if item.total_equity_usd is not None and item.total_equity_usd < 0:
        raise DataValidationError("total_equity_usd cannot be negative")
    for pos in item.positions:
        validate_portfolio_position(pos)

def validate_target_portfolio_state(item: TargetPortfolioState) -> None:
    if item.total_equity_usd is not None and item.total_equity_usd < 0:
        raise DataValidationError("total_equity_usd cannot be negative")
    for pos in item.target_positions:
        validate_portfolio_position(pos)

def validate_drift_measurement(item: DriftMeasurement) -> None:
    if not item.name:
        raise DataValidationError("drift name cannot be empty")

def validate_rebalance_action(item: RebalanceAction) -> None:
    if not item.symbol:
        raise DataValidationError("action symbol cannot be empty")
    if item.estimated_cost_usd is not None and item.estimated_cost_usd < 0:
        raise DataValidationError("estimated_cost_usd cannot be negative")
    if item.estimated_turnover_usd is not None and item.estimated_turnover_usd < 0:
        raise DataValidationError("estimated_turnover_usd cannot be negative")

def validate_turnover_assessment(item: TurnoverAssessment) -> None:
    if item.estimated_turnover_usd < 0:
        raise DataValidationError("estimated_turnover_usd cannot be negative")

def validate_rebalance_plan(item: RebalancePlan) -> None:
    if item.current_state:
        validate_current_portfolio_state(item.current_state)
    if item.target_state:
        validate_target_portfolio_state(item.target_state)
    for dm in item.drift_measurements:
        validate_drift_measurement(dm)
    for a in item.actions:
        validate_rebalance_action(a)
    if item.turnover_assessment:
        validate_turnover_assessment(item.turnover_assessment)

def create_portfolio_position_id(symbol: str) -> str:
    return f"pos_{symbol}_{uuid.uuid4().hex[:8]}"

def create_current_portfolio_state_id(prefix: str = "current_portfolio") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_target_portfolio_state_id(prefix: str = "target_portfolio") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_drift_measurement_id(name: str) -> str:
    safe_name = name.lower().replace(" ", "_")
    return f"drift_{safe_name}_{uuid.uuid4().hex[:8]}"

def create_rebalance_action_id(symbol: str) -> str:
    return f"action_{symbol}_{uuid.uuid4().hex[:8]}"

def create_turnover_assessment_id(prefix: str = "turnover") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rebalance_plan_id(prefix: str = "rebalance_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_rebalance_review_id(prefix: str = "rebalance_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

from enum import Enum
from dataclasses import asdict

def portfolio_position_to_dict(item: PortfolioPosition) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def current_portfolio_state_to_dict(item: CurrentPortfolioState) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def target_portfolio_state_to_dict(item: TargetPortfolioState) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def drift_measurement_to_dict(item: DriftMeasurement) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def rebalance_action_to_dict(item: RebalanceAction) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def turnover_assessment_to_dict(item: TurnoverAssessment) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def rebalance_plan_to_dict(item: RebalancePlan) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))

def rebalance_review_to_dict(item: RebalanceReview) -> dict:
    return json.loads(json.dumps(asdict(item), cls=CustomJSONEncoder))
