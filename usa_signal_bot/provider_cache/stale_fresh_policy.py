from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import StaleFreshPolicy, create_stale_fresh_policy_id

def build_default_stale_fresh_policy() -> StaleFreshPolicy:
    return StaleFreshPolicy(
        policy_id=create_stale_fresh_policy_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        default_ttl_seconds=86400,
        intraday_ttl_seconds=900,
        daily_ttl_seconds=86400,
        fundamentals_ttl_seconds=604800,
        macro_ttl_seconds=86400,
        allow_stale_read=True,
        stale_read_requires_warning=True,
        block_expired=False,
        timezone="UTC",
        policy_valid=True,
        warnings=[],
        errors=[],
        metadata={}
    )

def ttl_for_capability(policy: StaleFreshPolicy, capability: str, interval: str | None = None) -> int:
    if "FUNDAMENTALS" in capability.upper():
        return policy.fundamentals_ttl_seconds
    if "MACRO" in capability.upper():
        return policy.macro_ttl_seconds
    if interval and ("m" in interval.lower() or "h" in interval.lower()):
        return policy.intraday_ttl_seconds
    return policy.daily_ttl_seconds

def validate_stale_fresh_policy_safety(policy: StaleFreshPolicy) -> list[str]:
    return []

def stale_fresh_policy_summary(policy: StaleFreshPolicy) -> dict[str, Any]:
    return {"id": policy.policy_id, "default_ttl": policy.default_ttl_seconds}

def stale_fresh_policy_to_text(policy: StaleFreshPolicy) -> str:
    return f"Policy {policy.policy_id} - Valid: {policy.policy_valid}"
