# Data Validation

## Why OHLCV Validation is Necessary
Financial market data often suffers from anomalies such as missing fields, invalid prices (e.g., high < low), extreme outliers, or non-monotonic timestamps. This validation layer ensures that only structurally and logically sound data is allowed into the system, preventing corrupted inputs from poisoning technical indicators, signals, and backtest evaluations.

## Validation Rule List
1. **Required Fields:** Ensures open, high, low, close, and volume are present and prices are positive (>0).
2. **Price Consistency:** Verifies that high >= low, high >= open, high >= close, low <= open, and low <= close.
3. **Volume Validity:** Flags negative volumes as errors. Zero volumes can optionally trigger warnings (based on `DataQualityConfig.allow_zero_volume`).
4. **Timestamp Validity:** Ensures timestamps are not empty.
5. **Symbol Validity:** Ensures the symbol is not empty and matches expected requested symbols.
6. **Sequence (Monotonicity):** Warns if bars for a symbol are not in chronological order.
7. **Duplicate Bars:** Detects multiple bars for the same symbol at the exact same timestamp/timeframe.
8. **Missing Symbols:** Flags if an expected symbol returns no data.
9. **Empty Dataset:** Rejects totally empty responses with a critical error.

## Severity Levels
- **INFO:** Passed checks and routine observations.
- **WARNING:** Non-critical issues (e.g., zero volume, sequence issues, unexpected symbols) that don't immediately break the data logic.
- **ERROR:** Structural or logical failures (e.g., high < low, missing symbols, negative prices) that require intervention or bar dropping.
- **CRITICAL:** System-breaking issues, such as entirely empty datasets.

## Future Expansions
Validation rules will be expanded in later phases to cover statistical outlier detection (e.g., impossible daily returns) and suspicious market gaps (e.g., unexplained 90% drops between adjacent bars).

## CLI Examples

To validate an existing cache file:
```bash
python -m usa_signal_bot data-cache-validate --cache-file yfinance_AAPL_1d_start_end.jsonl
```

To view the latest validation and anomaly reports generated during downloads:
```bash
python -m usa_signal_bot data-validation-report --latest
```
