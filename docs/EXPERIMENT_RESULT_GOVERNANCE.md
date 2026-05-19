# Experiment Result Governance

## Overview
This phase introduces a robust governance layer for evaluating experiment results. It is strictly local research metadata and does not trigger live or demo broker actions.

## Evidence Pack
Bundles baseline, candidate, metrics, gates, and deltas into a verifiable payload.

## Gate Aggregation
Aggregates quality, sample size, and performance gates to determine research validity.

## Risk Flags
Flags such as leakage, cost regression, turnover regression, and walk-forward instability trigger warnings or rejections.

## CLI
```bash
python -m usa_signal_bot governance-info
python -m usa_signal_bot evidence-pack --write
python -m usa_signal_bot governance-review --write
```
