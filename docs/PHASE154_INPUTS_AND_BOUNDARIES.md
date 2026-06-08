# Phase 154 Inputs and Boundaries

## Inputs
- **Portfolio Foundation Review**: Contains the final state from Phase 153.
- **Candidate Universe Contract**: Sets which candidates can even enter prototyping.
- **Constraint Catalog & Risk Budget Contract**: Determines overall limitations.
- **Position Sizing Boundary**: Expected boundary settings.
- **Candidate Metrics**: Offline dataset containing `volatility_proxy`, `cost_proxy`, `drawdown_proxy`, etc.
- **Risk Budget Inputs**: Initial budget limits per strategy.

## Boundaries
Inputs are treated as strictly **read-only**. Any detected forbidden fields like `target_weight`, `allocation`, `actual_position_size`, or `capital_allocation` during input resolution will immediately trigger a blocked state and set `ready_for_phase155=False`.
