# Phase 129: Regime Transition Analytics

Phase 129 focuses on regime transition matrix, persistence analytics, and stability diagnostics. It consumes Phase 128 labeled regime artifacts via a read-only ingestion process and generates metadata representing market behavior.

## Scope
- Generates transition matrices (count, probability, dominant transition, entropy).
- Generates persistence analytics (average run length, persistence ratio).
- Evaluates stability and churn using deterministic diagnostics.
- Includes strict safety validations prohibiting execution language, secret leakage, or live trading commands.
- It is NOT an activation boundary.
- Model training, model prediction, and live trading are EXPLICITLY FORBIDDEN.

## CLI Commands
- `python -m usa_signal_bot regime-transition-info`
- `python -m usa_signal_bot regime-transition-matrix --write`
- `python -m usa_signal_bot regime-transition-review --write`
