from typing import Any
from pathlib import Path
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    ProviderCacheIndex,
    ProviderCacheRecord,
    create_provider_cache_index_id,
    ProviderCacheRiskFlag,
    ProviderCacheRecordStatus
)
from usa_signal_bot.provider_cache.cache_store import build_cache_record_from_path
import os

def build_provider_cache_index(cache_root: Path) -> ProviderCacheIndex:
    # A real implementation would scan cache_root directories
    # Here we simulate an empty scan or a minimal scan
    records = []

    if cache_root.exists():
        for provider_dir in cache_root.iterdir():
            if not provider_dir.is_dir(): continue
            for symbol_dir in provider_dir.iterdir():
                if not symbol_dir.is_dir(): continue
                for file_path in symbol_dir.glob("*.csv"):
                    # Basic extraction from path: cache_root / provider / symbol / cache_key.csv
                    # In a real system, the capability/interval might be embedded in the cache_key or metadata
                    rec = build_cache_record_from_path(
                        path=file_path,
                        provider_name=provider_dir.name,
                        symbol=symbol_dir.name,
                        capability="GET_DAILY_OHLCV",
                        interval="1d"
                    )
                    records.append(rec)

    return build_provider_cache_index_from_records(cache_root, records)

def build_provider_cache_index_from_records(cache_root: Path, records: list[ProviderCacheRecord]) -> ProviderCacheIndex:
    stale_count = sum(1 for r in records if r.status == ProviderCacheRecordStatus.STALE)
    fresh_count = sum(1 for r in records if r.status in [ProviderCacheRecordStatus.FRESH, ProviderCacheRecordStatus.VALIDATED])
    missing_count = sum(1 for r in records if r.status == ProviderCacheRecordStatus.MISSING)
    corrupt_count = sum(1 for r in records if r.status == ProviderCacheRecordStatus.CORRUPT)

    return ProviderCacheIndex(
        index_id=create_provider_cache_index_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cache_root=str(cache_root),
        records=records,
        total_records=len(records),
        fresh_records=fresh_count,
        stale_records=stale_count,
        missing_records=missing_count,
        corrupt_records=corrupt_count,
        index_valid=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def filter_cache_records(index: ProviderCacheIndex, provider_name: str | None = None, symbol: str | None = None, capability: str | None = None) -> list[ProviderCacheRecord]:
    res = index.records
    if provider_name:
        res = [r for r in res if r.provider_name == provider_name]
    if symbol:
        res = [r for r in res if r.symbol == symbol]
    if capability:
        res = [r for r in res if r.capability == capability]
    return res

def validate_provider_cache_index(index: ProviderCacheIndex) -> list[str]:
    errors = []
    if not index.index_valid:
        errors.append("Index is explicitly invalid")
    for r in index.records:
        if ".." in r.cache_path:
            errors.append(f"Traversal in record {r.record_id}")
    return errors

def provider_cache_index_summary(index: ProviderCacheIndex) -> dict[str, Any]:
    return {
        "id": index.index_id,
        "total": index.total_records,
        "valid": index.index_valid
    }

def provider_cache_index_to_text(index: ProviderCacheIndex, limit: int = 200) -> str:
    return f"Cache Index {index.index_id} - Total: {index.total_records}"
