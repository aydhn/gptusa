from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
import uuid
import datetime

from usa_signal_bot.core.enums import (
    LiquidityStatus,
    TradabilityStatus,
    ExecutionRealismStatus,
    BorrowabilityProxyStatus,
    ExecutionRiskLevel,
    LiquidityMetricName,
    ExecutionGuardReason,
    ExecutionReportType
)
from usa_signal_bot.core.exceptions import ExecutionValidationError

def create_liquidity_metric_id(symbol: str, metric_name: LiquidityMetricName) -> str:
    return f"lmetric_{symbol}_{metric_name.value}_{uuid.uuid4().hex[:8]}"

def create_liquidity_profile_id(symbol: str) -> str:
    return f"lprof_{symbol}_{uuid.uuid4().hex[:8]}"

def create_spread_proxy_estimate_id(symbol: str) -> str:
    return f"spread_{symbol}_{uuid.uuid4().hex[:8]}"

def create_slippage_proxy_estimate_id(symbol: str) -> str:
    return f"slippage_{symbol}_{uuid.uuid4().hex[:8]}"

def create_tradability_guard_id(symbol: str) -> str:
    return f"tguard_{symbol}_{uuid.uuid4().hex[:8]}"

def create_borrowability_proxy_id(symbol: str) -> str:
    return f"borrow_{symbol}_{uuid.uuid4().hex[:8]}"

