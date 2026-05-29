# Phase 128: Deterministic/Heuristic Regime Labeling

Phase 128 establishes a research-metadata-only regime labeling layer, generating deterministic assignments, rolling windows, and validations. It ingests Phase 127 artifacts to produce final regime metadata without any execution semantics.

## Highlights
- **Deterministic / Heuristic Labeling**: Purely rule-based assignment.
- **Read-Only Ingestion**: Ingests Phase 127 results safely.
- **Safety**: Fully execution-free. No strategy activation, deployment, or actual ML training/prediction.

## CLI Commands
- `python -m usa_signal_bot regime-labeling-info`
- `python -m usa_signal_bot heuristic-regime-labels --write`
- `python -m usa_signal_bot regime-labeling-review --write`
