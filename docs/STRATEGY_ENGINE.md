# Strategy Engine Foundation

The Strategy Engine is responsible for running trading strategies over feature sets to generate trading signal candidates.

## Architecture
- **StrategyRegistry**: Holds registered strategies.
- **StrategyInputBatch**: The contract for feeding feature rows to a strategy.
- **StrategyRunResult**: The summary and output signals of a strategy run.
- **StrategyEngine**: The core runner that validates input, executes strategies, and stores results.

## Skeleton Strategies
Phase 21 includes skeleton strategies for testing and interface validation:
- `trend_following_skeleton`
- `mean_reversion_skeleton`
- `momentum_skeleton`
- `volatility_breakout_skeleton`

**IMPORTANT**: These are candidate generators ONLY. They do not execute trades, and there is no backtesting or paper trading integration yet.

## CLI Usage
List strategies:
```bash
python -m usa_signal_bot strategy-list
```

Get strategy info:
```bash
python -m usa_signal_bot strategy-info --name trend_following_skeleton
```

Run strategy from feature store:
```bash
python -m usa_signal_bot strategy-run-feature-store --strategy trend_following_skeleton --symbols AAPL --write
```
