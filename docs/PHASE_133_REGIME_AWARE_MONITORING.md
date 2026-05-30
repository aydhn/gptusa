# Phase 133: Regime-Aware Monitoring, Drift Tracking and Context Degradation Diagnostics

Phase 133 ingests Phase 132 context validation outputs to monitor regime-aware alignment drifts over time.
It explicitly acts as a read-only metadata validation layer.

## CLI Usage
```bash
python -m usa_signal_bot regime-monitoring-info
python -m usa_signal_bot track-regime-drift --write
python -m usa_signal_bot regime-monitoring-review --write
```
