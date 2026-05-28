# Market State Dataset Contract

The `MarketStateDatasetContract` defines the structural schema for regime market states.

## Schema
- **Required Columns:** `symbol`, `timestamp`, `market_index_context`, `volatility_context`, `trend_context`, `momentum_context`, `liquidity_context`, `breadth_context`, `factor_context`, `data_quality_context`, `event_context`, `calendar_context`, `regime_label_placeholder`, `regime_confidence_placeholder`, `regime_source_metadata`.

## Safety Constraints
- It explicitly **forbids** column names like `buy_signal`, `sell_signal`, `portfolio_weight`, `order`, etc.
- The default skeleton dataset generated produces only placeholder metadata (e.g., `unknown_regime`) and does **not** contain true predictions.
