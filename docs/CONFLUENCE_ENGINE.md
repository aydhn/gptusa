# Confluence Engine

## Overview
The Confluence Engine is designed to group and analyze multiple strategy signals within a given context. The main objective is to detect directional alignment or conflicting signals to assist with filtering down high-quality trade opportunities.

## Aggregation Modes
Signals can be grouped based on one of the following `SignalAggregationMode` types:
- **BY_SYMBOL_TIMEFRAME:** Evaluate signals matching the same symbol and timeframe (default).
- **BY_SYMBOL:** Group solely by symbol, disregarding the timeframe.
- **BY_STRATEGY:** Group entirely by strategy name.
- **GLOBAL:** Group all signals into one bucket.

## Bias / Direction
The confluence output establishes a directional bias (`LONG_BIAS`, `SHORT_BIAS`, `FLAT_BIAS`, `WATCH_BIAS`, `MIXED`, or `CONFLICTED`) depending on the count of signals voting in a particular direction.
If both LONG and SHORT actions are present in the same group, it will be immediately flagged as `CONFLICTED`.

## Confluence Score
The confluence score is heavily dependent on the number of signals perfectly aligning their actions and their corresponding confidences. An aggregated score ranges from 0 to 100, which subsequently drives a qualitative `ConfluenceStrength` label (e.g. `WEAK`, `MODERATE`, `STRONG`, `VERY_STRONG`).

**Note:** The output is solely an analytical directional bias representation. It does not replace a backtested trade execution plan.

## CLI Usage Example

```bash
# Group signals and output confluence
python -m usa_signal_bot signal-confluence --file data/signals/example_signals.jsonl --mode by_symbol_timeframe --write

# Run multiple strategies and view the final confluence group
python -m usa_signal_bot strategy-run-confluence --strategies trend_following_skeleton,momentum_skeleton --symbols AAPL,MSFT --timeframes 1d
```
