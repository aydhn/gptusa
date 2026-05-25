from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ProviderRouteStatus, ProviderRouteDecision, ProviderOrchestrationRiskFlag
from usa_signal_bot.provider_orchestration.phase110_models import (
    ProviderRoutePlan, ProviderRouteResult, create_provider_route_result_id,
    validate_provider_route_result
)

class ProviderRouteSelector:
    def __init__(self, provider_quality_payload: dict[str, Any] | None = None, policy: dict[str, Any] | None = None):
        self.provider_quality_payload = provider_quality_payload
        self.policy = policy or {}

    def select_route(self, plan: ProviderRoutePlan) -> ProviderRouteResult:
        res = ProviderRouteResult(
            route_result_id=create_provider_route_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            route_plan_id=plan.route_plan_id,
            selected_provider=None,
            selected_fallback_provider=None,
            route_status=ProviderRouteStatus.UNKNOWN,
            route_decision=ProviderRouteDecision.UNKNOWN,
            used_blended_source=False,
            used_cache_only=True,
            used_local_fixture=False,
            network_used=False,
            paid_api_used=False,
            scraping_used=False,
            html_parsing_used=False,
            broker_used=False,
            order_created=False,
            paper_state_mutated=False,
            telegram_real_sent=False,
            dashboard_started=False,
            passed=False,
            risk_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )

        if plan.route_status == ProviderRouteStatus.BLOCKED:
            res.route_status = ProviderRouteStatus.BLOCKED
            res.route_decision = ProviderRouteDecision.BLOCK
            res.errors.append("Route plan is blocked")
            return res

        # Select logic
        if plan.primary_provider:
            res.selected_provider = plan.primary_provider
            res.route_status = ProviderRouteStatus.SELECTED_PRIMARY
            res.route_decision = ProviderRouteDecision.USE_PRIMARY_PROVIDER_FOR_RESEARCH_DATA
            res.passed = True
        elif plan.fallback_providers:
            res.selected_fallback_provider = plan.fallback_providers[0]
            res.route_status = ProviderRouteStatus.SELECTED_FALLBACK
            res.route_decision = ProviderRouteDecision.USE_FALLBACK_PROVIDER_FOR_RESEARCH_DATA
            res.passed = True
        else:
            res.route_status = ProviderRouteStatus.NO_AVAILABLE_PROVIDER
            res.route_decision = ProviderRouteDecision.INCONCLUSIVE
            res.risk_flags.append(ProviderOrchestrationRiskFlag.NO_PROVIDER_AVAILABLE)
            res.passed = False

        errors = self.validate_route_result_safety(res)
        if errors:
            res.errors.extend(errors)
            res.passed = False
            res.route_status = ProviderRouteStatus.BLOCKED
            res.route_decision = ProviderRouteDecision.BLOCK

        validate_provider_route_result(res)
        return res

    def select_batch(self, plans: list[ProviderRoutePlan]) -> list[ProviderRouteResult]:
        return [self.select_route(p) for p in plans]

    def validate_route_result_safety(self, result: ProviderRouteResult) -> list[str]:
        errors = []
        if result.network_used: errors.append("network_used must be False")
        if result.paid_api_used: errors.append("paid_api_used must be False")
        if result.scraping_used: errors.append("scraping_used must be False")
        if result.html_parsing_used: errors.append("html_parsing_used must be False")
        if result.broker_used: errors.append("broker_used must be False")
        if result.order_created: errors.append("order_created must be False")
        if result.paper_state_mutated: errors.append("paper_state_mutated must be False")
        return errors

def route_selector_summary(results: list[ProviderRouteResult]) -> dict[str, Any]:
    return {
        "total": len(results),
        "passed": sum(1 for r in results if r.passed),
        "blocked": sum(1 for r in results if r.route_status == ProviderRouteStatus.BLOCKED)
    }
