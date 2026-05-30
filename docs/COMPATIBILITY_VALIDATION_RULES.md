# Compatibility Validation Rules

The compatibility validation rules ensure that artifacts outputted from Phase 131 accurately describe the regime overlays without generating dangerous actions.

## Assessed Rules
1. `COMPATIBILITY_SCORE_RANGE_VALID`: Evaluates 0-100 unnormalized and 0.0-1.0 normalized thresholds.
2. `OVERLAY_SCORE_RANGE_VALID`: Evaluates 0-100 unnormalized and 0.0-1.0 normalized thresholds.
3. `LOW_COMPATIBILITY_EXPLAINED`: Ensures low compatibility context results have corresponding explanations.
4. `NO_SIGNAL_OUTPUT`: Asserts that `produces_trade_signal` is blocked.
5. `NO_EXECUTION_OUTPUT`: Asserts that `produces_order_decision` is blocked.
