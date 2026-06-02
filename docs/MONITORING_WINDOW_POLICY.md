# MONITORING_WINDOW_POLICY

## Policy Definition
The `MonitoringWindowPolicy` defines the temporal and structural boundaries for calculating drift baselines.

### Components
- **Reference Window:** Typically maps to `train` and `validation` splits.
- **Monitoring Window:** Typically maps to the `test` split or a simulated offline out-of-sample window.

## Safety Flags
The policy strictly enforces:
- `live_monitoring_enabled = False`
- `scheduler_enabled = False`
- `daemon_started = False`

The rolling and calendar window features are strictly metadata labels for research and do not initialize scheduled background workers.
