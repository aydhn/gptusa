# Phase 141 Limitations

Phase 141 explicitly operates within defined limitations to guarantee safety and prevent unintended execution.

## Limitations
- **Not Active Trading:** Phase 141 does not perform any active trading.
- **Not a Strategy Engine:** Does not run live strategies or generate signals.
- **Not Live Inference:** Inference on live data is strictly prohibited.
- **No Calibration Fitting:** We evaluate calibration (diagnostics) but do NOT fit Platt scaling or Isotonic regression models here.
- **No Calibrated Models:** We do not save new "calibrated" model artifacts.
- **No Threshold Optimization:** We do not find optimal classification thresholds.
- **No Deployment:** Artifacts generated here are not for production deployment.
- **Dependency Restrictions:** Cannot use heavy ML frameworks (sklearn, torch, xgboost) or web scraping tools.
- **Environment:** Entirely offline, utilizing local fixtures and previously generated artifacts.

Phase 142 will prepare ensemble research scaffolding and calibration-aware governance.
