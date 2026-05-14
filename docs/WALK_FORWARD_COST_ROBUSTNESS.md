
# Walk-Forward Cost Robustness

## Purpose
Evaluates if the out-of-sample (OOS) windows of a walk-forward analysis survive cost stress.

## Logic
If more than a configurable percentage (e.g., 30%) of OOS windows become unprofitable under moderate stress, the strategy is marked as Fragile.

## CLI Commands
`python -m usa_signal_bot walk-forward-cost-robustness --write`
