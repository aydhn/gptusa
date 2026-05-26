# Feature Input Contracts

The `FeatureInputContract` ensures that input datasets flowing into the feature engine are strictly compliant.

## Required OHLCV Columns
Any dataset to be transformed must contain:
- symbol
- timestamp
- open, high, low, close
- adjusted_close
- volume
- source
- fetched_at_utc
- quality_flags

## Optional Metadata Context
Extra data inputs are optionally allowed if they provide context for factors:
- provider_quality_score
- source_trust_profile
- event_context_metadata
- calendar_validation_metadata
- data_lineage_metadata

**Strictly Blocked:**
- Network downloads (allow_network = false)
- Paid API inputs
- Broker order parameters
