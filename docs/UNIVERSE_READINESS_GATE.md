# Universe Readiness Gate

The readiness gate acts as a strict checkpoint between data acquisition and feature engineering.

## Purpose
It prevents symbols with missing, sparse, or invalid data from reaching the strategy layers, ensuring high-quality signals.

## Evaluation
- **Primary Timeframe:** Every symbol must have its primary timeframe ready.
- **Score:** A symbol's readiness score reflects the ratio of its ready timeframes.
- **Status:** Symbols are marked as `ELIGIBLE`, `PARTIAL`, or `INELIGIBLE`.
- **Gate Status:** The entire universe run evaluates to `PASSED`, `PARTIAL`, or `FAILED` based on the configured ratio of eligible vs failed symbols.

## Future Usage
In subsequent phases, the feature engine will consume *only* the `eligible_symbols` list produced by the readiness gate.

## Commands
- `python -m usa_signal_bot active-universe-readiness --latest-run`
- `python -m usa_signal_bot active-universe-eligible --latest-run --format txt`
