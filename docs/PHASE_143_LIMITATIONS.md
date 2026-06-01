# Phase 143 Limitations

- This phase is NOT active trading.
- It is NOT a strategy or signal engine.
- No live inference, no online inference, no deployment.
- No broker APIs, no paper orders, no paper state mutation.
- No Telegram real send, no scraping, no HTML parsing.
- No dashboards, no paid APIs.
- No real network requests made during test execution.
- No heavy ML frameworks (sklearn/torch/xgboost/lightgbm) are added as hard dependencies.
- Offline ensemble predictions are not trade signals.
- Blend coefficients are not portfolio allocations.
- The Ensemble Registry is not a deployment registry.

Phase 144 will follow to handle model drift, monitoring baselines, and post-ensemble governance.
