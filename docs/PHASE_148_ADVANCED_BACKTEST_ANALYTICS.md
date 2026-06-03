# PHASE 148 — USA SIGNAL BOT / ADVANCED BACKTEST PERFORMANCE ANALYTICS

## Overview
Phase 148 is the offline advanced backtest analytics, trade diagnostics, and run validation phase.
It operates strictly by read-only ingestion of Phase 147 `BacktestRunFullReview` outputs.

## Restrictions
- This phase is **not** live trading, paper trading, or broker integration.
- This phase does **not** involve deployment, Telegram real sends, or actual execution.
- This phase does **not** run benchmark comparison, walk-forward, stress testing, or Monte-Carlo (these are Phase 149+).

## Usage
- `python -m usa_signal_bot backtest-analytics-info`
- `python -m usa_signal_bot build-return-series --write`
- `python -m usa_signal_bot calculate-advanced-performance-metrics --write`
- `python -m usa_signal_bot reconcile-backtest-ledger --write`
- `python -m usa_signal_bot backtest-analytics-review --write`
