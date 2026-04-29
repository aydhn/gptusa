# Cache Refresh Planner

USA Signal Bot stores OHLCV data locally in JSONL files to prevent unnecessary API calls and to allow fully offline operation. The cache refresh system decides when those files need to be re-downloaded.

## Cache Freshness (TTL)

A cache file is considered "fresh" if its age (time since last modification) is less than the configured Time-To-Live (TTL) in seconds.
By default, the TTL is `86400` seconds (24 hours).

## Decision Logic

For every symbol requested, the planner assigns a `CacheDecision`:

1. **USE_CACHE**: The cache file exists and its age is < TTL. No network request needed.
2. **CACHE_MISSING**: No cache file exists for this request. Network download required.
3. **CACHE_STALE**: The cache file exists but its age is > TTL. Network download required.
4. **REFRESH_CACHE**: A forced refresh was requested. Network download required.
5. **BYPASS_CACHE**: The user explicitly disabled cache reading. Network download required.

## CLI Usage

To view a dry-run plan of what would be downloaded vs. loaded from cache:
```bash
python -m usa_signal_bot data-refresh-plan --symbols AAPL,MSFT --timeframe 1d
```

To execute the plan (this will actually download data for stale/missing items):
```bash
python -m usa_signal_bot data-refresh-execute --symbols AAPL,MSFT --timeframe 1d
```

To force download everything, ignoring TTL:
```bash
python -m usa_signal_bot data-refresh-execute --symbols AAPL,MSFT --timeframe 1d --force
```
