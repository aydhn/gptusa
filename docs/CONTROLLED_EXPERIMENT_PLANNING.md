# Controlled Experiment Planning

The Controlled Experiment Planner sets up structured environments to test hypotheses without altering live/paper runtime logic.

## Features
- **Baseline vs. Candidate**: Defines historical references (baseline) versus proposed changes (candidate) for safe local comparisons.
- **Rollback Plan Generation**: Forces the definition of rollback steps before an experiment is even queued.
- **Validation Constraints**: Generates holdout, out-of-sample, and walk-forward validation specifications that an experiment must eventually fulfill to pass gates.

## Example CLI Usage
```bash
python -m usa_signal_bot experiment-plan --write
python -m usa_signal_bot validation-plan --scope single_strategy --experiment-type parameter_change
```
