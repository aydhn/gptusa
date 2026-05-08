# Live Signal Drift Analysis

## Overview
This subsystem analyzes how signals and candidates change ("drift") between the moment they were originally generated and when they are later replayed or re-scanned historically.

## Concepts
- **Signal Snapshot**: The exact state of a signal (symbol, timeframe, score, features) at creation time `created_at_utc`.
- **Replay Snapshot**: The state of the signal generated during a historical backtest or later scan for the same timeframe.

## Drift Metrics
- **Score/Confidence/Rank Drift**: Absolute difference between the original and replay values.
- **Feature Drift**: The average percentage difference of normalized numeric features.
- **Changed Action**: If the direction (buy vs sell) flips, this triggers a `SEVERE_DRIFT`.
- **Missing Signal**: Signal existed originally but vanished in replay.

## Status
- `NO_DRIFT`, `LOW_DRIFT`, `MODERATE_DRIFT`, `HIGH_DRIFT`, `SEVERE_DRIFT`.

## CLI Example
```bash
python -m usa_signal_bot signal-drift-report --original-signal-file data/signals/original.jsonl --replay-signal-file data/signals/replay.jsonl --write
```

## Important Disclaimer
Drift analysis is an engineering tool for pipeline stability. It is **NOT** investment advice and does not guarantee trade profitability.
