# Promotion Review

## Overview
Evaluates the eligibility of a candidate for promotion to a local research release candidate.

## Scoring
Scores the candidate based on completeness of evidence, lack of risk regressions, and positive performance improvements.

## Manual Review
Flags may enforce a strict requirement for manual review before promotion is permitted.

## CLI
```bash
python -m usa_signal_bot eligibility-score --write
python -m usa_signal_bot risk-regression-review --write
python -m usa_signal_bot decision-board-review --mode conservative --write
```
