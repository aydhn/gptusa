# Sandbox Allocation Method Contracts

## Method Types Supported
1. **Equal Sandbox Allocation:** Assigns equal prototype weights.
2. **Sizing-Score Sandbox Allocation:** Assigns prototype weights proportionally using sizing scores.
3. **Risk-Budget Sandbox Allocation:** Allocates based on derived risk tolerance scores.
4. **Robustness Sandbox Allocation:** Distributes weights proportional to the normalized robustness metric.
5. **Composite Sandbox:** Creates blended prototype outputs.

## Critical Limitation
These methods *only* produce outputs explicitly marked as sandbox allocations. The `actual_target_weight` and `actual_allocation` flags must always be restricted.
