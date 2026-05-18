# Baseline vs Candidate Comparison

## Purpose
Calculates execution deltas across critical metrics (e.g. `total_net_pnl_usd`, `max_drawdown_pct`, `walk_forward_pass_ratio`) to evaluate if the candidate proposal improved performance.

## Higher/Lower Better Logic
- **Higher Better**: PnL, win rate, robustness score, pass ratio.
- **Lower Better**: Drawdown, cost drag, turnover, latency.

## Warning
A `CANDIDATE_BETTER` outcome strictly indicates a local metadata improvement within historical sample bounds. It **does not guarantee future performance** and is not investment advice.

## CLI Examples
```bash
python -m usa_signal_bot compare-runs --write
python -m usa_signal_bot comparison-report --write
```
