# Baseline Model Family Registry

## Overview
Defines acceptable baseline models (e.g., heuristics, moving averages, placeholders for tree/linear models).

## Allowed Families
- `DUMMY_BASELINE`
- `PERSISTENCE_BASELINE`
- `MOVING_AVERAGE_BASELINE`
- `LINEAR_MODEL_PLACEHOLDER`
- `TREE_MODEL_PLACEHOLDER`

## Safety
- Heavy dependencies (e.g., `sklearn`, `xgboost`, `torch`) are restricted, and the registry enforces that model implementations are deferred to Phase 139.
- This registry is **NOT** a trained model registry. It strictly catalogs definitions.
