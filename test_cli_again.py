import sys
import os

from usa_signal_bot.app.cli import (
    handle_cost_robustness_info,
    handle_cost_stress_scenarios,
    handle_slippage_stress,
    handle_spread_stress,
    handle_sensitivity_matrix
)

# Mock context
class MockContext:
    pass

ctx = MockContext()
print("\n--- INFO ---")
handle_cost_robustness_info(ctx)
print("\n--- SCENARIOS ---")
handle_cost_stress_scenarios(ctx)
print("\n--- SLIPPAGE ---")
handle_slippage_stress(ctx, 10.0)
print("\n--- SPREAD ---")
handle_spread_stress(ctx, 5.0)
print("\n--- SENSITIVITY ---")
handle_sensitivity_matrix(ctx, False)
