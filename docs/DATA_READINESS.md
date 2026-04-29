# Data Readiness Checkpoint

Data Readiness is a strict checkpoint mechanism that ensures market data meets minimum quality and coverage standards before it can be used by subsequent layers (Feature Engine, Strategy, Backtesting).

## Concept

A readiness score is computed based on data coverage across required timeframes for the active universe.

## Readiness Statuses

- **READY**: Coverage meets or exceeds the required threshold.
- **PARTIAL**: Coverage is below the strict threshold but acceptable under relaxed criteria (e.g., allowed partial intraday data).
- **NOT_READY**: Coverage falls below acceptable thresholds, or the primary timeframe is missing.
- **FAILED**: A critical error occurred during the readiness check.

## Rules

- **Primary Timeframe**: Usually strictly required. If missing, the status is `NOT_READY`.
- **Coverage Ratio**: A score (0-100) representing how many expected bars were found.

## Importance

Passing the readiness checkpoint is a hard requirement. If data is `NOT_READY`, the feature engine will not execute, preventing garbage-in-garbage-out scenarios in strategy generation and backtesting.

## CLI Usage

```bash
# Check readiness from cache without downloading new data
python -m usa_signal_bot data-readiness-check --symbols AAPL,MSFT --timeframes 1d,1h --from-cache

# View the latest coverage report
python -m usa_signal_bot data-coverage-report
```
