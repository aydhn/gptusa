# Signal Scoring

## Overview
Signal Scoring evaluates raw `StrategySignal`s to quantify their quality, assign risk penalties, and map them to a standardized confidence bucket. The scoring engine evaluates a variety of elements such as feature snapshots, reasons length, baseline strategy config score, and assigned risk flags.

## Score Details
- **Range:** 0 to 100.
- **Confidence Calibration:** Maps the score directly to a `0.0 - 1.0` confidence scale.
- **Backtest Max Bound:** Without a backtest system, any generated signal will be capped to a maximum configurable score (e.g. 70.0 by default) to prevent overconfidence. This score is not a trade execution value, it's used strictly for review and filtering.

## Reason Quality
Signals are given a reason quality ratio (0.0 to 1.0) depending on the number of unique reasons provided (up to 4 reasons maxes out the ratio). This ratio multiplies the `reason_quality_weight` configuration parameter.

## Feature Snapshot
A signal's underlying feature snapshot length (the number of indicators captured at creation time) also scales a feature snapshot ratio, multiplying the `feature_snapshot_weight`. Empty feature snapshots score zero.

## Risk Penalties
If a signal has assigned `SignalRiskFlag` items (e.g., `INSUFFICIENT_FEATURES`), a penalty proportional to the number of risk flags is deducted from the final score.

## CLI Usage Example

```bash
# Read raw signal output and score them, and output a new scored report
python -m usa_signal_bot signal-score-file --file data/signals/example_signals.jsonl --write
```
