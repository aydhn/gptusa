# Feature Schema and Output Contract

The feature computation pipeline returns results that are validated by `FeatureOutputSchema` and checked by the `FeatureOutputContract`.

## Allowed Outputs
- FEATURE_METADATA
- FEATURE_SCHEMA
- FEATURE_PLAN
- LINEAGE_METADATA

## Blocked Outputs
Any output classified as a signal or execution command is completely blocked:
- TRADE_SIGNAL
- ORDER_DECISION
- BROKER_INSTRUCTION
- PAPER_STATE_MUTATION

Any feature or column name containing words like `buy`, `sell`, `signal`, or `order` will trigger a validation failure and block the entire pipeline.
