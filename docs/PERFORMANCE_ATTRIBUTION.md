# Performance Attribution

## Overview
The Performance Attribution system isolates the Gross and Net PnL of historical backtests and local paper trading runs across multiple dimensions. It operates strictly as a local heuristics layer and produces metadata designed to help identify the sources of performance.

## Gross vs Net PnL
Attribution models capture both Gross PnL (pre-cost) and Net PnL (post-cost). Discrepancies between the two highlight strategy components that may be overly fragile to execution costs.

## Dimensions
Performance attribution can be calculated across the following dimensions:
- `symbol`: Highlights top and worst contributing instruments.
- `strategy`: Highlights performance differences between deployed strategies.
- `sector` / `cluster`: Aggregates performance by higher-level asset classifications.
- `regime`: Shows how performance varies across different identified market regimes (e.g. BULL, BEAR, HIGH_VOL).

## Quality Metrics
The system provides a `win_rate` and `avg_net_pnl_usd` for each dimension to evaluate robustness. Groups with low sample sizes will trigger warnings, and their quality rating will fall to `WEAK` or `NOISY`.

## CLI Usage
```bash
python -m usa_signal_bot attribution-info
python -m usa_signal_bot pnl-attribution --dimension symbol
python -m usa_signal_bot strategy-attribution
```
