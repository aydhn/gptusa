from dataclasses import dataclass, field
from typing import Any
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    ExposureLimitType,
    RiskSeverity,
    RiskCheckStatus,
    RiskRejectionReason,
    PositionSizingMethod,
    SignalAction,
    RiskDecisionStatus,
    RiskRunStatus
)
from usa_signal_bot.core.exceptions import RiskLimitError, PositionSizingError

@dataclass
class RiskLimit:
    name: str
    limit_type: ExposureLimitType
    value: float
    enabled: bool = True
    severity: RiskSeverity = RiskSeverity.HIGH
    description: str | None = None

@dataclass
class RiskCheckResult:
    check_name: str
    status: RiskCheckStatus
    severity: RiskSeverity
    message: str
    rejection_reason: RiskRejectionReason | None = None
    observed_value: float | None = None
    limit_value: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PositionSizingRequest:
    candidate_id: str
    symbol: str
    strategy_name: str | None
    timeframe: str
    action: SignalAction
    confidence: float
    rank_score: float | None
    price: float
    portfolio_equity: float
    available_cash: float
    volatility_value: float | None = None
    atr_value: float | None = None
    risk_per_trade_pct: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PositionSizingResult:
    candidate_id: str
    method: PositionSizingMethod
    approved_quantity: float
    approved_notional: float
    raw_quantity: float
    raw_notional: float
    capped: bool
    cap_reasons: list[str]
    warnings: list[str]
    errors: list[str]

@dataclass
class RiskDecision:
    decision_id: str
    candidate_id: str
    signal_id: str | None
    symbol: str
    strategy_name: str | None
    timeframe: str
    status: RiskDecisionStatus
    action: SignalAction
    approved_quantity: float
    approved_notional: float
    sizing_method: PositionSizingMethod
    checks: list[RiskCheckResult]
    rejection_reasons: list[RiskRejectionReason]
    risk_score: float
    severity: RiskSeverity
    notes: list[str]
    created_at_utc: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RiskRunResult:
    run_id: str
    created_at_utc: str
    status: RiskRunStatus
    total_candidates: int
    approved_count: int
    rejected_count: int
    reduced_count: int
    needs_review_count: int
    decisions: list[RiskDecision]
    warnings: list[str]
    errors: list[str]

def risk_limit_to_dict(limit: RiskLimit) -> dict[str, Any]:
    return {
        "name": limit.name,
        "limit_type": limit.limit_type.value,
        "value": limit.value,
        "enabled": limit.enabled,
        "severity": limit.severity.value,
        "description": limit.description
    }

def risk_check_result_to_dict(result: RiskCheckResult) -> dict[str, Any]:
    return {
        "check_name": result.check_name,
        "status": result.status.value,
        "severity": result.severity.value,
        "message": result.message,
        "rejection_reason": result.rejection_reason.value if result.rejection_reason else None,
        "observed_value": result.observed_value,
        "limit_value": result.limit_value,
        "metadata": result.metadata
    }

def position_sizing_request_to_dict(request: PositionSizingRequest) -> dict[str, Any]:
    return {
        "candidate_id": request.candidate_id,
        "symbol": request.symbol,
        "strategy_name": request.strategy_name,
        "timeframe": request.timeframe,
        "action": request.action.value,
        "confidence": request.confidence,
        "rank_score": request.rank_score,
        "price": request.price,
        "portfolio_equity": request.portfolio_equity,
        "available_cash": request.available_cash,
        "volatility_value": request.volatility_value,
        "atr_value": request.atr_value,
        "risk_per_trade_pct": request.risk_per_trade_pct,
        "metadata": request.metadata
    }

def position_sizing_result_to_dict(result: PositionSizingResult) -> dict[str, Any]:
    return {
        "candidate_id": result.candidate_id,
        "method": result.method.value,
        "approved_quantity": result.approved_quantity,
        "approved_notional": result.approved_notional,
        "raw_quantity": result.raw_quantity,
        "raw_notional": result.raw_notional,
        "capped": result.capped,
        "cap_reasons": result.cap_reasons,
        "warnings": result.warnings,
        "errors": result.errors
    }

def risk_decision_to_dict(decision: RiskDecision) -> dict[str, Any]:
    return {
        "decision_id": decision.decision_id,
        "candidate_id": decision.candidate_id,
        "signal_id": decision.signal_id,
        "symbol": decision.symbol,
        "strategy_name": decision.strategy_name,
        "timeframe": decision.timeframe,
        "status": decision.status.value,
        "action": decision.action.value,
        "approved_quantity": decision.approved_quantity,
        "approved_notional": decision.approved_notional,
        "sizing_method": decision.sizing_method.value,
        "checks": [risk_check_result_to_dict(c) for c in decision.checks],
        "rejection_reasons": [r.value for r in decision.rejection_reasons],
        "risk_score": decision.risk_score,
        "severity": decision.severity.value,
        "notes": decision.notes,
        "created_at_utc": decision.created_at_utc,
        "metadata": decision.metadata
    }

def risk_run_result_to_dict(result: RiskRunResult) -> dict[str, Any]:
    return {
        "run_id": result.run_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "total_candidates": result.total_candidates,
        "approved_count": result.approved_count,
        "rejected_count": result.rejected_count,
        "reduced_count": result.reduced_count,
        "needs_review_count": result.needs_review_count,
        "decisions": [risk_decision_to_dict(d) for d in result.decisions],
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_risk_limit(limit: RiskLimit) -> None:
    if not limit.name:
        raise RiskLimitError("Risk limit name cannot be empty")
    if limit.value < 0:
        raise RiskLimitError(f"Risk limit value cannot be negative: {limit.value}")
    if not isinstance(limit.limit_type, ExposureLimitType):
        raise RiskLimitError(f"Invalid limit_type: {limit.limit_type}")
    if not isinstance(limit.severity, RiskSeverity):
        raise RiskLimitError(f"Invalid severity: {limit.severity}")

def validate_position_sizing_request(request: PositionSizingRequest) -> None:
    if request.price is None or request.price <= 0:
        raise PositionSizingError(f"Invalid price for sizing request: {request.price}")
    if request.portfolio_equity <= 0:
        raise PositionSizingError(f"Invalid portfolio_equity for sizing request: {request.portfolio_equity}")

def validate_position_sizing_result(result: PositionSizingResult) -> None:
    if result.approved_quantity < 0:
        raise PositionSizingError(f"Approved quantity cannot be negative: {result.approved_quantity}")
    if result.approved_notional < 0:
        raise PositionSizingError(f"Approved notional cannot be negative: {result.approved_notional}")

def create_risk_decision_id(candidate_id: str, symbol: str) -> str:
    return f"dec_{symbol}_{candidate_id[:8]}_{uuid.uuid4().hex[:8]}"

def create_risk_run_id(prefix: str = "risk") -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}_{uuid.uuid4().hex[:6]}"
