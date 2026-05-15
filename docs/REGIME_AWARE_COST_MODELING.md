# Regime-Aware Cost Modeling

This documentation explains the purpose of Regime-Aware Cost Modeling in the USA Signal Bot.

Fixed slippage or execution costs are unrealistic because execution quality heavily depends on prevailing market conditions. A highly volatile or illiquid market significantly widens spreads and increases slippage compared to a calm, liquid session.

To address this, we define multiple cost regimes:
- **Volatility Regime:** Ranges from `VERY_LOW` to `EXTREME` based on ATR and gap sizes.
- **Liquidity Regime:** Ranges from `DEEP` to `FROZEN` based on average dollar volume and trading status.
- **Spread Regime:** Ranges from `TIGHT` to `UNRELIABLE` based on observed spread bps.
- **Session Regime:** Identifies `REGULAR`, `PREMARKET`, `AFTER_HOURS`, or `CLOSED`.
- **Lifecycle Regime:** Identifies `NORMAL`, `CORPORATE_ACTION_WATCH`, `DELISTING_RISK`, etc.

These individual regimes combine into a `CombinedCostRegime` (e.g., `NORMAL`, `STRESSED`, `HIGH_RISK`, `BLOCKED`).

You can explore these regimes using the CLI:
```bash
python -m usa_signal_bot regime-cost-info
python -m usa_signal_bot combined-cost-regime --symbol SPY --atr-pct 2 --adv 10000000 --spread-bps 50
```
