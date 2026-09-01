"""Attribution models and core data structures for performance and risk attribution."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    AttributionDimension,
    ContributionDirection,
    AttributionQuality,
    SignalContributionStatus,
    RiskContributionType,
    AttributionReportType
)
from usa_signal_bot.core.exceptions import AttributionValidationError


@dataclass
class AttributionTradeEvent:
    event_id: str
    symbol: str
    timestamp_utc: Optional[str] = None
    strategy_name: Optional[str] = None
    signal_id: Optional[str] = None
    signal_family: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    notional_usd: Optional[float] = None
    gross_pnl_usd: Optional[float] = None
    net_pnl_usd: Optional[float] = None
    total_cost_usd: Optional[float] = None
    slippage_cost_usd: Optional[float] = None
    market_impact_cost_usd: Optional[float] = None
    sector: Optional[str] = None
    cluster: Optional[str] = None
    regime_label: Optional[str] = None
    liquidity_bucket: Optional[str] = None
    risk_bucket: Optional[str] = None
    sizing_status: Optional[str] = None
    rebalance_action_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttributionContribution:
    contribution_id: str
    dimension: AttributionDimension
    name: str
    contribution_direction: ContributionDirection
    gross_pnl_usd: float
    net_pnl_usd: float
    total_cost_usd: float
    trade_count: int
    win_count: int
    loss_count: int
    win_rate: Optional[float] = None
    avg_net_pnl_usd: Optional[float] = None
    contribution_pct_total: Optional[float] = None
    quality: AttributionQuality = AttributionQuality.UNKNOWN
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskAttributionContribution:
    contribution_id: str
    risk_type: RiskContributionType
    dimension: AttributionDimension
    name: str
    risk_contribution_score: Optional[float] = None
    drawdown_contribution_usd: Optional[float] = None
    volatility_contribution_proxy: Optional[float] = None
    exposure_contribution_usd: Optional[float] = None
    concentration_contribution_pct: Optional[float] = None
    contribution_direction: ContributionDirection = ContributionDirection.UNKNOWN
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SignalContribution:
    contribution_id: str
    gross_pnl_usd: float
    net_pnl_usd: float
    cost_drag_usd: float
    trade_count: int
    signal_family: Optional[str] = None
    strategy_name: Optional[str] = None
    signal_id: Optional[str] = None
    status: SignalContributionStatus = SignalContributionStatus.UNKNOWN
    win_rate: Optional[float] = None
    avg_signal_score: Optional[float] = None
    avg_confidence: Optional[float] = None
    drawdown_contribution_usd: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttributionScorecard:
    scorecard_id: str
    created_at_utc: str
    total_gross_pnl_usd: float
    total_net_pnl_usd: float
    total_cost_usd: float
    total_trade_count: int
    positive_contributor_count: int
    negative_contributor_count: int
    detrimental_signal_count: int
    high_risk_contributor_count: int
    attribution_quality: AttributionQuality
    summary_scores: Dict[str, Optional[float]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttributionReview:
    review_id: str
    created_at_utc: str
    report_type: AttributionReportType
    events: List[AttributionTradeEvent]
    performance_contributions: List[AttributionContribution]
    risk_contributions: List[RiskAttributionContribution]
    signal_contributions: List[SignalContribution]
    scorecard: Optional[AttributionScorecard] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# --- Serialization ---

def attribution_trade_event_to_dict(item: AttributionTradeEvent) -> Dict[str, Any]:
    return {
        "event_id": item.event_id,
        "symbol": item.symbol,
        "timestamp_utc": item.timestamp_utc,
        "strategy_name": item.strategy_name,
        "signal_id": item.signal_id,
        "signal_family": item.signal_family,
        "side": item.side,
        "quantity": item.quantity,
        "notional_usd": item.notional_usd,
        "gross_pnl_usd": item.gross_pnl_usd,
        "net_pnl_usd": item.net_pnl_usd,
        "total_cost_usd": item.total_cost_usd,
        "slippage_cost_usd": item.slippage_cost_usd,
        "market_impact_cost_usd": item.market_impact_cost_usd,
        "sector": item.sector,
        "cluster": item.cluster,
        "regime_label": item.regime_label,
        "liquidity_bucket": item.liquidity_bucket,
        "risk_bucket": item.risk_bucket,
        "sizing_status": item.sizing_status,
        "rebalance_action_type": item.rebalance_action_type,
        "metadata": item.metadata,
    }


def attribution_contribution_to_dict(item: AttributionContribution) -> Dict[str, Any]:
    return {
        "contribution_id": item.contribution_id,
        "dimension": item.dimension.value,
        "name": item.name,
        "contribution_direction": item.contribution_direction.value,
        "gross_pnl_usd": item.gross_pnl_usd,
        "net_pnl_usd": item.net_pnl_usd,
        "total_cost_usd": item.total_cost_usd,
        "trade_count": item.trade_count,
        "win_count": item.win_count,
        "loss_count": item.loss_count,
        "win_rate": item.win_rate,
        "avg_net_pnl_usd": item.avg_net_pnl_usd,
        "contribution_pct_total": item.contribution_pct_total,
        "quality": item.quality.value,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def risk_attribution_contribution_to_dict(item: RiskAttributionContribution) -> Dict[str, Any]:
    return {
        "contribution_id": item.contribution_id,
        "risk_type": item.risk_type.value,
        "dimension": item.dimension.value,
        "name": item.name,
        "risk_contribution_score": item.risk_contribution_score,
        "drawdown_contribution_usd": item.drawdown_contribution_usd,
        "volatility_contribution_proxy": item.volatility_contribution_proxy,
        "exposure_contribution_usd": item.exposure_contribution_usd,
        "concentration_contribution_pct": item.concentration_contribution_pct,
        "contribution_direction": item.contribution_direction.value,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def signal_contribution_to_dict(item: SignalContribution) -> Dict[str, Any]:
    return {
        "contribution_id": item.contribution_id,
        "signal_family": item.signal_family,
        "strategy_name": item.strategy_name,
        "signal_id": item.signal_id,
        "status": item.status.value,
        "gross_pnl_usd": item.gross_pnl_usd,
        "net_pnl_usd": item.net_pnl_usd,
        "cost_drag_usd": item.cost_drag_usd,
        "trade_count": item.trade_count,
        "win_rate": item.win_rate,
        "avg_signal_score": item.avg_signal_score,
        "avg_confidence": item.avg_confidence,
        "drawdown_contribution_usd": item.drawdown_contribution_usd,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def attribution_scorecard_to_dict(item: AttributionScorecard) -> Dict[str, Any]:
    return {
        "scorecard_id": item.scorecard_id,
        "created_at_utc": item.created_at_utc,
        "total_gross_pnl_usd": item.total_gross_pnl_usd,
        "total_net_pnl_usd": item.total_net_pnl_usd,
        "total_cost_usd": item.total_cost_usd,
        "total_trade_count": item.total_trade_count,
        "positive_contributor_count": item.positive_contributor_count,
        "negative_contributor_count": item.negative_contributor_count,
        "detrimental_signal_count": item.detrimental_signal_count,
        "high_risk_contributor_count": item.high_risk_contributor_count,
        "attribution_quality": item.attribution_quality.value,
        "summary_scores": item.summary_scores,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def attribution_review_to_dict(item: AttributionReview) -> Dict[str, Any]:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value,
        "events": [attribution_trade_event_to_dict(e) for e in item.events],
        "performance_contributions": [attribution_contribution_to_dict(c) for c in item.performance_contributions],
        "risk_contributions": [risk_attribution_contribution_to_dict(c) for c in item.risk_contributions],
        "signal_contributions": [signal_contribution_to_dict(c) for c in item.signal_contributions],
        "scorecard": attribution_scorecard_to_dict(item.scorecard) if item.scorecard else None,
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

# --- Validation ---

def validate_attribution_trade_event(item: AttributionTradeEvent) -> None:
    if not item.symbol:
        raise AttributionValidationError("Symbol cannot be empty.")
    if item.quantity is not None and item.quantity < 0:
        raise AttributionValidationError("Quantity cannot be negative.")
    if item.notional_usd is not None and item.notional_usd < 0:
        raise AttributionValidationError("Notional cannot be negative.")
    if item.total_cost_usd is not None and item.total_cost_usd < 0:
        raise AttributionValidationError("Cost cannot be negative.")


def validate_attribution_contribution(item: AttributionContribution) -> None:
    if item.trade_count < 0:
        raise AttributionValidationError("Trade count cannot be negative.")
    if item.win_rate is not None and (item.win_rate < 0 or item.win_rate > 100):
        raise AttributionValidationError("Win rate must be between 0 and 100.")
    if item.contribution_pct_total is not None and (item.contribution_pct_total < -1000 or item.contribution_pct_total > 1000):
        raise AttributionValidationError("Contribution percentage is outside expected bounds.")


def validate_risk_attribution_contribution(item: RiskAttributionContribution) -> None:
    if not item.name:
        raise AttributionValidationError("Name cannot be empty.")
    if item.concentration_contribution_pct is not None and (item.concentration_contribution_pct < -100 or item.concentration_contribution_pct > 100):
        raise AttributionValidationError("Concentration percentage is outside expected bounds.")


def validate_signal_contribution(item: SignalContribution) -> None:
    if item.trade_count < 0:
        raise AttributionValidationError("Trade count cannot be negative.")
    if item.win_rate is not None and (item.win_rate < 0 or item.win_rate > 100):
        raise AttributionValidationError("Win rate must be between 0 and 100.")


def validate_attribution_review(item: AttributionReview) -> None:
    for e in item.events:
        validate_attribution_trade_event(e)
    for c in item.performance_contributions:
        validate_attribution_contribution(c)
    for r in item.risk_contributions:
        validate_risk_attribution_contribution(r)
    for s in item.signal_contributions:
        validate_signal_contribution(s)


# --- ID Factories ---

def create_attribution_trade_event_id(symbol: str) -> str:
    return f"ev_{symbol.lower()}_{uuid.uuid4().hex[:8]}"

def create_attribution_contribution_id(name: str) -> str:
    safe_name = name.lower().replace(" ", "_").replace("/", "_")
    return f"contrib_{safe_name}_{uuid.uuid4().hex[:8]}"

def create_risk_attribution_contribution_id(name: str) -> str:
    safe_name = name.lower().replace(" ", "_").replace("/", "_")
    return f"rcontrib_{safe_name}_{uuid.uuid4().hex[:8]}"

def create_signal_contribution_id(name: Optional[str] = None) -> str:
    if name:
        safe_name = name.lower().replace(" ", "_").replace("/", "_")
        return f"scontrib_{safe_name}_{uuid.uuid4().hex[:8]}"
    return f"scontrib_{uuid.uuid4().hex[:8]}"

def create_attribution_scorecard_id(prefix: str = "attribution_scorecard") -> str:
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    return f"{prefix}_{timestamp}_{uuid.uuid4().hex[:6]}"

def create_attribution_review_id(prefix: str = "attribution_review") -> str:
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    return f"{prefix}_{timestamp}_{uuid.uuid4().hex[:6]}"
