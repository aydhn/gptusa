# Execution Realism Gap

## Overview
The execution realism gap attempts to quantify how realistic the historical backtest execution assumptions were compared to the paper run (forward simulation).

## Metrics Analyzed
- **Fill Price Gap**: Difference between paper fill price and backtest fill price.
- **Timing Gap**: The number of bars delayed between paper entry/exit and backtest entry/exit.
- **PnL Gap**: Net difference in PnL for matched trades.
- **Fee/Slippage Gap**: Differences in simulated cost assumptions.
- **Missing Fill/Trade**: `PAPER_ONLY` or `BACKTEST_ONLY` occurrences.

## Execution Realism Score & Bucket
The engine generates a 0-100 score:
- Penalizes unmatched trades.
- Penalizes wide price gaps.
- Penalizes timing delays.

Buckets: `HIGH_REALISM`, `ACCEPTABLE_REALISM`, `MODERATE_GAP`, `LARGE_GAP`, `SEVERE_GAP`.

## CLI Example
```bash
python -m usa_signal_bot execution-gap-report --latest-comparison
```

## Important Disclaimer
This score does **NOT** validate actual broker fills. It measures the divergence between two *simulations*. It is not a guarantee of live execution realism.
