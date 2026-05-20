# Bridge Telemetry

## Purpose
Bridge Telemetry is a strictly local system that records metadata about dry-run bridge operations. It does not integrate with external telemetry systems like Prometheus, Datadog, or Grafana. It ensures that any attempt by a candidate to run forbidden operations is caught, recorded, and summarized.

## Telemetry Events
Events are recorded whenever an action is allowed or denied. For example:
- **session_started**: Logged when a session is initiated.
- **blocked_operation_attempted**: Logged when forbidden actions (e.g., real broker order, state mutation) are attempted.

## CLI Usage
```bash
python -m usa_signal_bot dry-run-operation-monitor --operation send_paper_order
python -m usa_signal_bot bridge-telemetry-report --write
```
