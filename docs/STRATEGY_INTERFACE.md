# Strategy Interface

The `Strategy` abstract class is the contract for all signal generation algorithms.

## Required Components
- `metadata`: A `StrategyMetadata` object defining the name, version, category, and required features.
- `parameter_schema`: Defines the tunable parameters.
- `generate_signals`: The core method that takes a `StrategyInputBatch` and returns a list of `StrategySignal` objects.

## Guardrails
- Strategies must call `self.assert_no_execution()` inside `generate_signals`.
- Strategies should not initiate any broker requests.
- Output actions are purely candidates (e.g., `SignalAction.WATCH`).
