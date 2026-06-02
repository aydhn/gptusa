# Simulated Execution

Simulates fills based on rules.
Guarantees `real_order_created=False`, `broker_execution_used=False`, `paper_state_mutated=False`.
Missing prices generate NO_FILL events.
