from typing import Any

from usa_signal_bot.providers.provider_models import (
    ProviderRequest, ProviderResponse, ProviderCapabilityProfile, ProviderHealthResult,
    ProviderQualityScore, ProviderRoutingResult, ProviderReviewResult
)
from usa_signal_bot.providers.provider_health import provider_health_result_to_text
from usa_signal_bot.providers.provider_quality import provider_quality_score_to_text
from usa_signal_bot.providers.provider_capabilities import capability_profiles_to_text

def provider_request_to_text(request: ProviderRequest) -> str:
    lines = [
        f"--- Provider Request: {request.request_id} ---",
        f"Provider: {request.provider_name.value}",
        f"Type: {request.request_type.value}",
        f"Symbols: {len(request.symbols)} ({', '.join(request.symbols[:5])}{'...' if len(request.symbols) > 5 else ''})",
        f"Interval: {request.interval}"
    ]
    return "\n".join(lines)

def provider_response_to_text(response: ProviderResponse) -> str:
    lines = [
        f"--- Provider Response: {response.response_id} ---",
        f"Provider: {response.provider_name.value}",
        f"Status: {response.status.value}",
        f"Rows: {response.row_count}",
        f"Latency: {response.latency_ms:.2f}ms" if response.latency_ms is not None else "Latency: Unknown"
    ]
    if response.warnings:
        lines.append("Warnings:")
        for w in response.warnings:
            lines.append(f"  - {w}")
    if response.errors:
        lines.append("Errors:")
        for e in response.errors:
            lines.append(f"  - {e}")
    return "\n".join(lines)

def capability_profile_to_text(profile: ProviderCapabilityProfile) -> str:
    return capability_profiles_to_text([profile])

def provider_routing_result_to_text(result: ProviderRoutingResult) -> str:
    lines = [
        f"--- Provider Routing Result: {result.routing_id} ---",
        f"Decision: {result.decision.value}",
        f"Selected: {result.selected_provider.value}",
        f"Attempted: {[p.value for p in result.attempted_providers]}",
        f"Fallback Used: {result.fallback_used}"
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f"  - {e}")
    return "\n".join(lines)

def provider_review_result_to_text(result: ProviderReviewResult) -> str:
    lines = [
        f"--- Provider Review: {result.review_id} ---",
        f"Report Type: {result.report_type.value}",
        f"Health Results: {len(result.health_results)}",
        f"Quality Scores: {len(result.quality_scores)}",
        f"Routing Results: {len(result.routing_results)}",
        provider_limitations_text()
    ]
    return "\n".join(lines)

def provider_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "--- Provider Store Summary ---",
        f"Health Files: {summary['health_files']}",
        f"Quality Files: {summary['quality_files']}",
        f"Routing Files: {summary['routing_files']}",
        f"Review Files: {summary['review_files']}"
    ]
    return "\n".join(lines)

def provider_limitations_text() -> str:
    return """
--- Provider Limitations & Disclaimers ---
* No paid providers are used.
* No web scraping is performed.
* No live or demo broker execution occurs.
* Provider scores are for data quality only, NOT investment advice.
* Fallback selection does not guarantee correctness of data.
"""
