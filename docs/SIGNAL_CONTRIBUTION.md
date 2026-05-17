# Signal Contribution

## Overview
The Signal Contribution system measures how specific signal families, strategies, and individual signal IDs contribute to overall performance.

## Status Classifications
Signals are classified based on their PnL contribution:
- **CONTRIBUTIVE:** Net positive PnL.
- **NEUTRAL:** Flat performance or zero net PnL.
- **COST_DEGRADED:** Positive Gross PnL but negative Net PnL due to slippage/fees.
- **DETRIMENTAL:** Negative Gross PnL and Net PnL.

## CLI Usage
```bash
python -m usa_signal_bot signal-contribution --write
```
