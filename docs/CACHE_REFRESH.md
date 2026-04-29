# Cache Refresh System

## What is Cache Freshness?
Cache freshness evaluates whether a locally stored market data file is recent enough to be used for research without querying the upstream provider. A cache file is considered "fresh" if its modification age is less than the configured Time-To-Live (TTL).

## TTL Logic and Age
TTL is configured via `CacheRefreshConfig.default_ttl_seconds`.
Different assets and timeframes can theoretically demand different freshness standards:
- **Daily Timeframes:** A max cache age of several days (e.g., 3 days, over a weekend) might be acceptable.
- **Intraday Timeframes:** Intraday data becomes stale much faster (e.g., within 1 day or hours).

## CacheDecision Enums
The Cache Refresh Planner assigns a decision to every symbol based on its cache status:
- `USE_CACHE`: Valid, existing, and fresh file found.
- `CACHE_MISSING`: File does not exist; refresh required.
- `CACHE_STALE`: File exists but is older than TTL; refresh required.
- `REFRESH_CACHE`: Manual override via force flag.
- `BYPASS_CACHE`: User requested to bypass cache entirely.
- `CACHE_INVALID`: Future expansion for when quality checks deem a cache file unreadable.

## Refresh Planner and Executor
1. **Refresh Plan:** Analyzes requests against local cache files and returns a `CacheRefreshPlan` detailing exactly which symbols are fresh and which must be fetched over the network.
2. **Refresh Execute:** Takes a plan, spins up the `MarketDataDownloader`, and pulls only the missing or stale symbols, caching them seamlessly upon successful download and repair.

## CLI Examples

Plan a cache refresh without executing network calls:
```bash
python -m usa_signal_bot data-refresh-plan --symbols AAPL,MSFT --timeframe 1d
```

Execute a refresh (forcing it regardless of cache age):
```bash
python -m usa_signal_bot data-refresh-execute --symbols AAPL,MSFT --timeframe 1d --force
```
