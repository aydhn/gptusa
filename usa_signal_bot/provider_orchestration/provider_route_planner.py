from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ProviderRouteStatus, ProviderRouteDecision, SourceBlendMethod
from usa_signal_bot.provider_orchestration.phase110_models import (
    OrchestratedDataRequest, ProviderRoutePlan, create_orchestrated_data_request_id,
    create_provider_route_plan_id, validate_provider_route_plan, validate_orchestrated_data_request
)

def build_orchestrated_data_request(symbol: str, capability: str = "GET_DAILY_OHLCV",
                                    interval: str | None = "1d", preferred_provider: str | None = None,
                                    allow_blending: bool = True, allow_fallback: bool = True) -> OrchestratedDataRequest:
    req = OrchestratedDataRequest(
        request_id=create_orchestrated_data_request_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        capability=capability,
        interval=interval,
        preferred_provider=preferred_provider,
        allow_blending=allow_blending,
        allow_fallback=allow_fallback,
        cache_only=True,
        local_fixture_allowed=True,
        dry_run_only=True,
        research_data_only=True,
        allow_network=False,
        allow_paid_api=False,
        allow_scraping=False,
        allow_html_parsing=False,
        allow_broker=False,
        allow_order=False,
        allow_paper_mutation=False,
        metadata={}
    )
    validate_orchestrated_data_request(req)
    return req

def build_provider_route_plan(request: OrchestratedDataRequest, provider_quality_payload: dict[str, Any] | None = None) -> ProviderRoutePlan:
    plan = ProviderRoutePlan(
        route_plan_id=create_provider_route_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        request_id=request.request_id,
        symbol=request.symbol,
        capability=request.capability,
        interval=request.interval,
        route_status=ProviderRouteStatus.PLANNED,
        route_decision=ProviderRouteDecision.UNKNOWN,
        primary_provider=request.preferred_provider,
        source_blend_method=SourceBlendMethod.UNKNOWN,
        cache_only=True,
        dry_run_only=True,
        research_data_only=True,
        network_required=False,
        refresh_required_future=False,
        metadata={}
    )

    if provider_quality_payload:
        scores = provider_quality_payload.get("selection_scores", [])
        symbol_scores = [s for s in scores if s.get("symbol") == request.symbol]
        if symbol_scores:
            symbol_scores.sort(key=lambda x: x.get("selection_score", 0), reverse=True)
            candidate_providers = [s.get("provider_name") for s in symbol_scores if s.get("provider_name")]
            plan.candidate_providers = candidate_providers

            if not plan.primary_provider and candidate_providers:
                plan.primary_provider = candidate_providers[0]

            if request.allow_fallback:
                plan.fallback_providers = [p for p in candidate_providers if p != plan.primary_provider]

    errors = validate_provider_route_plan_safety(plan)
    if errors:
        plan.errors.extend(errors)
        plan.route_status = ProviderRouteStatus.BLOCKED
        plan.route_decision = ProviderRouteDecision.BLOCK

    validate_provider_route_plan(plan)
    return plan

def build_default_provider_route_plans(symbols: list[str] | None = None) -> list[ProviderRoutePlan]:
    if not symbols:
        symbols = ["AAPL", "MSFT", "SPY"]

    plans = []
    for sym in symbols:
        req = build_orchestrated_data_request(sym)
        plan = build_provider_route_plan(req)
        plans.append(plan)
    return plans

def validate_provider_route_plan_safety(plan: ProviderRoutePlan) -> list[str]:
    errors = []
    if not plan.cache_only: errors.append("cache_only must be True")
    if not plan.dry_run_only: errors.append("dry_run_only must be True")
    if not plan.research_data_only: errors.append("research_data_only must be True")
    if plan.network_required: errors.append("network_required must be False")
    return errors

def provider_route_plan_summary(plan: ProviderRoutePlan) -> dict[str, Any]:
    return {
        "symbol": plan.symbol,
        "status": plan.route_status.value,
        "primary": plan.primary_provider,
        "fallbacks": plan.fallback_providers
    }

def provider_route_plan_to_text(plan: ProviderRoutePlan) -> str:
    lines = [
        f"--- Route Plan {plan.symbol} ---",
        f"Status: {plan.route_status.value}",
        f"Decision: {plan.route_decision.value}",
        f"Primary: {plan.primary_provider}",
        f"Fallbacks: {plan.fallback_providers}",
        f"Errors: {plan.errors}"
    ]
    return "\n".join(lines)
