# Advanced Feature Table Schema

Advanced feature tables extend Phase 117's core feature tables with additional derived columns.

## Rules
1. **Preserve Core Columns**: Base OHLCV and core indicators remain intact.
2. **Preserve Warmup Nulls**: NaN values from rolling windows must be preserved natively without interpolation.
3. **Forbidden Columns**: Any column containing `buy`, `sell`, `entry`, `exit`, `order`, `broker`, `portfolio_weight` is strictly blocked.
4. **Whitelisting**: Only Phase 117 indicators (like `macd_signal_9`) are allowed to use the word `signal`.

Any table failing schema validation will be rejected by the AdvancedFeatureComputationValidator.
