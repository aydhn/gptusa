# Volatility and Liquidity Cost Curves

Multipliers are derived for each dimension:
- **Volatility Multiplier:** Base = 1.0. Extreme volatility can scale up to 2.5x.
- **Liquidity Multiplier:** Base = 1.0. Illiquid conditions scale up to 3.0x.
- **Spread Multiplier:** Scales up to 3.5x for unreliable spreads.
- **Session & Lifecycle Multipliers:** Penalize off-hours trading or corporate action risk.

A **Cost Curve Profile** is selected based on the combined regime:
- `LIQUID` (deep liquidity, low vol)
- `BASELINE` (normal conditions)
- `CONSERVATIVE` (thin liquidity or missing data)
- `STRESSED` (high vol, thin liquidity)
- `EXTREME` / `BLOCKED` (severe conditions)

CLI Tools:
```bash
python -m usa_signal_bot volatility-cost-regime --atr-pct 5
python -m usa_signal_bot liquidity-cost-regime --adv 2000000
python -m usa_signal_bot cost-curve-select --symbol SPY --atr-pct 5 --adv 2000000 --spread-bps 150
```
