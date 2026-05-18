# Local Research Run Registry

## Purpose
Manages the local database of `ResearchRun` execution histories. This includes artifacts, configuration snapshots, metrics, and comparisons.

## Core Models
- `ResearchRunStatus`: (CREATED, READY, RUNNING, COMPLETED, FAILED...)
- `ExperimentArtifactType`: (CONFIG_SNAPSHOT, RUN_CONTEXT, BACKTEST_RESULT...)

## Limitations
- Operates entirely locally.
- Does not depend on external databases.
- Does not export telemetry to platforms like Datadog or Prometheus.

## CLI Examples
```bash
python -m usa_signal_bot mock-experiment-run --run-type baseline --write
python -m usa_signal_bot run-registry --write
python -m usa_signal_bot research-execution-summary
```
