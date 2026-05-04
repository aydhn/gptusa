# Walk-Forward Analysis Limitations

Walk-Forward Analysis is a powerful tool, but it is critical to understand its limitations:

1. **No Future Guarantees**: Walk-forward analysis (including out-of-sample results) is strictly historical research. It does NOT guarantee future performance.
2. **No Optimizer**: In Phase 28, this system performs evaluation only. There is no parameter optimizer or search algorithm running.
3. **Data Quality**: The analysis relies on locally cached `yfinance` data. Data anomalies, missing dividends, or splits can distort results.
4. **Survivorship Bias**: The active universe contains current constituents. Testing historically on a modern universe introduces survivorship bias.
5. **Execution Realism**: Results are based on simulated market conditions using next-open logic. They do not account for true market depth, impact, or live broker latencies.
6. **Transaction Costs**: Fees and slippage are hypothetical estimates defined in the configuration, not guaranteed broker rates.
