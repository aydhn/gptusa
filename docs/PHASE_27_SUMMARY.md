# Phase 27: Benchmark Comparison & Performance Attribution

Phase 27 introduces essential research analytics tools, enabling the comparison of strategy backtest results against market benchmarks and decomposing performance across multiple dimensions.

## Key Features Implemented

1. **Benchmark Models & Sets:**
   - Defined core models (`BenchmarkSpec`, `BenchmarkSet`) to represent benchmarks (ETF, INDEX_PROXY, CASH).
   - Created predefined sets like `default` (SPY, QQQ, IWM, CASH) and `broad_market`.

2. **Benchmark Loader (Cache-Only):**
   - Implemented `benchmark_loader.py` to securely load OHLCV data from the local cache without executing live web/broker requests, adhering to the project's strict local execution constraints.

3. **Buy-and-Hold & Cash Baselines:**
   - Designed a simple baseline engine that buys at the first available open and holds until the final close.
   - Designed a `CASH` baseline generator that produces a flat equity curve.

4. **Benchmark Comparison Engine:**
   - Synchronizes strategy equity curves with benchmark equity curves on matching timestamps.
   - Calculates relative performance metrics including **Excess Return**, **Relative Drawdown**, and proxy approximations like **Correlation-like**, **Beta-like**, **Tracking-Error-like**, and **Information-Ratio-like**.

5. **Performance Attribution:**
   - Decomposes trade ledger PnL by multiple dimensions: `STRATEGY`, `SYMBOL`, `TIMEFRAME`, `ACTION`, `MONTH`, `YEAR`, and `HOLDING_PERIOD`.
   - Calculates win rate, net PnL, average PnL, and contribution percentage for each group.

6. **Storage & Integration:**
   - Integrated comparison and attribution logic seamlessly into the `BacktestEngine`, allowing reports to be automatically generated during a run (controlled via `config/default.yaml`).
   - `benchmark_store.py` manages writing JSON artifacts locally.

7. **CLI Expansions:**
   - New commands: `benchmark-info`, `benchmark-cache-check`, `buy-and-hold-baseline`, `backtest-benchmark-compare`, `backtest-attribution`, `benchmark-summary`.

## Not Implemented (Future Phases)
- Walk-forward analysis
- Monte Carlo simulations
- Strategy Optimizer or ML models
- Paper trading / Live broker connections

## Technical Adherence
- All data loaded locally. No requests are made.
- Strict typing and pure Python/Pandas logic.
- Backward compatibility maintained for existing features.
