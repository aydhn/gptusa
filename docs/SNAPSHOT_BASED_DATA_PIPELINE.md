# Snapshot-Based Data Pipeline

This pipeline ensures robust and predictable data acquisition by utilizing the Active Universe Snapshot.

## Why Snapshot-Based?
Relying on a static snapshot prevents mid-run universe mutations and ensures all downstream processes (coverage, readiness, feature engineering) evaluate the exact same symbols.

## Workflow
1. **Resolution:** Active snapshot is loaded.
2. **Multi-Timeframe Request:** Build data requests (e.g., 1d, 1h, 15m) for the symbols.
3. **Cache/Refresh:** Download new data or retrieve from cache.
4. **Validation/Repair:** Inspect downloaded data for anomalies and repair.
5. **Coverage/Readiness:** Generate data coverage and readiness reports.
6. **Readiness Gate:** Final filter to separate eligible from ineligible symbols.

## Batch Processing
For large universes, the symbols are chunked into smaller batches to respect API limits, avoid timeouts, and allow safe interruption/resumption.

## Commands
- `python -m usa_signal_bot active-universe-plan --timeframes 1d,1h --limit 50`
- `python -m usa_signal_bot active-universe-download --timeframes 1d,1h --limit 50`
