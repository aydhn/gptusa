# Read-Only Parallel Monitoring

The Read-Only Parallel Monitoring system (`parallel_monitor.py`) tracks the candidate strategy in real-time alongside the active paper portfolio without interfering with it.

## Overview
It achieves this by capturing a read-only snapshot of the active paper state and passing it to the candidate's locked observer runtime. The candidate then generates `ObserverOutput` items, which are subsequently compared against the paper snapshot.

## Drift Detection
The `drift_detector.py` identifies discrepancies (drift) between the candidate's actions and the baseline:
*   `SIGNAL_COUNT_DRIFT`
*   `PROPOSAL_COUNT_DRIFT`
*   `RISK_STATUS_DRIFT`
*   `SAFETY_FLAG_DRIFT`

## Output Monitoring
The monitoring analyzer counts and validates:
*   `SIGNAL_MIRROR` outputs
*   `PROPOSAL_MIRROR` outputs
*   `RISK_MIRROR` outputs
*   `NOTIFICATION_PREVIEW` outputs

*Note: The parallel monitoring generates purely local metadata. It does not use external APM telemetry tools (e.g., Datadog, Prometheus).*

## CLI Usage
Run a mock read-only parallel monitoring session:
```bash
python -m usa_signal_bot observer-parallel-monitor --write
```

Detect drift on mock outputs:
```bash
python -m usa_signal_bot observer-drift-detect --write
```
