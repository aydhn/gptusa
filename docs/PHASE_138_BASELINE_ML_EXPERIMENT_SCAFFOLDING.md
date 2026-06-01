# Phase 138: Baseline ML Experiment Scaffolding

## Overview
Phase 138 introduces the baseline ML experiment scaffolding and non-activation evaluation harness. It ingests the `MLDatasetAssemblyFullReview` output from Phase 137 in read-only mode to establish the baseline configuration and rules required for model evaluation.

## Key Concepts
- **Non-Activation**: This phase does **NOT** train models, execute predictions, create broker orders, or mutate paper state.
- **Scaffolding Only**: This phase merely builds the schema and safety boundary for models. The actual artifact generation and offline training are deferred to Phase 139.

## CLI Usage
```bash
python -m usa_signal_bot baseline-ml-scaffolding-info
python -m usa_signal_bot build-baseline-experiment-specs --write
python -m usa_signal_bot build-evaluation-harness-contract --write
python -m usa_signal_bot baseline-scaffolding-review --write
```
