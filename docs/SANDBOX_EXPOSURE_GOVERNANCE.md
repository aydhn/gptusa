# Sandbox Exposure Governance

Exposure metadata bounds the maximum weights, group weights, and normalized sandbox allocations.

## Core Rules
- Output records contain `sandbox_optimizer_weight` only.
- `actual_target_weight`, `actual_portfolio_weight`, `actual_allocation`, and `actual_position_size` must explicitly equal `None`.
- Not valid for actual market positioning.
