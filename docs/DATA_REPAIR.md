# Data Repair Pipeline

When the validation layer detects blocking anomalies (ERROR or CRITICAL severities) in market data, the repair pipeline attempts to automatically fix the data so it can be safely used.

## Repair Philosophy

The repair process prioritizes data integrity. We would rather discard a bad bar than invent data or use logically impossible prices.

- **Never Silent**: Every repair action is logged and tracked in a `DataRepairReport`.
- **Drop over Guessing**: If price data is corrupt (e.g., negative prices, or high < low), the bar is dropped. We do not attempt to interpolate or guess prices.

## Automatic Actions

1. **Fill Missing Volume**: If a bar is valid but the volume field is `None`, it is replaced with `0.0`.
2. **Drop Duplicates**: If exact duplicate timestamps exist for a symbol, only the first encountered bar is kept. The rest are dropped.
3. **Drop Invalid Prices**: Bars with prices $\le 0$ or where `high < low` are removed entirely from the dataset.
4. **Chronological Sorting**: After repairs, all bars are re-sorted by symbol and timestamp to fix sequence anomalies.

## CLI Usage

To manually trigger a repair on a specific cache file:

```bash
python -m usa_signal_bot data-cache-repair --cache-file my_data.jsonl
```

By default, this writes a new file prefixed with `repaired_`.
To overwrite the original file (which automatically creates a `.bak` backup first):

```bash
python -m usa_signal_bot data-cache-repair --cache-file my_data.jsonl --overwrite
```
