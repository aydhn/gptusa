# Signal Contract

The `StrategySignal` defines the standard output from a strategy run.

## Properties
- `signal_id`: Deterministic hash.
- `action`: E.g., LONG, SHORT, FLAT, WATCH, AVOID.
- `confidence`: Float [0, 1].
- `score`: Float [0, 100].
- `reasons`: List of strings explaining the signal.
- `feature_snapshot`: State of the indicators at the time of generation.

## Validations
- Duplicate IDs are rejected.
- Overconfidence (too many signals >0.8) triggers warnings.
- Missing required fields triggers errors.

**Note**: Signals are NOT execution orders.
