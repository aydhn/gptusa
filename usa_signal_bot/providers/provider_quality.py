from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import ProviderQualityStatus
from usa_signal_bot.providers.provider_models import ProviderResponse, ProviderQualityScore, create_provider_quality_score_id
from usa_signal_bot.providers.provider_validation import (
    validate_provider_response_schema, validate_freshness, validate_completeness
)

def score_provider_response_quality(response: ProviderResponse) -> ProviderQualityScore:
    warnings = []
    errors = []

    freshness = score_freshness(response)
    completeness = score_completeness(response)
    schema = score_schema(response)
    ohlcv = score_ohlcv_consistency(response)
    latency = score_latency(response)
    err_score = score_errors(response)

    parts = {
        "freshness": freshness,
        "completeness": completeness,
        "schema": schema,
        "ohlcv": ohlcv,
        "latency": latency,
        "errors": err_score
    }

    combined = combine_provider_quality_scores(parts)
    status = classify_provider_quality(combined, errors)

    if schema == 0.0 or ohlcv == 0.0:
        status = ProviderQualityStatus.POOR
        errors.append("Critical validation failure (schema or ohlcv is 0)")

    return ProviderQualityScore(
        score_id=create_provider_quality_score_id(),
        provider_name=response.provider_name,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        score=combined,
        freshness_score=freshness,
        completeness_score=completeness,
        schema_score=schema,
        ohlcv_score=ohlcv,
        latency_score=latency,
        error_score=err_score,
        evidence={"row_count": response.row_count, "symbol_count": response.symbol_count, "latency_ms": response.latency_ms},
        warnings=warnings,
        errors=errors
    )

def score_freshness(response: ProviderResponse) -> float | None:
    if not response.data:
        return 0.0
    # simplified logic
    all_fresh = True
    for symbol, rows in response.data.items():
        valid, warns, errs = validate_freshness(rows, max_staleness_days=7)
        if warns or errs:
            all_fresh = False
    return 100.0 if all_fresh else 50.0

def score_completeness(response: ProviderResponse) -> float | None:
    if not response.data:
        return 0.0
    all_complete = True
    for symbol, rows in response.data.items():
        valid, warns, errs = validate_completeness(rows, min_rows=20)
        if warns:
            all_complete = False
    return 100.0 if all_complete else 50.0

def score_schema(response: ProviderResponse) -> float | None:
    if not response.data:
        return 0.0
    valid, warns, errs = validate_provider_response_schema(response)
    if errs:
        return 0.0
    if warns:
        return 80.0
    return 100.0

def score_ohlcv_consistency(response: ProviderResponse) -> float | None:
    # already checked in schema
    valid, warns, errs = validate_provider_response_schema(response)
    if errs:
        return 0.0
    return 100.0

def score_latency(response: ProviderResponse) -> float | None:
    if response.latency_ms is None:
        return None
    if response.latency_ms < 500:
        return 100.0
    if response.latency_ms < 2000:
        return 80.0
    if response.latency_ms < 5000:
        return 50.0
    return 20.0

def score_errors(response: ProviderResponse) -> float | None:
    if response.errors:
        return 0.0
    if response.warnings:
        return 50.0
    return 100.0

def combine_provider_quality_scores(parts: dict[str, float | None]) -> float | None:
    weights = {
        "freshness": 0.20,
        "completeness": 0.20,
        "schema": 0.20,
        "ohlcv": 0.20,
        "latency": 0.10,
        "errors": 0.10
    }

    total_score = 0.0
    total_weight = 0.0

    for key, val in parts.items():
        if val is not None:
            total_score += val * weights[key]
            total_weight += weights[key]

    if total_weight == 0.0:
        return None

    # normalize
    return (total_score / total_weight)

def classify_provider_quality(score: float | None, errors: list[str] | None = None) -> ProviderQualityStatus:
    if errors:
        return ProviderQualityStatus.POOR

    if score is None:
        return ProviderQualityStatus.UNKNOWN

    if score >= 90.0:
        return ProviderQualityStatus.EXCELLENT
    if score >= 75.0:
        return ProviderQualityStatus.GOOD
    if score >= 60.0:
        return ProviderQualityStatus.ACCEPTABLE
    if score >= 40.0:
        return ProviderQualityStatus.DEGRADED
    return ProviderQualityStatus.POOR

def provider_quality_score_to_text(score: ProviderQualityScore) -> str:
    lines = [
        f"--- Provider Quality Score: {score.provider_name.value} ---",
        f"Status: {score.status.value}",
        f"Overall Score: {score.score:.2f}" if score.score is not None else "Overall Score: None",
        f"Freshness: {score.freshness_score}",
        f"Completeness: {score.completeness_score}",
        f"Schema: {score.schema_score}",
        f"OHLCV: {score.ohlcv_score}",
        f"Latency: {score.latency_score}",
        f"Errors: {score.error_score}"
    ]
    if score.warnings:
        lines.append(f"Warnings: {len(score.warnings)}")
    if score.errors:
        lines.append(f"Errors: {len(score.errors)}")
    return "\n".join(lines)
