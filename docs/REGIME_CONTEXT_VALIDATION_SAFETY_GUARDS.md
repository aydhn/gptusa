# Regime-Context Validation Safety Guards

All processing in Phase 132 falls under the strictest possible offline-only, local boundary conditions:

1. **No Real Execution**: `activation_allowed`, `strategy_activation_allowed`, and `deployment_allowed` must be strictly `False`.
2. **No Trades or Orders**: `produces_trade_signal` and `produces_order_decision` are rigorously blocked.
3. **No Network**: Network calls, broker routing, and external APIs are turned off.
4. **No Unsafe Text**: Diagnostics output parsing fails if strings like "buy", "sell", "execution order", "kesin al", etc., appear anywhere in generated text or column names.
