# CALIBRATION_RESIDUAL_LABEL_REGIME_DRIFT

## Metrics
- **Calibration Drift:** Measures the shift in Expected Calibration Error (ECE) and Brier Score.
- **Residual Drift:** Tracks the mean and standard deviation shift of the prediction residuals.
- **Label Distribution Drift:** Analyzes the distribution changes in the true labels.
- **Regime Drift:** Analyzes the ratio shifts in market regimes between the reference and monitoring windows.

These metrics provide offline diagnostics regarding the robustness of the ML ensemble under changing market conditions. They do not trigger threshold optimizations or active regime switching in the trading engine.
