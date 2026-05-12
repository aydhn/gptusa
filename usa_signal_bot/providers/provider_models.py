from dataclasses import dataclass, field
from typing import Any, Optional
import datetime
import uuid

from usa_signal_bot.core.enums import (
    DataProviderName, DataProviderType, ProviderCapability, ProviderRequestType,
    ProviderResponseStatus, ProviderQualityStatus, ProviderRoutingDecision, ProviderReportType
)

@dataclass
class ProviderRequest:
    request_id: str
    provider_name: DataProviderName
    request_type: ProviderRequestType
    symbols: list[str]
    interval: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    adjusted: bool = True
    use_cache: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderResponse:
    response_id: str
    request_id: str
    provider_name: DataProviderName
    status: ProviderResponseStatus
    created_at_utc: str
    symbol_count: int
    row_count: int
    data: dict[str, Any]
    latency_ms: Optional[float] = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderCapabilityProfile:
    provider_name: DataProviderName
    provider_type: DataProviderType
    capabilities: list[ProviderCapability]
    requires_api_key: bool
    supports_offline: bool
    supports_bulk: bool
    supports_adjusted: bool
    notes: list[str] = field(default_factory=list)

@dataclass
class ProviderHealthResult:
    health_id: str
    provider_name: DataProviderName
    checked_at_utc: str
    status: ProviderQualityStatus
    reachable: bool
    capability_status: dict[str, bool]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    latency_ms: Optional[float] = None

@dataclass
class ProviderQualityScore:
    score_id: str
    provider_name: DataProviderName
    created_at_utc: str
    status: ProviderQualityStatus
    evidence: dict[str, Any]
    score: Optional[float] = None
    freshness_score: Optional[float] = None
    completeness_score: Optional[float] = None
    schema_score: Optional[float] = None
    ohlcv_score: Optional[float] = None
    latency_score: Optional[float] = None
    error_score: Optional[float] = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class ProviderRoutingResult:
    routing_id: str
    created_at_utc: str
    request: ProviderRequest
    decision: ProviderRoutingDecision
    selected_provider: DataProviderName
    attempted_providers: list[DataProviderName]
    quality_scores: list[ProviderQualityScore]
    fallback_used: bool
    response: Optional[ProviderResponse] = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class ProviderReviewResult:
    review_id: str
    created_at_utc: str
    report_type: ProviderReportType
    health_results: list[ProviderHealthResult]
    quality_scores: list[ProviderQualityScore]
    routing_results: list[ProviderRoutingResult]
    output_paths: dict[str, str]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_provider_request_id(prefix: str = "provider_req") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_provider_response_id(prefix: str = "provider_resp") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_provider_health_id(prefix: str = "provider_health") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_provider_quality_score_id(prefix: str = "provider_quality") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_provider_routing_id(prefix: str = "provider_route") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_provider_review_id(prefix: str = "provider_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def provider_request_to_dict(request: ProviderRequest) -> dict:
    return {
        "request_id": request.request_id,
        "provider_name": request.provider_name.value,
        "request_type": request.request_type.value,
        "symbols": request.symbols,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "interval": request.interval,
        "adjusted": request.adjusted,
        "use_cache": request.use_cache,
        "metadata": request.metadata
    }

def provider_response_to_dict(response: ProviderResponse) -> dict:
    return {
        "response_id": response.response_id,
        "request_id": response.request_id,
        "provider_name": response.provider_name.value,
        "status": response.status.value,
        "created_at_utc": response.created_at_utc,
        "symbol_count": response.symbol_count,
        "row_count": response.row_count,
        "data": response.data,
        "latency_ms": response.latency_ms,
        "warnings": response.warnings,
        "errors": response.errors,
        "metadata": response.metadata
    }

def capability_profile_to_dict(profile: ProviderCapabilityProfile) -> dict:
    return {
        "provider_name": profile.provider_name.value,
        "provider_type": profile.provider_type.value,
        "capabilities": [c.value for c in profile.capabilities],
        "requires_api_key": profile.requires_api_key,
        "supports_offline": profile.supports_offline,
        "supports_bulk": profile.supports_bulk,
        "supports_adjusted": profile.supports_adjusted,
        "notes": profile.notes
    }

def provider_health_result_to_dict(result: ProviderHealthResult) -> dict:
    return {
        "health_id": result.health_id,
        "provider_name": result.provider_name.value,
        "checked_at_utc": result.checked_at_utc,
        "status": result.status.value,
        "reachable": result.reachable,
        "latency_ms": result.latency_ms,
        "capability_status": result.capability_status,
        "warnings": result.warnings,
        "errors": result.errors
    }

def provider_quality_score_to_dict(score: ProviderQualityScore) -> dict:
    return {
        "score_id": score.score_id,
        "provider_name": score.provider_name.value,
        "created_at_utc": score.created_at_utc,
        "score": score.score,
        "status": score.status.value,
        "freshness_score": score.freshness_score,
        "completeness_score": score.completeness_score,
        "schema_score": score.schema_score,
        "ohlcv_score": score.ohlcv_score,
        "latency_score": score.latency_score,
        "error_score": score.error_score,
        "evidence": score.evidence,
        "warnings": score.warnings,
        "errors": score.errors
    }

def provider_routing_result_to_dict(result: ProviderRoutingResult) -> dict:
    return {
        "routing_id": result.routing_id,
        "created_at_utc": result.created_at_utc,
        "request": provider_request_to_dict(result.request),
        "decision": result.decision.value,
        "selected_provider": result.selected_provider.value,
        "attempted_providers": [p.value for p in result.attempted_providers],
        "response": provider_response_to_dict(result.response) if result.response else None,
        "quality_scores": [provider_quality_score_to_dict(q) for q in result.quality_scores],
        "fallback_used": result.fallback_used,
        "warnings": result.warnings,
        "errors": result.errors
    }

def provider_review_result_to_dict(result: ProviderReviewResult) -> dict:
    return {
        "review_id": result.review_id,
        "created_at_utc": result.created_at_utc,
        "report_type": result.report_type.value,
        "health_results": [provider_health_result_to_dict(h) for h in result.health_results],
        "quality_scores": [provider_quality_score_to_dict(q) for q in result.quality_scores],
        "routing_results": [provider_routing_result_to_dict(r) for r in result.routing_results],
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_provider_request(request: ProviderRequest) -> None:
    if not request.symbols:
        raise ValueError("symbols array cannot be empty")
    if not request.interval:
        raise ValueError("interval cannot be empty")

def validate_provider_response(response: ProviderResponse) -> None:
    pass

def validate_provider_quality_score(score: ProviderQualityScore) -> None:
    if score.score is not None and (score.score < 0 or score.score > 100):
        raise ValueError("score must be between 0 and 100")
    if score.latency_score is not None and (score.latency_score < 0 or score.latency_score > 100):
        raise ValueError("latency_score must be between 0 and 100")
