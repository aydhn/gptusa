# Phase 109 - Provider Data Quality Scoring

## Overview
Phase 109 establishes the Data Quality Scoring layer for local research providers. It evaluates incoming data against 8 critical components (completeness, freshness, schema validity, continuity, source agreement, outlier profile, cache reliability, and safety compliance) to produce a composite `ProviderDataQualityScore`.

## Core Mechanics
- Reads outputs from Phase 108 `ProviderCacheFullReview`.
- Computes weighted score via the default configurable scoring policy.
- Strictly offline, leveraging local artifacts without generating real fetch requests.
- Scores are strictly for Research Data Use, not trading signals.

## Example CLI Usage
```bash
python -m usa_signal_bot provider-quality-info
python -m usa_signal_bot provider-data-quality-score
python -m usa_signal_bot provider-quality-review --write
```
