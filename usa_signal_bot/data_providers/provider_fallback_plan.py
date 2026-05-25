
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderFallbackPlan, ProviderRegistryEntry, create_provider_fallback_plan_id, _now
from usa_signal_bot.core.enums import DataProviderKind, DataProviderCapability, ProviderSelectorMode

def build_provider_fallback_plan(provider_kind: DataProviderKind, capability: DataProviderCapability, entries: list[ProviderRegistryEntry] | None = None) -> ProviderFallbackPlan:
    return ProviderFallbackPlan(
        plan_id=create_provider_fallback_plan_id(),
        created_at_utc=_now(),
        provider_kind=provider_kind,
        capability=capability,
        primary_provider=None,
        fallback_chain=[],
        fallback_mode=ProviderSelectorMode.METADATA_ONLY,
        max_attempts=3,
        network_allowed=False,
        paid_api_allowed=False,
        scraping_allowed=False,
        broker_allowed=False,
        order_allowed=False,
        plan_safe=True
    )

def build_default_provider_fallback_plans(entries: list[ProviderRegistryEntry] | None = None) -> list[ProviderFallbackPlan]:
    return []

def validate_provider_fallback_plan_safety(plan: ProviderFallbackPlan) -> list[str]:
    return []

def provider_fallback_plan_summary(plan: ProviderFallbackPlan) -> dict[str, Any]:
    return {"safe": plan.plan_safe}

def provider_fallback_plan_to_text(plan: ProviderFallbackPlan) -> str:
    return f"Fallback Plan {plan.plan_id}"
