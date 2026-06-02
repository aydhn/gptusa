# Phase 146: Realistic Backtest Foundation

Phase 146 sets up the data contracts, safety boundaries, and transaction cost/slippage models for the backtesting engine.

It explicitly does **NOT** run full backtests. It does **NOT** run live trading. It only creates a foundation to ensure subsequent phases (Phase 147) can execute backtests deterministically and safely.

## CLI Commands
- `python -m usa_signal_bot backtest-foundation-info`
- `python -m usa_signal_bot build-backtest-dataset-contract --write`
- `python -m usa_signal_bot build-transaction-cost-model --write`
- `python -m usa_signal_bot build-market-simulation-contract --write`
- `python -m usa_signal_bot backtest-foundation-review --write`
