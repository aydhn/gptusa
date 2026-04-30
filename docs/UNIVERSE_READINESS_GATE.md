# Universe Readiness Gate

## What is the Universe Readiness Gate?
The Universe Readiness Gate is the final checkpoint before market data is allowed to pass to the Feature Engine. It takes the output of the Data Readiness module and makes a binary (Eligible/Ineligible) decision for every symbol in the universe.

## Eligible vs. Ineligible Symbols
- **Eligible**: The symbol has sufficient data quality, density, and contains the required primary timeframe.
- **Ineligible**: The symbol is missing too much data, failed validation, or is entirely missing the primary timeframe.
- **Partial**: The symbol has the primary timeframe but is missing some intraday confirmation timeframes (allowed if configured).

## Primary Timeframe Requirement
A core rule of the gate is that every symbol **must** have valid data for the configured `required_primary_timeframe` (usually `1d`). If the daily data fails, the intraday data is considered useless for the core strategy.

## Score Logic
Symbols receive a readiness score from 0.0 to 100.0 based on how many of the requested timeframes successfully passed data validation. The gate configuration defines a `min_symbol_score` (default 70.0).

## Gate Statuses
The entire universe run receives a final gate status:
- `PASSED`: The required ratio of symbols were deemed Eligible.
- `PARTIAL`: Failed to meet the ideal ratio, but enough eligible symbols exist to continue cautiously.
- `FAILED`: Too many symbols failed validation; the pipeline stops.
- `NOT_EVALUATED`: Gate was bypassed or disabled.

## The Future: Feature Engine
In Phase 13, the Feature Engine will explicitly ignore the raw universe and instead load `data/universe/readiness/eligible_symbols.csv` as its starting point.

## CLI Examples

View the readiness gate report for the latest run:
```bash
python -m usa_signal_bot active-universe-readiness --latest-run
```

Export the list of eligible symbols:
```bash
python -m usa_signal_bot active-universe-eligible --latest-run --format txt
```
