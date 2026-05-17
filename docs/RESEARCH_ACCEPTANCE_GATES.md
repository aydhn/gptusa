# Research Acceptance Gates

Acceptance Gates enforce statistical, qualitative, and leakage safeguards before an experiment can be deemed "supported."

## Implemented Gates
1. **Minimum Sample Size Guard**: Restricts confidence on low-evidence tests.
2. **Out-of-Sample (OOS) Improvement**: Ensures candidates perform better than baselines on holdout data.
3. **Walk-Forward Stability**: Verifies performance persists across rolling time windows.
4. **Cost Robustness**: Caps maximum theoretical degradation via slippage testing.
5. **Drawdown Reduction**: Prevents candidates from worsening maximum drawdown curves.
6. **No-Leakage / No-Overfit Guards**: Validates isolation of training versus testing bounds.
7. **Manual Review Required**: Strict boolean barrier ensuring a human reads the final report.

## Example CLI Usage
```bash
python -m usa_signal_bot acceptance-gates --experiment-type parameter_change --scope single_strategy
python -m usa_signal_bot sample-size-guard --sample-size 10 --min-required 30
python -m usa_signal_bot leakage-overfit-guard
```
