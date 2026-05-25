# Cache-Aware Fetch Dry-Run

The data provider runtime implements a strict dry-run engine that does not perform actual network fetches by default.
Instead, it:
1. Builds a stable `ProviderCacheKey`.
2. Performs a `ProviderCacheLookupResult` check.
3. If the cache hits, it simulates fetching rows (`rows_available`).
4. If it misses, it skips the actual fetch to prevent unwanted execution.

This is a preparation step for Phase 108.
