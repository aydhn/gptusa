# Phase 126: Regime Classification Foundation

Phase 126 is the foundational phase for regime classification and market behavior. It establishes the input bundles, output contracts, dataset schemas, taxonomies, and safety boundaries.

## Goals
- Read-only ingest of Phase 125 `FinalClosureFullReview`.
- Build the `RegimeResearchInputBundle` from frozen artifacts.
- Define the `MarketStateDatasetContract` and skeleton dataset structure.
- Define the `RegimeLabelTaxonomy`.
- Establish a rigorous `RegimeNonActivationBoundaryResult` to guarantee no execution.

## Limitations
- This phase is **NOT** an active paper trading phase.
- It does **NOT** build the signal engine or perform strategy activation.
- It does **NOT** run any broker integrations.
- It produces pure research metadata (`regime_research_only`).

## CLI Commands
- `python -m usa_signal_bot regime-foundation-info`
- `python -m usa_signal_bot regime-label-taxonomy --write`
- `python -m usa_signal_bot regime-foundation-review --write`
