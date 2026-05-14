# Dynamic Slippage Curves

Instead of fixed basis-point slippage, USA Signal Bot uses participation-based heuristic curves to dynamically model slippage for different order sizes.

## Multipliers
*   **Liquidity Multiplier**: Increases slippage on thin/illiquid names.
*   **Volatility Multiplier**: Increases slippage during high ATR or gaps.
*   **Spread Multiplier**: Increases slippage on wide spread names.

## CLI Usage

```bash
python -m usa_signal_bot slippage-curve
python -m usa_signal_bot slippage-estimate --participation 1.0
```
