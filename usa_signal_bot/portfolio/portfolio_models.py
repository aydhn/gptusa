from dataclasses import dataclass, field
from typing import Any, Optional, List
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    SignalAction,
    PortfolioCandidateStatus,
    AllocationMethod,
    AllocationStatus,
    PortfolioReviewStatus,
    PortfolioConstructionStatus
)

@dataclass
class PortfolioCandidate:
    candidate_id: str
    symbol: str
    timeframe: str
    action: SignalAction
    approved_quantity: float
    approved_notional: float
    signal_id: Optional[str] = None
    strategy_name: Optional[str] = None
    rank_score: Optional[float] = None
    confidence: Optional[float] = None
    risk_score: Optional[float] = None
    price: Optional[float] = None
    volatility_value: Optional[float] = None
    atr_value: Optional[float] = None
    risk_flags: List[str] = field(default_factory=list)
    status: PortfolioCandidateStatus = PortfolioCandidateStatus.ELIGIBLE
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationRequest:
    request_id: str
    candidates: List[PortfolioCandidate]
    portfolio_equity: float
    available_cash: float
    method: AllocationMethod
    max_total_allocation_pct: float
    created_at_utc: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AllocationResult:
    candidate_id: str
    symbol: str
    timeframe: str
    method: AllocationMethod
    status: AllocationStatus
    target_weight: float
    target_notional: float
    target_quantity: float
    raw_weight: float
    raw_notional: float
    capped: bool
    cap_reasons: List[str]
    warnings: List[str]
    errors: List[str]
    strategy_name: Optional[str] = None

@dataclass
class PortfolioBasket:
    basket_id: str
    created_at_utc: str
    method: AllocationMethod
    portfolio_equity: float
    available_cash: float
    candidates: List[PortfolioCandidate]
    allocations: List[AllocationResult]
    total_target_notional: float
    total_target_weight: float
    cash_buffer_after_allocation: float
    review_status: PortfolioReviewStatus
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PortfolioConstructionResult:
    run_id: str
    created_at_utc: str
    status: PortfolioConstructionStatus
    request: AllocationRequest
    risk_budget_report: dict[str, Any]
    concentration_report: dict[str, Any]
    approved_allocations: List[AllocationResult]
    rejected_allocations: List[AllocationResult]
    warnings: List[str]
    errors: List[str]
    basket: Optional[PortfolioBasket] = None
    output_paths: dict[str, str] = field(default_factory=dict)

def create_allocation_request_id(prefix: str = "alloc") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_portfolio_basket_id(prefix: str = "basket") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_portfolio_run_id(prefix: str = "portfolio") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_portfolio_candidate(candidate: PortfolioCandidate) -> None:
    from usa_signal_bot.core.exceptions import PortfolioCandidateError
    if not candidate.candidate_id:
        raise PortfolioCandidateError("candidate_id is empty.")
    if not candidate.symbol:
        raise PortfolioCandidateError("symbol is empty.")
    if not candidate.timeframe:
        raise PortfolioCandidateError("timeframe is empty.")
    if candidate.approved_quantity < 0:
        raise PortfolioCandidateError("approved_quantity cannot be negative.")
    if candidate.approved_notional < 0:
        raise PortfolioCandidateError("approved_notional cannot be negative.")
    if candidate.rank_score is not None and not (0 <= candidate.rank_score <= 100):
        raise PortfolioCandidateError("rank_score must be between 0 and 100.")
    if candidate.confidence is not None and not (0 <= candidate.confidence <= 1):
        raise PortfolioCandidateError("confidence must be between 0 and 1.")
    if candidate.risk_score is not None and not (0 <= candidate.risk_score <= 100):
        raise PortfolioCandidateError("risk_score must be between 0 and 100.")

