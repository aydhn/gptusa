# Backtest Engine Foundation

The USA Signal Bot includes a fully local backtest engine for historical signal replay and research. It is built as a deterministic, event-driven simulation environment designed strictly for paper-trading historical insights without external API dependencies.

## Design Goals
* **Local and Free**: Uses local data cache and standard Python libraries (pandas, pyarrow, etc).
* **Event-Driven Model**: Market bars and generated signals are merged into a chronologically sorted event stream.
* **Deterministic Replay**: All execution steps follow a fixed sequence based on timestamps, guaranteeing reproducible runs.
* **Strict Guardrails**: Prevents "same-bar" fills by default to mitigate lookahead bias by deferring orders to the `NEXT_OPEN`.

## Core Components
1. **Event Stream**: Merges market replay events and strategy signal events.
2. **Signal Adapter**: Converts a `StrategySignal` into a `BacktestOrderIntent` using configurable rules like minimum confidence and scoring.
3. **Simulated Fill**: Fills `BacktestOrderIntent`s at specified market prices (default `NEXT_OPEN`) while applying simulated slippage and fees.
4. **Position & Portfolio Model**: Tracks long positions (shorting is disabled by default in Phase 25), calculates unrealized/realized PnL, and produces `BacktestPortfolioSnapshot`s on every market bar.
5. **Equity Curve & Metrics**: Calculates drawdowns, win rate, total returns, and generates the final `BacktestRunResult`.

## Important Note
This engine **does not** produce real or paper orders for a live broker. It is strictly for historical research.

## CLI Usage
To view the foundation configuration:
```bash
python -m usa_signal_bot backtest-info
```

To run a backtest on generated signals:
```bash
python -m usa_signal_bot backtest-run-signals --signal-file data/signals/example.jsonl --symbols AAPL,MSFT --timeframe 1d --write
```
