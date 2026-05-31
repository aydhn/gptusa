# Phase 137: ML Dataset Assembly

This phase focuses on creating the datasets needed for ML experiments in a safe, repeatable, and non-executing manner.

## Key Concepts
- ML foundation ingestion from Phase 136
- Dataset source resolution
- Feature, target, and label matrix assembly
- Dataset manifest generation
- Train/Validation/Test Split Policy design
- Split Assignment
- Leakage Audit
- Dataset Quality and Split Quality evaluation
- Readiness Gate

## Important Limitations
- This phase DOES NOT train any models.
- This phase DOES NOT predict outcomes.
- This phase DOES NOT activate strategies or deployments.
- Everything is local and research-only. No live network, no broker API.

## CLI Usage
`python -m usa_signal_bot ml-dataset-assembly-info`
`python -m usa_signal_bot assemble-feature-matrix --write`
`python -m usa_signal_bot run-ml-leakage-audit --write`
`python -m usa_signal_bot ml-dataset-assembly-review --write`
