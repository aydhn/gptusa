
# Execution Sensitivity Matrix

## Purpose
Creates a multi-axis grid to find the exact thresholds where a strategy fails.

## Axes
- Slippage
- Spread
- Market Impact
- Fill Realism Mode

## Output
A matrix of cells showing Pass/Fail/Warn status based on net profitability.

## CLI Commands
`python -m usa_signal_bot sensitivity-matrix --write`
