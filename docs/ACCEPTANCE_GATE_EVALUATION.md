# Acceptance Gate Evaluation

## Purpose
Provides preliminary evaluation of constraints required for a strategy candidate to be considered viable.

## Supported Gates
1. **Min Sample Size:** Minimum trade occurrences needed for statistical significance.
2. **OOS Improvement:** Requires the candidate walk-forward pass ratio to improve.
3. **Cost Robustness:** Requires the candidate to exceed specific robustness score limits against simulated slippage/costs.
4. **Drawdown:** Hard percentage limits on maximum drawdown.

## Critical Disclaimer
A gate `PASS` is purely an advisory, preliminary check. It does **not** equal a live trading approval.

## CLI Examples
```bash
python -m usa_signal_bot evaluate-gates --write
```
