import os
from pathlib import Path
from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderCacheKey,
    ProviderCacheLookupResult,
    create_provider_cache_lookup_id
)
from usa_signal_bot.core.enums import ProviderCacheLookupStatus, ProviderRuntimeRiskFlag


def run_cache_lookup_dry_run(cache_key: ProviderCacheKey, cache_root: Optional[Path] = None) -> ProviderCacheLookupResult:
    result = ProviderCacheLookupResult(
        lookup_id=create_provider_cache_lookup_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cache_key=cache_key,
        dry_run_only=True,
        cache_enabled=True,
        network_required=False,
        network_used=False
    )

    errors = validate_cache_lookup_result_safety(result)
    if errors:
        result.status = ProviderCacheLookupStatus.BLOCKED
        result.errors.extend(errors)
        result.risk_flags.append(ProviderRuntimeRiskFlag.CACHE_LOOKUP_FAILED)
        return result

    if not cache_key.valid:
        result.status = ProviderCacheLookupStatus.BLOCKED
        result.errors.append("Invalid cache key")
        result.risk_flags.append(ProviderRuntimeRiskFlag.CACHE_KEY_INVALID)
        return result

    if not cache_root:
        # Simulate miss if no root given
        result.status = ProviderCacheLookupStatus.CACHE_MISS
        result.cache_path_exists = False
        return result

    full_path = cache_root / cache_key.cache_path
    if full_path.exists():
        result.status = ProviderCacheLookupStatus.CACHE_HIT
        result.cache_path_exists = True
        try:
            # try to estimate rows for dry run without reading the whole file
            # just read lines count
            with open(full_path, 'r', encoding='utf-8') as f:
                result.rows_available = sum(1 for _ in f) - 1 # minus header
            result.fresh = True
        except Exception as e:
            result.warnings.append(f"Failed to count rows in cache: {str(e)}")
            result.rows_available = 0
    else:
        result.status = ProviderCacheLookupStatus.CACHE_MISS
        result.cache_path_exists = False

    return result


def simulate_cache_hit(cache_key: ProviderCacheKey, rows_available: int = 10) -> ProviderCacheLookupResult:
    result = ProviderCacheLookupResult(
        lookup_id=create_provider_cache_lookup_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cache_key=cache_key,
        status=ProviderCacheLookupStatus.CACHE_HIT,
        dry_run_only=True,
        cache_enabled=True,
        cache_path_exists=True,
        rows_available=rows_available,
        fresh=True,
        network_required=False,
        network_used=False
    )
    return result

def simulate_cache_miss(cache_key: ProviderCacheKey) -> ProviderCacheLookupResult:
    result = ProviderCacheLookupResult(
        lookup_id=create_provider_cache_lookup_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cache_key=cache_key,
        status=ProviderCacheLookupStatus.CACHE_MISS,
        dry_run_only=True,
        cache_enabled=True,
        cache_path_exists=False,
        rows_available=0,
        network_required=False, # We don't require it here since it's dry run
        network_used=False
    )
    return result

def validate_cache_lookup_result_safety(result: ProviderCacheLookupResult) -> List[str]:
    errors = []
    if not result.dry_run_only:
        errors.append("dry_run_only must be True")
    if result.network_used:
        errors.append("network_used must be False")
    return errors


def cache_lookup_dry_run_summary(result: ProviderCacheLookupResult) -> Dict[str, Any]:
    return {
        "lookup_id": result.lookup_id,
        "status": result.status.value,
        "cache_path_exists": result.cache_path_exists,
        "rows_available": result.rows_available
    }

def cache_lookup_dry_run_to_text(result: ProviderCacheLookupResult) -> str:
    lines = [
        "=== Provider Cache Lookup Result ===",
        f"ID: {result.lookup_id}",
        f"Status: {result.status.value}",
        f"Cache Path Exists: {result.cache_path_exists}",
        f"Rows Available: {result.rows_available}",
        ""
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
