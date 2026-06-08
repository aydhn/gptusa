# Phase 153: Portfolio Construction Foundation

Phase 153 establishes the Portfolio Construction Foundation, Position Sizing Boundary, and Risk Budgeting Contract.
It read-only ingests the Phase 152 backtest closure handoff package.
It does NOT perform actual portfolio construction, sizing, or allocation.
It prepares deterministic position sizing prototypes for Phase 154.

## CLI Usage
- `python -m usa_signal_bot portfolio-foundation-info`
- `python -m usa_signal_bot portfolio-load-handoff --write`
- `python -m usa_signal_bot build-candidate-universe-contract --write`
- `python -m usa_signal_bot build-risk-budget-contract --write`
- `python -m usa_signal_bot portfolio-foundation-review --write`
