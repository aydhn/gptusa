# Phase 140 - Baseline Model Comparison

Phase 140 is the fifth phase in the Advanced ML, ensemble, calibration, model drift, explainability, and governance band.

## Purpose
- Ingest Phase 139 BaselineTrainingFullReview read-only.
- Verify offline fitted model artifacts, prediction artifacts, evaluation reports, and non-activation model registries.
- Build baseline model comparison layer.
- Produce model ranking, metric aggregation, split-aware comparison, and regime-aware comparison metadata.
- Produce calibration preparation artifacts (no actual calibration fitting in this phase).
- Build selection governance layer.
- Produce candidate model shortlist (NOT for strategy activation, trade signals, or deployment).
- Prepare ground for Phase 141.

## Important Constraints
- **Not Active Paper Trading**
- **Not a Strategy/Signal Engine**
- **No Broker Integration**
- **No Real Paper Orders**
- **No Telegram Real Sends**
- **No Deployments**
- **No Live Inference**
- **No Calibration Fitting**

All outputs are `research_data_only`.

## CLI Commands
- `python -m usa_signal_bot model-comparison-info`
- `python -m usa_signal_bot normalize-model-metrics --write`
- `python -m usa_signal_bot build-model-ranking --write`
- `python -m usa_signal_bot build-calibration-preparation --write`
- `python -m usa_signal_bot model-comparison-review --write`
