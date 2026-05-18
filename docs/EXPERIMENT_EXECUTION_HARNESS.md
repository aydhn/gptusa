# Experiment Execution Harness

## Purpose
The `LocalExperimentHarness` orchestrates the local execution of an `ExperimentPlan` using either mock, backtest, or walk-forward runners. It compares the behavior of a baseline configuration snapshot against a candidate overlay.

## Principles
1. **Local Analytics:** The harness operates strictly offline.
2. **No Config Mutation:** `allow_config_mutation` is forced to `False`. The original `default.yaml` or any production configuration file is never written.
3. **No Order Routing:** `allow_order_routing` is forced to `False`.

## CLI Examples
```bash
python -m usa_signal_bot research-execution-info
python -m usa_signal_bot experiment-harness-run --mode mock_only --write
```
