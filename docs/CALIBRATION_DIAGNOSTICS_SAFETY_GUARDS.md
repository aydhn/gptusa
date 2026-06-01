# Calibration Diagnostics Safety Guards

Ensures Phase 141 remains strictly within offline research bounds.

## Restrictions
- No trade signal.
- No strategy activation.
- No deployment.
- No order decision.
- No portfolio weights.
- No investment advice.
- No broker connectivity.
- No paper state mutation.
- No Telegram real send.
- No scraping or HTML parsing.
- No dashboard.
- No paid API usage.
- No network fetch default enabled.
- No live inference.
- No online inference.
- **No calibration fitting.**
- **No calibrated model creation.**
- **No threshold optimization.**
- No heavy ML dependencies (e.g. pytorch, sklearn, xgboost).
- No daemon/scheduler.
- No execution language (e.g. 'buy', 'sell', 'guaranteed profit').
