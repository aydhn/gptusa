# Phase 116 Feature Factor Engine Foundation

This document outlines the foundation of the advanced indicators, features, and factor engine in the `usa_signal_bot`.
It handles the metadata, schema validation, safety guarantees, and input/output contracts.

Phase 116 acts strictly as the "foundation" stage and produces **no actual indicator computations**. It solely prepares the configuration and enforces rules so that Phase 117 can safely implement technical calculations over local data.

**Important Principles of Phase 116:**
- **No live trading**: The system generates schemas and plans, not trade signals.
- **No activation**: Features are metadata, not live strategies.
- **No external connections**: All schemas are defined offline without network dependencies.
- **No mutations**: Paper states and actual trading portfolios remain completely untouched.

## Structure
- `kickoff_gate_ingestion.py`: Ingests outputs from Phase 115 safely.
- `indicator_registry.py`, `feature_registry.py`, `factor_registry.py`: Provide structural blueprints.
- `feature_schema.py`: Validate outputs against blocked fields like signals.
- `feature_transform_pipeline.py`: A skeleton pipeline that simulates computations using dry-runs.

## CLI Usage
Check feature registry:
```bash
python -m usa_signal_bot feature-registry
```

View the overall foundation full review metadata report:
```bash
python -m usa_signal_bot feature-foundation-review --write
```
