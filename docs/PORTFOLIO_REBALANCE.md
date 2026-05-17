# Portfolio Rebalance Engine

## Purpose
The Portfolio Rebalance Engine calculates the necessary drift between the targeted portfolio allocations (from Phase 61) and the current local paper or backtest portfolio state.

## Rebalance Action Types
- `HOLD`: No drift above thresholds.
- `INCREASE`: Existing position needs to grow.
- `DECREASE`: Existing position needs to shrink.
- `ENTER`: Target exists but no current position.
- `EXIT`: Current position exists but no target.
- `REVIEW`/`SUPPRESS`/`BLOCK`: Action blocked due to cost, turnover, regime, or dust guards.

## Important Note
**Rebalance Plans are local metadata ONLY.**
They do NOT generate real broker orders and are NOT investment advice.

## CLI Usage
`python -m usa_signal_bot rebalance-info`
`python -m usa_signal_bot rebalance-plan --equity 100000 --write`
