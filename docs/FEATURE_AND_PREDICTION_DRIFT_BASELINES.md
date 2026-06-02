# FEATURE_AND_PREDICTION_DRIFT_BASELINES

## Calculation
- **Feature Drift:** Calculates the statistical shift (mean, std dev, overlap) between the reference and monitoring feature matrices.
- **Prediction Drift:** Computes the shift in the predicted outputs of the ensemble prototype.

## Constraints
Drift baselines are pure research diagnostics. They are explicitly disconnected from strategy activation logic and do not emit trade signals, portfolio weights, or order decisions.
