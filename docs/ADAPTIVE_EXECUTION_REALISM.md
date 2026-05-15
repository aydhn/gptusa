# Adaptive Execution Realism

Adaptive Execution Realism translates regime risk into simulation decisions. Rather than blindly applying high costs, the engine can block fill simulations or suppress signals entirely.

- **Baseline / Conservative / Stressed:** Modifies the baseline cost estimate with the derived regime multiplier.
- **Require Review:** Flags the operation as `HIGH_RISK`, requiring manual review in production scenarios.
- **Block Fill / Block Signal:** During closed sessions or frozen liquidity, fill simulations and signal propagation are blocked entirely.

Important: A `PASS` from this system is **not** a live trading approval. This is an operational heuristic for local backtesting.

CLI Example:
```bash
python -m usa_signal_bot adaptive-execution-decision --symbol SPY --atr-pct 8 --adv 1000000 --spread-bps 250
```
