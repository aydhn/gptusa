# Regime Cost Limitations

This system uses heuristic approximations for regime-aware execution costs. Please be aware of the following strictly enforced limitations:

1. **Heuristic Classifications:** Volatility and liquidity buckets are threshold-based heuristics, not deep-learning execution models.
2. **No Real Order Book:** The system does not possess Level-2 data, order book depth, or real micro-structure event streams.
3. **No Broker Fill Data:** Fill simulations rely entirely on mathematical adjustment of reference prices.
4. **No Fill Guarantees:** A selected cost curve is not a guarantee of true market slippage.
5. **Not Investment Advice:** Adaptive execution decisions (e.g., `USE_BASELINE_COSTS`) are operational configurations for local pipelines, **not** investment advice or live trading approvals.
6. **No Live Orders:** This architecture explicitly prohibits connecting to a live or demo broker API.
