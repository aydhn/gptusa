import os
from pathlib import Path
import csv
import hashlib
from datetime import datetime, timezone
from typing import Any, List, Dict
from usa_signal_bot.core.exceptions import CacheStoreError
from usa_signal_bot.provider_cache.phase108_models import (
    ProviderCacheRecord,
    create_provider_cache_record_id,
    ProviderCacheRecordStatus,
    ProviderCacheRiskFlag
)
import uuid

def write_provider_cache_csv(path: Path, records: list[dict[str, Any]], overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise CacheStoreError(f"Cache file {path} already exists and overwrite is False.")

    os.makedirs(path.parent, exist_ok=True)

    if not records:
        # Write empty file
        with open(path, 'w', newline='') as f:
            pass
        return path

    fieldnames = list(records[0].keys())
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    return path

def read_provider_cache_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records = []
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

def cache_file_checksum(path: Path) -> str | None:
    if not path.exists():
        return None
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def validate_cache_records_schema(records: list[dict[str, Any]]) -> list[str]:
    if not records:
        return ["Empty records"]

    first = records[0]
    expected_cols = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in expected_cols if c not in first]
    if missing:
        return [f"Missing expected columns: {missing}"]
    return []

def build_cache_record_from_path(path: Path, provider_name: str, symbol: str, capability: str, interval: str | None = None) -> ProviderCacheRecord:
    now_str = datetime.now(timezone.utc).isoformat()
    if not path.exists():
        return ProviderCacheRecord(
            record_id=create_provider_cache_record_id(),
            created_at_utc=now_str,
            provider_name=provider_name,
            symbol=symbol,
            capability=capability,
            interval=interval,
            cache_key=path.stem,
            cache_path=str(path),
            status=ProviderCacheRecordStatus.MISSING,
            rows=0, first_timestamp=None, last_timestamp=None,
            fetched_at_utc=None, as_of_utc=now_str, stale_after_seconds=None,
            file_size_bytes=None, schema_valid=False, checksum=None,
            quality_flags=[], risk_flags=[ProviderCacheRiskFlag.CACHE_RECORD_MISSING],
            warnings=["File missing."], errors=[], metadata={}
        )

    try:
        records = read_provider_cache_csv(path)
        stat = path.stat()

        schema_errors = validate_cache_records_schema(records)
        schema_valid = len(schema_errors) == 0

        first_ts = records[0].get("timestamp") if records else None
        last_ts = records[-1].get("timestamp") if records else None
        # Assume fetched_at is file modification time for now
        fetched_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()

        status = ProviderCacheRecordStatus.VALIDATED if schema_valid and len(records) > 0 else ProviderCacheRecordStatus.EMPTY
        if len(records) == 0:
            status = ProviderCacheRecordStatus.EMPTY
        if not schema_valid and len(records) > 0:
            status = ProviderCacheRecordStatus.CORRUPT

        risk_flags = []
        if status == ProviderCacheRecordStatus.CORRUPT:
            risk_flags.append(ProviderCacheRiskFlag.CACHE_RECORD_CORRUPT)

        return ProviderCacheRecord(
            record_id=create_provider_cache_record_id(),
            created_at_utc=now_str,
            provider_name=provider_name,
            symbol=symbol,
            capability=capability,
            interval=interval,
            cache_key=path.stem,
            cache_path=str(path),
            status=status,
            rows=len(records),
            first_timestamp=first_ts,
            last_timestamp=last_ts,
            fetched_at_utc=fetched_at,
            as_of_utc=now_str,
            stale_after_seconds=None, # Filled by policy
            file_size_bytes=stat.st_size,
            schema_valid=schema_valid,
            checksum=cache_file_checksum(path),
            quality_flags=[],
            risk_flags=risk_flags,
            warnings=schema_errors,
            errors=[],
            metadata={"mtime": stat.st_mtime}
        )
    except Exception as e:
        return ProviderCacheRecord(
            record_id=create_provider_cache_record_id(),
            created_at_utc=now_str, provider_name=provider_name, symbol=symbol,
            capability=capability, interval=interval, cache_key=path.stem, cache_path=str(path),
            status=ProviderCacheRecordStatus.CORRUPT,
            rows=0, first_timestamp=None, last_timestamp=None, fetched_at_utc=None, as_of_utc=now_str,
            stale_after_seconds=None, file_size_bytes=None, schema_valid=False, checksum=None,
            quality_flags=[], risk_flags=[ProviderCacheRiskFlag.CACHE_RECORD_CORRUPT],
            warnings=[f"Error reading cache file: {str(e)}"], errors=[str(e)], metadata={}
        )

def cache_store_summary(path: Path) -> dict[str, Any]:
    return {"path": str(path), "exists": path.exists()}
