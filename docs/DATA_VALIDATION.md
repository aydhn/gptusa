# Data Validation

Data quality is the most crucial part of any trading signal generator. Before any analysis occurs, USA Signal Bot enforces strict validation rules on the downloaded OHLCV data.

## Why is OHLCV Validation Necessary?
Providers can return bad data due to splits, glitches, zero-volume days, or network timeouts. Generating signals on bad data is dangerous. Our validation layer ensures consistency before data reaches the cache.

## Validation Rules

1. **Required Fields**:
   - Every bar must have a symbol and a timestamp.
2. **Price Consistency**:
   - `open`, `high`, `low`, `close` must be strictly positive (> 0).
   - `high` must be $\ge$ `low`.
   - `high` must be $\ge$ `open` and `close`.
   - `low` must be $\le$ `open` and `close`.
3. **Volume**:
   - `volume` cannot be negative.
   - Zero volume is allowed by default but flagged as a warning.
4. **Duplicate Bars**:
   - Multiple bars with the exact same symbol, timeframe, and timestamp will produce an ERROR.
5. **Missing Symbols**:
   - If a requested symbol returns absolutely no data, it generates an ERROR.
6. **Timestamp Sequence**:
   - Bars belonging to the same symbol should be in strictly increasing chronological order.

## Severity Levels
- **INFO**: Minor notifications.
- **WARNING**: The data is suspicious but theoretically possible (e.g., zero volume on a halt day). Warnings can be tolerated depending on config.
- **ERROR / CRITICAL**: The data is mathematically or logically invalid (e.g., negative price). Such data must be repaired or dropped.

## CLI Usage

To validate the most recent cache file:
```bash
python -m usa_signal_bot data-cache-validate
```

To validate a specific cache file:
```bash
python -m usa_signal_bot data-cache-validate --cache-file my_cache.jsonl
```

To view the recent validation and anomaly reports generated during downloads:
```bash
python -m usa_signal_bot data-validation-report
```
