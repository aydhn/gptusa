# Provider Quality Module (Phase 109)

This module implements strictly offline, metadata-only data quality scoring, source trust profiling, and provider ranking. It explicitly prohibits trade signal generation, broker order execution, and network fetching.

## Scorer Components
- `completeness_scorer`: Rates dataset fill rate.
- `freshness_scorer`: Rates staleness of the cache.
- `schema_validity_scorer`: Checks schema compliance.
- `continuity_scorer`: Detects timestamp gaps.
- `source_disagreement_scorer`: Compares divergence across sources.
- `outlier_penalty_scorer`: Punishes basic OHLCV errors.
- `cache_reliability_scorer`: Values stable caches.
- `provider_safety_compliance_scorer`: Blocks execution/mutating behavior.

## Core Models
- `ProviderDataQualityScore`
- `SourceTrustProfile`
- `ProviderSelectionScore`
- `ProviderRanking`

## Validation & Safety
The `selection_safety_validator.py` and `score_calibration_guard.py` rigorously enforce constraints that scoring never yields trade or broker directives.
