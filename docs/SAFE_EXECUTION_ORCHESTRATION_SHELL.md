# Safe Execution Orchestration Shell

The Safe Execution Orchestration Shell is responsible for taking the validated Runtime Service Graph and generating an orchestration plan.

## Design
The shell produces a `SafeOrchestrationPlan` that details the required order to initialize and run services. Crucially, the shell operates strictly in dry-run mode.

## Constraints
- **Dry-Run Only:** The shell never starts real runtime instances.
- **Safety Validated:** The output of the shell (`OrchestrationDryRunResult`) asserts that no network, broker, or paper-state mutations occurred during the validation pass.

## CLI Usage
- `python -m usa_signal_bot orchestration-plan --write`
- `python -m usa_signal_bot orchestration-dry-run --write`
- `python -m usa_signal_bot orchestration-safety-check`
