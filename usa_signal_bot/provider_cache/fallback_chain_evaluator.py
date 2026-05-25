from typing import Any
from usa_signal_bot.provider_cache.phase108_models import (
    FallbackDryRunPlan,
    ProviderCacheIndex,
    ProviderCacheRecord,
    ProviderCacheRecordStatus
)

def evaluate_fallback_chain(plan: FallbackDryRunPlan, cache_index: ProviderCacheIndex) -> dict[str, Any]:
    # Simulate finding records for each provider in chain
    attempted = []
    skipped = []
    selected_provider = None
    selected_record = None

    for provider in plan.fallback_chain:
        attempted.append(provider)
        # Find record
        records = [r for r in cache_index.records if r.provider_name == provider and r.symbol == plan.symbol and r.capability == plan.capability]
        # Prefer validated/fresh
        valid_records = [r for r in records if r.status in [ProviderCacheRecordStatus.VALIDATED, ProviderCacheRecordStatus.FRESH, ProviderCacheRecordStatus.STALE]]
        if valid_records:
            selected_provider = provider
            selected_record = valid_records[0]
            skipped = [p for p in plan.fallback_chain if p not in attempted]
            break

    return {
        "selected_provider": selected_provider,
        "selected_record_id": selected_record.record_id if selected_record else None,
        "attempted": attempted,
        "skipped": skipped,
        "exhausted": selected_provider is None,
        "stale_used": selected_record.status == ProviderCacheRecordStatus.STALE if selected_record else False
    }

def choose_first_usable_cache_record(plan: FallbackDryRunPlan, cache_index: ProviderCacheIndex) -> ProviderCacheRecord | None:
    for provider in plan.fallback_chain:
        records = [r for r in cache_index.records if r.provider_name == provider and r.symbol == plan.symbol]
        for r in records:
            if r.status in [ProviderCacheRecordStatus.VALIDATED, ProviderCacheRecordStatus.FRESH, ProviderCacheRecordStatus.STALE]:
                return r
    return None

def fallback_chain_has_unsafe_provider(plan: FallbackDryRunPlan) -> bool:
    unsafe_keywords = ["BROKER", "LIVE", "PAPER", "PAID"]
    for p in plan.fallback_chain:
        if any(k in p.upper() for k in unsafe_keywords):
            return True
    return False

def fallback_chain_evaluator_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"selected": payload.get("selected_provider")}

def fallback_chain_evaluator_to_text(payload: dict[str, Any]) -> str:
    return f"Fallback Evaluated - Selected: {payload.get('selected_provider')}"
