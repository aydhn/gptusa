# Feature Storage

Computed technical features are persisted locally for subsequent phases (such as backtesting or machine learning).

## Storage Location

Features are stored in the `data/features` directory by default.
To prevent path traversal, the storage engine strictly enforces that all writes occur within this root directory.

## Formats

1. **JSONL (Default)**: Highly compatible, easily appendable format. Each line represents a `FeatureRow` containing symbol, timeframe, timestamp, and a dictionary of computed features.
2. **CSV (Optional)**: Can be enabled via configuration. Generates flat table structures with a column for each feature.

## Feature Validation Report

Before storage, the engine generates a `FeatureValidationReport`. This checks for:
- Empty dataframes
- High ratios of `NaN` values
- Mathematically invalid features (e.g., Infinite values)

## Output Metadata

Alongside the raw feature rows, the engine saves a `{output_id}_meta.json` file. It tracks the provider, universe snapshot, requested indicators, output row counts, and storage paths.

## CLI Commands

Manage and view the feature store:
```bash
# Compute and write features
python -m usa_signal_bot feature-compute-cache --symbols AAPL,MSFT --timeframes 1d --indicators close_return,close_sma --write

# Inspect storage capacity and file counts
python -m usa_signal_bot feature-store-info

# View recent runs
python -m usa_signal_bot feature-summary
```