def create_execution_realism_review_id(prefix: str = "execution_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass
class LiquidityMetric:
    metric_id: str
    symbol: str
    metric_name: LiquidityMetricName
    value: float | int | str | None
    unit: str | None
    created_at_utc: str
    lookback_bars: int | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LiquidityProfile:
    profile_id: str
    symbol: str
    created_at_utc: str
    status: LiquidityStatus
    avg_daily_volume: float | None
    avg_dollar_volume: float | None
    median_daily_volume: float | None
    median_dollar_volume: float | None
    last_price: float | None
    last_volume: float | None
    atr_pct: float | None
    gap_pct: float | None
    stale_data_days: int | None
    metrics: list[LiquidityMetric]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SpreadProxyEstimate:
    estimate_id: str
    symbol: str
    created_at_utc: str
    spread_proxy_bps: float | None
    method: str
    status: ExecutionRealismStatus
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SlippageProxyEstimate:
    estimate_id: str
    symbol: str
    created_at_utc: str
    side: str
    notional_usd: float | None
    participation_rate_pct: float | None
    slippage_proxy_bps: float | None
    status: ExecutionRealismStatus
    risk_level: ExecutionRiskLevel
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TradabilityGuardResult:
    guard_id: str
    symbol: str
    created_at_utc: str
    status: TradabilityStatus
    risk_level: ExecutionRiskLevel
    liquidity_profile: LiquidityProfile | None
    spread_estimate: SpreadProxyEstimate | None
    slippage_estimate: SlippageProxyEstimate | None
    reasons: list[ExecutionGuardReason]
    recommended_guards: list[str]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BorrowabilityProxyResult:
    result_id: str
    symbol: str
    created_at_utc: str
    status: BorrowabilityProxyStatus
    risk_level: ExecutionRiskLevel
    score: float | None
    reasons: list[ExecutionGuardReason]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionRealismReview:
    review_id: str
    created_at_utc: str
    report_type: ExecutionReportType
    symbols: list[str]
    liquidity_profiles: list[LiquidityProfile]
    tradability_results: list[TradabilityGuardResult]
    borrowability_results: list[BorrowabilityProxyResult]
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def validate_liquidity_metric(metric: LiquidityMetric) -> None:
    if not metric.symbol:
        raise ExecutionValidationError("Symbol cannot be empty in LiquidityMetric.")

def validate_liquidity_profile(profile: LiquidityProfile) -> None:
    if not profile.symbol:
        raise ExecutionValidationError("Symbol cannot be empty in LiquidityProfile.")
    if profile.avg_daily_volume is not None and profile.avg_daily_volume < 0:
        raise ExecutionValidationError("Volume cannot be negative.")
    if profile.avg_dollar_volume is not None and profile.avg_dollar_volume < 0:
        raise ExecutionValidationError("Volume cannot be negative.")
    if profile.last_price is not None and profile.last_price <= 0:
        raise ExecutionValidationError("Price cannot be zero or negative.")

def validate_slippage_proxy_estimate(estimate: SlippageProxyEstimate) -> None:
    if not estimate.symbol:
        raise ExecutionValidationError("Symbol cannot be empty.")
    if estimate.slippage_proxy_bps is not None and estimate.slippage_proxy_bps < 0:
        raise ExecutionValidationError("bps cannot be negative.")
    if estimate.participation_rate_pct is not None and estimate.participation_rate_pct < 0:
        raise ExecutionValidationError("Participation rate cannot be negative.")

def validate_tradability_guard_result(result: TradabilityGuardResult) -> None:
    if not result.symbol:
        raise ExecutionValidationError("Symbol cannot be empty.")

def validate_borrowability_proxy_result(result: BorrowabilityProxyResult) -> None:
    if not result.symbol:
        raise ExecutionValidationError("Symbol cannot be empty.")
    if result.score is not None and (result.score < 0 or result.score > 100):
        raise ExecutionValidationError("Score must be between 0 and 100.")

def liquidity_metric_to_dict(metric: LiquidityMetric) -> dict:
    return {
        "metric_id": metric.metric_id,
        "symbol": metric.symbol,
        "metric_name": metric.metric_name.value if hasattr(metric.metric_name, 'value') else metric.metric_name,
        "value": metric.value,
        "unit": metric.unit,
        "created_at_utc": metric.created_at_utc,
        "lookback_bars": metric.lookback_bars,
        "warnings": metric.warnings,
        "errors": metric.errors,
        "metadata": metric.metadata
    }

def liquidity_profile_to_dict(profile: LiquidityProfile) -> dict:
    return {
        "profile_id": profile.profile_id,
        "symbol": profile.symbol,
        "created_at_utc": profile.created_at_utc,
        "status": profile.status.value if hasattr(profile.status, 'value') else profile.status,
        "avg_daily_volume": profile.avg_daily_volume,
        "avg_dollar_volume": profile.avg_dollar_volume,
        "median_daily_volume": profile.median_daily_volume,
        "median_dollar_volume": profile.median_dollar_volume,
        "last_price": profile.last_price,
        "last_volume": profile.last_volume,
        "atr_pct": profile.atr_pct,
        "gap_pct": profile.gap_pct,
        "stale_data_days": profile.stale_data_days,
        "metrics": [liquidity_metric_to_dict(m) for m in profile.metrics],
        "warnings": profile.warnings,
        "errors": profile.errors,
        "metadata": profile.metadata
    }

def spread_proxy_estimate_to_dict(estimate: SpreadProxyEstimate) -> dict:
    return {
        "estimate_id": estimate.estimate_id,
        "symbol": estimate.symbol,
        "created_at_utc": estimate.created_at_utc,
        "spread_proxy_bps": estimate.spread_proxy_bps,
        "method": estimate.method,
        "status": estimate.status.value if hasattr(estimate.status, 'value') else estimate.status,
        "warnings": estimate.warnings,
        "errors": estimate.errors,
        "metadata": estimate.metadata
    }

def slippage_proxy_estimate_to_dict(estimate: SlippageProxyEstimate) -> dict:
    return {
        "estimate_id": estimate.estimate_id,
        "symbol": estimate.symbol,
        "created_at_utc": estimate.created_at_utc,
        "side": estimate.side,
        "notional_usd": estimate.notional_usd,
        "participation_rate_pct": estimate.participation_rate_pct,
        "slippage_proxy_bps": estimate.slippage_proxy_bps,
        "status": estimate.status.value if hasattr(estimate.status, 'value') else estimate.status,
        "risk_level": estimate.risk_level.value if hasattr(estimate.risk_level, 'value') else estimate.risk_level,
        "warnings": estimate.warnings,
        "errors": estimate.errors,
        "metadata": estimate.metadata
    }

def tradability_guard_result_to_dict(result: TradabilityGuardResult) -> dict:
    return {
        "guard_id": result.guard_id,
        "symbol": result.symbol,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value if hasattr(result.status, 'value') else result.status,
        "risk_level": result.risk_level.value if hasattr(result.risk_level, 'value') else result.risk_level,
        "liquidity_profile": liquidity_profile_to_dict(result.liquidity_profile) if result.liquidity_profile else None,
        "spread_estimate": spread_proxy_estimate_to_dict(result.spread_estimate) if result.spread_estimate else None,
        "slippage_estimate": slippage_proxy_estimate_to_dict(result.slippage_estimate) if result.slippage_estimate else None,
        "reasons": [r.value if hasattr(r, 'value') else r for r in result.reasons],
        "recommended_guards": result.recommended_guards,
        "warnings": result.warnings,
        "errors": result.errors,
        "metadata": result.metadata
    }

def borrowability_proxy_result_to_dict(result: BorrowabilityProxyResult) -> dict:
    return {
        "result_id": result.result_id,
        "symbol": result.symbol,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value if hasattr(result.status, 'value') else result.status,
        "risk_level": result.risk_level.value if hasattr(result.risk_level, 'value') else result.risk_level,
        "score": result.score,
        "reasons": [r.value if hasattr(r, 'value') else r for r in result.reasons],
        "warnings": result.warnings,
        "errors": result.errors,
        "metadata": result.metadata
    }

def execution_realism_review_to_dict(review: ExecutionRealismReview) -> dict:
    return {
        "review_id": review.review_id,
        "created_at_utc": review.created_at_utc,
        "report_type": review.report_type.value if hasattr(review.report_type, 'value') else review.report_type,
        "symbols": review.symbols,
        "liquidity_profiles": [liquidity_profile_to_dict(p) for p in review.liquidity_profiles],
        "tradability_results": [tradability_guard_result_to_dict(r) for r in review.tradability_results],
        "borrowability_results": [borrowability_proxy_result_to_dict(r) for r in review.borrowability_results],
        "output_paths": review.output_paths,
        "warnings": review.warnings,
        "errors": review.errors
    }
