import hashlib
import json
import re
from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderCacheKey,
    create_provider_cache_key_id
)
from usa_signal_bot.core.exceptions import ProviderCacheKeyError
from usa_signal_bot.core.enums import ProviderRuntimeRiskFlag

def sanitize_cache_key_part(value: Optional[str]) -> str:
    if not value:
        return ""

    # allow only alphanumeric and underscore/dash
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', value)
    return sanitized.strip('_')

def stable_cache_key_hash(payload: Dict[str, Any]) -> str:
    # Ensure stable json dump
    json_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()

def build_provider_cache_key(
    provider_name: str,
    capability: str,
    symbol: Optional[str] = None,
    interval: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    adjusted: bool = True,
    cache_namespace: str = "market_data"
) -> ProviderCacheKey:

    if not provider_name or not capability:
        raise ProviderCacheKeyError("provider_name and capability are required")

    cache_key = ProviderCacheKey(
        cache_key_id=create_provider_cache_key_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_name=provider_name,
        capability=capability,
        symbol=symbol,
        interval=interval,
        start_date=start_date,
        end_date=end_date,
        adjusted=adjusted,
        cache_namespace=cache_namespace
    )

    parts = [
        sanitize_cache_key_part(provider_name.lower()),
        sanitize_cache_key_part(capability.lower())
    ]

    if symbol:
        parts.append(sanitize_cache_key_part(symbol.lower()))
    if interval:
        parts.append(sanitize_cache_key_part(interval.lower()))

    date_parts = []
    if start_date:
        date_parts.append(sanitize_cache_key_part(start_date))
    if end_date:
        date_parts.append(sanitize_cache_key_part(end_date))

    if date_parts:
        parts.append("-".join(date_parts))

    parts.append("adj" if adjusted else "unadj")

    key_str = "_".join(p for p in parts if p)

    # Hash for the final path logic to avoid long names
    payload = {
        "p": provider_name,
        "c": capability,
        "s": symbol,
        "i": interval,
        "sd": start_date,
        "ed": end_date,
        "a": adjusted
    }
    key_hash = stable_cache_key_hash(payload)[:12]

    cache_key.cache_key = f"{key_str}_{key_hash}"
    cache_key.cache_path = f"{cache_namespace}/{provider_name.lower()}/{cache_key.cache_key}.csv"
    cache_key.valid = True

    errors = validate_provider_cache_key_safety(cache_key)
    if errors:
        cache_key.valid = False
        cache_key.errors.extend(errors)

    return cache_key


def validate_provider_cache_key_safety(key: ProviderCacheKey) -> List[str]:
    errors = []
    if ".." in key.cache_path or "/" == key.cache_path[0]:
        errors.append("Path traversal detected in cache key")

    if "secret" in key.cache_key.lower() or "token" in key.cache_key.lower():
        errors.append("Secret or token detected in cache key")

    return errors


def provider_cache_key_summary(key: ProviderCacheKey) -> Dict[str, Any]:
    return {
        "cache_key_id": key.cache_key_id,
        "provider": key.provider_name,
        "capability": key.capability,
        "symbol": key.symbol,
        "cache_path": key.cache_path,
        "valid": key.valid
    }

def provider_cache_key_to_text(key: ProviderCacheKey) -> str:
    lines = [
        "=== Provider Cache Key ===",
        f"ID: {key.cache_key_id}",
        f"Path: {key.cache_path}",
        f"Valid: {key.valid}",
        ""
    ]
    if key.errors:
        lines.append("Errors:")
        for e in key.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
