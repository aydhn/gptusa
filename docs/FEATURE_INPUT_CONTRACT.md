# Feature Input Contract

The Feature Engine enforces a strict boundary between market data and feature computation.

## What is the Input Contract?

The Feature Engine does not perform HTTP requests or scrape data. It only accepts validated market data in the form of `FeatureBatchInput` and `FeatureInput` objects. This separation of concerns ensures that the data going into the indicators has already passed the strict Readiness Gate (Phase 12).

## OHLCV to Feature Input

When `build_feature_inputs_from_cache` is called, the system:
1. Scans the local JSONL market data cache.
2. Filters out any missing or partial symbols according to the `eligible_symbols` parameter (derived from the Readiness Gate).
3. Packages the OHLCV bars into `FeatureInput` structures grouped by symbol and timeframe.

## Eligible Symbols and Readiness Gate

Feature computation is intentionally expensive. To avoid wasting compute cycles or generating noise, the engine should only process symbols that have passed the Active Universe Readiness Gate. Symbols that lack sufficient historical data or fail basic quality checks are ignored at the input boundary.

## Validation

If a `FeatureInput` has fewer than the required `min_bars` for a requested indicator, it is marked invalid and dropped from the batch.
