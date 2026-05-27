# Feature Grouping

The Feature Group Registry groups parsed feature table columns into logical segments.

## Categories
Categories include:
- `PRICE_ACTION`
- `RETURNS`
- `VOLATILITY`
- `MOMENTUM`
- `TREND`
- `VOLUME_LIQUIDITY`
- `CROSS_SECTIONAL`
- `EVENT_CONTEXT`
- `QUALITY_CONTEXT`
- `CALENDAR_CONTEXT`
- `CONFIDENCE_FRESHNESS`
- `INTERACTIONS`
- `LINEAGE_CONTEXT`

## Group Profiles
The group profiler generates a `FeatureGroupProfile` reporting:
- `coverage_ratio`
- `average_missingness`
- `average_stability_score`
- `average_redundancy_score`

*Note: Group profiling is for categorizing analytical datasets, not trade portfolio construction.*
