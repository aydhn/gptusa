import pytest
from pathlib import Path
from usa_signal_bot.provider_cache.cache_store import write_provider_cache_csv, read_provider_cache_csv
from usa_signal_bot.provider_cache.phase108_models import *

def test_cache_store_read_write(tmp_path):
    p = tmp_path / "test.csv"
    data = [{"timestamp": "2024-01-01", "close": 150.0}]
    write_provider_cache_csv(p, data)
    assert p.exists()

    loaded = read_provider_cache_csv(p)
    assert len(loaded) == 1
    assert loaded[0]["close"] == "150.0"

def test_cache_safety_validator():
    from usa_signal_bot.provider_cache.cache_safety_validator import validate_cache_record_safety
    rec = ProviderCacheRecord(
        record_id="test", created_at_utc="", provider_name="", symbol="", capability="", interval="",
        cache_key="", cache_path="../test.csv", status=ProviderCacheRecordStatus.UNKNOWN, rows=0,
        first_timestamp=None, last_timestamp=None, fetched_at_utc=None, as_of_utc=None,
        stale_after_seconds=None, file_size_bytes=None, schema_valid=False, checksum=None,
        quality_flags=[], risk_flags=[], warnings=[], errors=[], metadata={}
    )
    errs = validate_cache_record_safety(rec)
    assert len(errs) > 0
    assert "Path traversal detected" in errs[0]

def test_no_network_in_fallback():
    from usa_signal_bot.provider_cache.fallback_dry_run_engine import ProviderFallbackDryRunEngine
    from usa_signal_bot.provider_cache.fallback_dry_run_plan import build_fallback_dry_run_plan

    plan = build_fallback_dry_run_plan("AAPL")
    engine = ProviderFallbackDryRunEngine(None, None)
    res = engine.run(plan)
    assert res.network_used == False
    assert res.broker_used == False
