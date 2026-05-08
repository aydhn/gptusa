# Comparison Limitations

1. **Simulation Only**: Both Paper and Backtest are local simulations. There is no real broker connection.
2. **No Real Execution**: The system does not route, generate, or manage live/demo orders on external platforms.
3. **Price Discrepancies**: Local cache prices (e.g. yfinance daily bars) used in paper trading might not perfectly mirror real-time intraday data.
4. **Matching Heuristics**: The trade and fill matching uses proximity heuristics (time tolerances) and might mismatch if highly clustered trades occur.
5. **Assumption Divergence**: Differences in fees, slippage, and next-open assumptions heavily influence the "Execution Realism Gap."
6. **No Investment Advice**: The metrics and gaps reported do not constitute investment advice.
7. **No Web/Dashboard**: All reports are file-based and CLI-driven. No web dashboard exists.
