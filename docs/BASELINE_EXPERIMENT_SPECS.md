# Baseline Experiment Specs

## Overview
Baseline Experiment Specs dictate the scope and methodology for training and evaluating baseline ML models in offline contexts.

## Kinds
- `CLASSIFICATION_BASELINE`
- `REGRESSION_BASELINE`
- `REGIME_CONTEXT_BASELINE`
- `VOLATILITY_BASELINE`
- `DRAWDOWN_BASELINE`
- `NAIVE_BENCHMARK_BASELINE`

## Rules
- Model training and prediction are deferred to Phase 139 (`training_deferred_to_phase139=True`, `prediction_deferred_to_phase139=True`).
- Specs do not produce trade signals or portfolio activations.
