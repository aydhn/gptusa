# Regime-Aware Backtest and Paper Analytics

The regime-aware cost model integrates directly into simulation environments:
- **Backtesting:** Appends trade-level metadata (`cost_regime`, `adjusted_cost_bps`). Summarizes the distribution of trades across regimes.
- **Walk-Forward:** Tracks regime cost distribution per out-of-sample window, detecting stability shifts.
- **Basket Simulation:** Monitors portfolio concentration in high-risk or illiquid regimes.
- **Paper Trading:** Implements pessimistic fill adaptations by adjusting fill prices with the scaled `adjusted_cost_bps`.
- **Signal & Candidate Selection:** Applies rank penalties to candidates originating from `HIGH_RISK` regimes and suppresses those in `BLOCKED` regimes.

CLI Example:
```bash
python -m usa_signal_bot regime-cost-review --write
```
