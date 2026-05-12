# Local Performance Baselines

The Local Performance Baselines framework constructs analytical summaries of expected pipeline execution costs purely sourced from historical local runs.

## Goal
To build predictable bounds for time and memory profiles preventing runaways and enforcing quality across scans and backtests without cloud integrations.

## Data Sources
It ingests execution metrics via isolated local caches:
- `data/profiling/runs`
- `data/regression/runs`
- `data/scheduler/runs`
- `data/taskqueue/runs`
- `data/quality/runs`

## Baseline Metrics
Calculated distributions:
- `mean_value`
- `median_value`
- `p75_value`
- `p90_value` (Core Benchmark Standard)
- `min_value`, `max_value`

## Constraints
- **NO EXTERNAL TELEMETRY**: Prometheus, Grafana, Datadog are prohibited.
- Local processing logic inherently depends on the deterministic compute capability of your active hardware environment.

## CLI Usage

View Configuration:
```bash
python -m usa_signal_bot performance-info
```

Generate Active Operational Baseline:
```bash
python -m usa_signal_bot performance-build-baseline --write
```

List Active Models:
```bash
python -m usa_signal_bot performance-baselines
```
