# Stress Inputs and Boundaries

## Inputs
- `WalkForwardFullReview` from Phase 150.
- `Strategy Return Series`
- `Strategy Equity Curve`
- `Fold Replay Results`

## Boundaries
- Input references are rigorously checked for forbidden execution columns (e.g., `broker_order`, `portfolio_weight`).
- Inputs are treated as **read-only**.
