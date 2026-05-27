# Phase 120: Factor Composition

Phase 120 is the fifth phase of the feature/factor engine band (Phase 116-125). It builds on the outputs of Phase 119's feature enrichment pipeline.

## Core Operations
- Ingests the `FeatureEnrichmentFullReview` output from Phase 119 as read-only.
- Profiles columns in enriched feature tables into feature groups based on a rule engine.
- Assembles candidate factors (Momentum, Trend, etc.) using `factor_component_registry` and `factor_candidate_registry`.
- Evaluates feature metadata (coverage, missingness, stability, redundancy) via dedicated analyzers.
- Determines `FeatureSelectionMetadata` statuses strictly for research use.
- Evaluates the `FactorReadinessGate` to guarantee that local candidates and metadata are ready for Phase 121 scoring.

## Limitations
- This phase is **NOT** a strategy activation.
- It is **NOT** a signal generation engine.
- Broker executions, orders, and paper state mutations are strictly blocked.
- Trade signals and portfolio weights are NOT computed.

## Example CLI Usage
- `python -m usa_signal_bot factor-composition-info`
- `python -m usa_signal_bot factor-composition-review --write`
- `python -m usa_signal_bot factor-readiness-gate --write`
