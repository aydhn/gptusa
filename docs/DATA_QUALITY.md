# Data Quality Constraints

Raw data fetched from free providers is generally dirty or inconsistent. The project guarantees basic sanity through quality evaluations occurring concurrently with caching.

Because algorithmic components depend completely on historical inputs, rejecting bad rows reduces strategy corruption.

## Common Evaluated Issues
- **Negative Volume:** Volumes below zero flag errors.
- **Malformed Prices:** Any missing, blank, or less-than-zero prices.
- **Impossible Spreads:** Case when `high < low`.
- **Duplicates:** Symbols returned twice or duplicate timestamps.
- **Empty Return Sets:** Missing symbols requested from a target chunk.

## Error/Warning Disposition
Quality issues fall into warnings or errors. Critical malformed blocks fail strict validation entirely, leaving cleanly verified data for analysis. The cache summary report identifies anomalies for future investigation.
