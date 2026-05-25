# Provider Selection Safety Guards

Phase 109 actively guards against any configuration that hints at active trading execution.

- **No Trade Signals**: `produces_trade_signal` is blocked.
- **No Order Decision**: `produces_order_decision` is blocked.
- **No Broker/Paper Mutation**: All mutating actions are mapped to score `0` and explicitly blocked.
- **Language Guard**: Text explanation blocks terms like "buy signal", "sell signal", "guaranteed return".
