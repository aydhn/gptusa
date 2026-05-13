# Universe Snapshot Workflow

## Overview
A `UniverseSnapshot` captures the exact membership of a universe at a specific point in time (`as_of_date`). This snapshot is vital for historical backtesting, as it ensures that the backtest engine uses the universe exactly as it looked on that day, preventing look-ahead bias.

## Snapshot Types
- `CURRENT`: The currently active universe definition.
- `HISTORICAL`: A freeze-frame of the universe from a past date.
- `BACKTEST_AS_OF`: An artificially generated snapshot reflecting the universe state at the start of a specific backtest.
- `MANUAL`: Generated manually by an operator.

## Generating and Diffing Snapshots
Snapshots are stored as JSON files. By creating snapshots periodically, you can track symbol additions and removals over time.

Diffing two snapshots helps identify ticker lifecycle events (like replacements due to acquisition).

## CLI Usage
Create a snapshot:
```bash
python -m usa_signal_bot universe-snapshot-create --write
```
Diff two snapshots:
```bash
python -m usa_signal_bot universe-snapshot-diff --old old.json --new new.json
```

## Limitations
Universe snapshots are only as accurate as the underlying manual registry and local cache. They do not provide official exchange-grade historical membership guarantees.
