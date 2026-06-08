# Allocation Sandbox Safety Boundary

## Safety Boundary Constraints
Every run within Phase 155 is gated by the Safety Boundary Validation module.

The rule assertions explicitly verify the following conditions before establishing a 'Pass' state:
- Must only emit research allocation sandbox artifacts.
- Must verify that artifacts consumed are strictly read-only.
- Must guarantee no `actual_target_weights` are defined.
- Must guarantee no `actual_portfolio_weights` are defined.
- Must guarantee no `actual_allocation` amounts are set.
- Must guarantee no `actual_position_size` amounts are set.
- Must guarantee no `order_size` is computed.
- Must guarantee no capital deployments are configured.
- Must block actions associated with active portfolio optimizations.
- Must block rebalancing sequence execution.
- Must restrict access/deployment to Live and Paper modes.
- Must restrict Broker integration, networking layers, real order creation, paper state mutation, Telegram notification dispatches, and dashboard initializations.
