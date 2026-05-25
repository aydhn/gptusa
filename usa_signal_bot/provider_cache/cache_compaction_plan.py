from typing import Any
from datetime import datetime, timezone
import uuid
from usa_signal_bot.provider_cache.phase108_models import ProviderCacheIndex, ProviderCacheRecordStatus

def build_cache_compaction_plan(index: ProviderCacheIndex) -> dict[str, Any]:
    stale_count = sum(1 for r in index.records if r.status == ProviderCacheRecordStatus.STALE)
    corrupt_count = sum(1 for r in index.records if r.status == ProviderCacheRecordStatus.CORRUPT)
    empty_count = sum(1 for r in index.records if r.status == ProviderCacheRecordStatus.EMPTY)

    compaction_required = (corrupt_count > 0 or empty_count > 0)

    return {
        "plan_id": f"CCP-{uuid.uuid4().hex[:8].upper()}",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "cache_root": index.cache_root,
        "stale_record_count": stale_count,
        "corrupt_record_count": corrupt_count,
        "empty_record_count": empty_count,
        "compaction_required": compaction_required,
        "destructive_delete_allowed": False,
        "dry_run_only": True,
        "warnings": [],
        "errors": []
    }

def validate_cache_compaction_plan_safety(plan: dict[str, Any]) -> list[str]:
    errors = []
    if plan.get("destructive_delete_allowed"):
        errors.append("destructive_delete_allowed must be false")
    if not plan.get("dry_run_only"):
        errors.append("dry_run_only must be true")
    return errors

def cache_compaction_plan_to_text(plan: dict[str, Any]) -> str:
    return f"Compaction Plan {plan['plan_id']} - Required: {plan['compaction_required']}"
