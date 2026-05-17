# Hypothesis Tracker

The Hypothesis Tracker formally translates items in the Strategy Repair Queue into testable assumptions.

## Features
- **Null Condition**: Explicitly defines the failure metric indicating an unsuccessful experiment.
- **Success/Failure Criteria**: Associates expected qualitative outcomes (e.g., OOS Improvement > 0) with a hypothesis.
- **Confidence Rating**: Ranks hypothesis viability based on evidence strength and historical sample size. Hypotheses with low data points are tagged as `INSUFFICIENT_EVIDENCE`.

## Example CLI Usage
```bash
python -m usa_signal_bot hypothesis-create --write
python -m usa_signal_bot hypothesis-review --write
```
