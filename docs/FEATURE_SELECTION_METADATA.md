# Feature Selection Metadata

Feature Selection Metadata bridges the gap between raw features and analytical factors. It is entirely non-execution metadata.

## Selection Dimensions
1. **Coverage Ratio**: Evaluates proportion of non-null records for a feature.
2. **Missingness Ratio**: Reciprocal of coverage ratio, evaluates dropouts.
3. **Stability Score**: Uses a deterministic heuristic for value variance and categorical distribution stability.
4. **Redundancy Score**: Derived from high correlation pairs against other numerical features.
5. **Confidence / Freshness / Lineage**: Preserved from upstream lineage tracking.

## Status & Reason
- Produces statuses like `SELECTED_FOR_RESEARCH`, `WATCHLIST`, or exclusion blocks (e.g., `EXCLUDED_LOW_COVERAGE`).
- It produces a reason code mapping, e.g., `GOOD_COVERAGE`, `UNSAFE_NAME`.

## Disclaimer
This is for research feature selection only. It is **NOT** signal generation or strategy selection.
