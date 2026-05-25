from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    StaleFreshEvaluation,
    StaleFreshStatus,
    ProviderCacheRecord,
    StaleFreshPolicy,
    create_stale_fresh_evaluation_id,
    ProviderCacheRiskFlag
)
from usa_signal_bot.provider_cache.stale_fresh_policy import build_default_stale_fresh_policy, ttl_for_capability

def evaluate_cache_record_stale_fresh(record: ProviderCacheRecord, policy: StaleFreshPolicy | None = None, now_utc: str | None = None) -> StaleFreshEvaluation:
    if not policy:
        policy = build_default_stale_fresh_policy()

    now = datetime.fromisoformat(now_utc) if now_utc else datetime.now(timezone.utc)
    now_str = now.isoformat()

    ttl = ttl_for_capability(policy, record.capability, record.interval)

    if not record.fetched_at_utc:
        return StaleFreshEvaluation(
            evaluation_id=create_stale_fresh_evaluation_id(),
            created_at_utc=now_str,
            cache_record_id=record.record_id,
            provider_name=record.provider_name,
            symbol=record.symbol,
            status=StaleFreshStatus.UNKNOWN_AGE,
            age_seconds=None, ttl_seconds=ttl, fresh=False, stale=True, expired=False,
            readable=policy.allow_stale_read, refresh_required_future=True,
            risk_flags=[ProviderCacheRiskFlag.CACHE_RECORD_STALE],
            warnings=["No fetched_at timestamp. Assuming stale."], errors=[], metadata={}
        )

    try:
        fetched_time = datetime.fromisoformat(record.fetched_at_utc)
        age = (now - fetched_time).total_seconds()

        status = StaleFreshStatus.FRESH
        fresh = True
        stale = False
        expired = False

        if age > ttl:
            status = StaleFreshStatus.STALE
            fresh = False
            stale = True

        readable = True
        warnings = []
        if stale and policy.stale_read_requires_warning:
            warnings.append("Stale read detected.")
        if stale and policy.block_expired and age > (ttl * 2): # arbitrary expiration logic
            expired = True
            status = StaleFreshStatus.EXPIRED
            readable = False
            warnings.append("Record expired and blocked.")

        risk_flags = []
        if stale:
            risk_flags.append(ProviderCacheRiskFlag.CACHE_RECORD_STALE)

        return StaleFreshEvaluation(
            evaluation_id=create_stale_fresh_evaluation_id(),
            created_at_utc=now_str,
            cache_record_id=record.record_id,
            provider_name=record.provider_name,
            symbol=record.symbol,
            status=status, age_seconds=int(age), ttl_seconds=ttl,
            fresh=fresh, stale=stale, expired=expired, readable=readable,
            refresh_required_future=stale, risk_flags=risk_flags,
            warnings=warnings, errors=[], metadata={}
        )
    except ValueError:
        return StaleFreshEvaluation(
            evaluation_id=create_stale_fresh_evaluation_id(), created_at_utc=now_str, cache_record_id=record.record_id, provider_name=record.provider_name, symbol=record.symbol,
            status=StaleFreshStatus.INVALID_TIMESTAMP, age_seconds=None, ttl_seconds=ttl, fresh=False, stale=True, expired=False, readable=False, refresh_required_future=True, risk_flags=[], warnings=["Invalid timestamp format."], errors=[], metadata={}
        )

def evaluate_cache_index_stale_fresh(index: ProviderCacheIndex, policy: StaleFreshPolicy | None = None) -> list[StaleFreshEvaluation]:
    if not policy:
        policy = build_default_stale_fresh_policy()
    return [evaluate_cache_record_stale_fresh(r, policy) for r in index.records]

def stale_fresh_evaluation_summary(items: list[StaleFreshEvaluation]) -> dict[str, Any]:
    return {"total": len(items), "stale": sum(1 for i in items if i.stale)}

def stale_fresh_evaluation_to_text(item: StaleFreshEvaluation) -> str:
    return f"Eval {item.evaluation_id} - {item.symbol} - {item.status.value}"
