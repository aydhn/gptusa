from usa_signal_bot.provider_cache.phase108_models import (
    ProviderCacheContext,
    ProviderCacheRecord,
    ProviderCacheIndex,
    FallbackDryRunResult,
    ProviderCacheRiskFlag
)
from usa_signal_bot.core.exceptions import ProviderCacheSafetyValidationError
from typing import Any

def validate_provider_cache_context_safety(context: ProviderCacheContext) -> list[str]:
    errors = []
    if context.network_enabled_by_default: errors.append("network_enabled_by_default true")
    if context.paid_api_enabled: errors.append("paid_api_enabled true")
    if context.scraping_enabled: errors.append("scraping_enabled true")
    if context.broker_execution_enabled: errors.append("broker_execution_enabled true")
    if context.order_creation_enabled: errors.append("order_creation_enabled true")
    if context.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled true")
    if context.telegram_real_send_enabled: errors.append("telegram_real_send_enabled true")
    if context.dashboard_enabled: errors.append("dashboard_enabled true")

    for plan in context.fallback_plans:
        if plan.allow_network: errors.append("fallback plan allow_network true")

    for res in context.fallback_results:
        if res.network_used: errors.append("fallback result network_used true")
        if res.order_created: errors.append("fallback result order_created true")
        if res.paper_state_mutated: errors.append("fallback result paper_state_mutated true")

    for res in context.source_comparisons:
        if res.network_used: errors.append("source comparison network_used true")

    return errors

def validate_cache_record_safety(record: ProviderCacheRecord) -> list[str]:
    if ".." in record.cache_path:
        return ["Path traversal detected"]
    return []

def validate_cache_index_safety(index: ProviderCacheIndex) -> list[str]:
    errors = []
    for r in index.records:
        errors.extend(validate_cache_record_safety(r))
    return errors

def validate_fallback_results_safety(results: list[FallbackDryRunResult]) -> list[str]:
    errors = []
    for r in results:
        if r.network_used: errors.append("network_used true")
        if r.order_created: errors.append("order_created true")
    return errors

def collect_cache_risk_flags(context: ProviderCacheContext | None = None) -> list[ProviderCacheRiskFlag]:
    if not context: return []
    flags = set(context.risk_flags)
    for p in context.fallback_plans:
        flags.update(p.risk_flags)
    for r in context.fallback_results:
        flags.update(r.risk_flags)
    for c in context.source_comparisons:
        flags.update(c.risk_flags)
    return list(flags)

def cache_safety_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": errors}

def cache_safety_validator_to_text(errors: list[str]) -> str:
    if not errors: return "Cache Context is safe."
    return f"Cache Safety Errors: {errors}"
