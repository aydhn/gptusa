# Portfolio Construction

This module takes sized candidates from the `allocation` module and processes them into a unified portfolio plan.

## Purpose
- Manages portfolio-level limits (gross, net, long, short exposure).
- Enforces concentration guards (symbol, strategy, sector, cluster).
- Balances candidates based on configurable weighting modes (e.g., EQUAL_WEIGHT, SCORE_WEIGHTED, HYBRID).

## Local Proxy Warning
**This system is entirely local.** It does NOT generate broker orders and should NOT be considered investment advice. The output is strictly local metadata representing a theoretical allocation.

## Example CLI Commands
```bash
python -m usa_signal_bot portfolio-construction-info
python -m usa_signal_bot portfolio-plan --equity 100000 --write
```
