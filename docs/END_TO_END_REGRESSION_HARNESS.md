# End to End Regression Harness

## Overview
The End-to-End Regression Harness is designed to run the entire USA Signal Bot pipeline using deterministic 'Golden Fixtures'. This evaluates local pipeline stability and guards against unintended regressions in the feature, strategy, risk, or portfolio layers.

## Step Plans

Regression runs can be executed with different scopes:

- **smoke_only**: Runs only the core data loading and essential pipeline components to verify basic structural integrity.
- **golden_sample**: Runs all local steps, simulating the entire pipeline.
- **full_local_stack**: Runs all rehearsal steps and includes the Snapshot Comparison step.
- **quality_gate_only**: Only executes the final acceptance evaluators.

## Snapshot Comparison and Drift Detection
Each step produces a serialized snapshot. The harness compares the checksums of current step outputs against previously saved baseline snapshots. A mismatch indicates a "Drift", which can be flagged by `fail-on-drift` configuration.

## Critical Limitation
**A "PASS" result from the Regression Harness does NOT constitute an approval for live trading or investment advice.** The regression harness runs entirely on deterministic synthetic data without any live broker routing, network requests, or real risk constraints.

## CLI Examples

```bash
python -m usa_signal_bot regression-info
python -m usa_signal_bot regression-run-smoke
python -m usa_signal_bot regression-run --scope golden_sample --write
```
