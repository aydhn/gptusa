# POST_ENSEMBLE_GOVERNANCE

## Rules
The Post-Ensemble Governance layer validates that the monitoring package complies with the non-activation boundaries:
- `ENSEMBLE_REGISTRY_VALID`
- `DRIFT_INPUTS_VALID`
- `NO_LIVE_MONITORING`
- `NO_ALERT_SENDER`
- `NO_SCHEDULER`
- `NO_SIGNAL_OUTPUT`
- `NO_ORDER_OUTPUT`
- `NO_DEPLOYMENT`

Passing this governance check is a strict prerequisite for producing the `PHASE145_READY` flag.
