# Factor Readiness Gate

The Factor Readiness Gate verifies that all Phase 120 conditions are satisfied and safe for passing to Phase 121 (Factor Scoring & Normalization).

## Core Rules
- **Feature Tables Available**: Ensures upstream artifacts load correctly.
- **Factor Candidates Valid**: Ensures no unsafe elements exist in the component specification.
- **Coverage/Missingness/Stability/Redundancy Acceptable**: Ensures metadata quality blocks have functioned correctly.
- **No Execution Output**: Strictly guarantees the absence of execution fields (`produces_trade_signal`, `produces_order_decision`, `produces_portfolio_weights`).

## Gate Outcome
The Readiness Gate outputs `ready_for_phase121`. It is strictly blocked from allowing `activation_allowed` or `strategy_activation_allowed`.