def validate_allocation_request(request: AllocationRequest) -> None:
    from usa_signal_bot.core.exceptions import PortfolioValidationError
    if not request.request_id:
        raise PortfolioValidationError("request_id is empty.")
    if request.portfolio_equity <= 0:
        raise PortfolioValidationError("portfolio_equity must be greater than 0.")
    if request.available_cash < 0:
        raise PortfolioValidationError("available_cash cannot be negative.")
    if not (0 <= request.max_total_allocation_pct <= 1):
        raise PortfolioValidationError("max_total_allocation_pct must be between 0 and 1.")

def validate_allocation_result(result: AllocationResult) -> None:
    from usa_signal_bot.core.exceptions import PortfolioValidationError
    if not result.candidate_id:
        raise PortfolioValidationError("candidate_id is empty.")
    if not result.symbol:
        raise PortfolioValidationError("symbol is empty.")
    if result.target_weight < 0:
        raise PortfolioValidationError("target_weight cannot be negative.")
    if result.target_notional < 0:
        raise PortfolioValidationError("target_notional cannot be negative.")
    if result.target_quantity < 0:
        raise PortfolioValidationError("target_quantity cannot be negative.")
    if result.raw_weight < 0:
        raise PortfolioValidationError("raw_weight cannot be negative.")
    if result.raw_notional < 0:
        raise PortfolioValidationError("raw_notional cannot be negative.")

def validate_portfolio_basket(basket: PortfolioBasket) -> None:
    from usa_signal_bot.core.exceptions import PortfolioValidationError
    if not basket.basket_id:
        raise PortfolioValidationError("basket_id is empty.")
    if basket.portfolio_equity <= 0:
        raise PortfolioValidationError("portfolio_equity must be greater than 0.")
    if basket.available_cash < 0:
        raise PortfolioValidationError("available_cash cannot be negative.")
    if basket.total_target_notional < 0:
        raise PortfolioValidationError("total_target_notional cannot be negative.")
    if basket.total_target_weight < 0:
        raise PortfolioValidationError("total_target_weight cannot be negative.")
    # Intentionally ignoring cash_buffer_after_allocation check here to allow error reporting later.

def portfolio_candidate_to_dict(candidate: PortfolioCandidate) -> dict:
    from dataclasses import asdict
    d = asdict(candidate)
    d["action"] = candidate.action.value if hasattr(candidate.action, "value") else str(candidate.action)
    d["status"] = candidate.status.value if hasattr(candidate.status, "value") else str(candidate.status)
    return d

def allocation_request_to_dict(request: AllocationRequest) -> dict:
    from dataclasses import asdict
    d = asdict(request)
    d["method"] = request.method.value if hasattr(request.method, "value") else str(request.method)
    d["candidates"] = [portfolio_candidate_to_dict(c) for c in request.candidates]
    return d

def allocation_result_to_dict(result: AllocationResult) -> dict:
    from dataclasses import asdict
    d = asdict(result)
    d["method"] = result.method.value if hasattr(result.method, "value") else str(result.method)
    d["status"] = result.status.value if hasattr(result.status, "value") else str(result.status)
    return d

def portfolio_basket_to_dict(basket: PortfolioBasket) -> dict:
    from dataclasses import asdict
    d = asdict(basket)
    d["method"] = basket.method.value if hasattr(basket.method, "value") else str(basket.method)
    d["review_status"] = basket.review_status.value if hasattr(basket.review_status, "value") else str(basket.review_status)
    d["candidates"] = [portfolio_candidate_to_dict(c) for c in basket.candidates]
    d["allocations"] = [allocation_result_to_dict(a) for a in basket.allocations]
    return d

def portfolio_construction_result_to_dict(result: PortfolioConstructionResult) -> dict:
    from dataclasses import asdict
    d = asdict(result)
    d["status"] = result.status.value if hasattr(result.status, "value") else str(result.status)
    d["request"] = allocation_request_to_dict(result.request)
    if result.basket:
        d["basket"] = portfolio_basket_to_dict(result.basket)
    else:
        d["basket"] = None
    d["approved_allocations"] = [allocation_result_to_dict(a) for a in result.approved_allocations]
    d["rejected_allocations"] = [allocation_result_to_dict(a) for a in result.rejected_allocations]
    return d
