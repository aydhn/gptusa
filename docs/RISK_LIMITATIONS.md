# Risk Engine Limitations

The Risk Engine serves as a simulated quantitative framework and assumes explicit boundaries to adhere to the project's local research-first paradigm.

## Critical Disclaimers
1. **Not Real Advice**: The Risk Engine provides an analytical sizing structure, but it is *not* registered portfolio advice or official financial consulting.
2. **No Broker Execution**: Decisions, `PositionSizingResult`, and approvals **do not and will not** generate paper or live orders.
3. **Mock Estimations**: `volatility_value` and `atr_value` rely strictly on localized historical data inferences. Errors or missing indicators will cause fallbacks or rejections.
4. **Data Provider Limits**: The same data constraints and limits from local yfinance / cached sources apply.
5. **No Optimization Engines**: There is no ML Kelly optimization, covariance-based portfolio balancing (like Markowitz), or any dynamic parameter hunting implemented in this framework.
6. **Research Layer Only**: Risk approval acts strictly as a filtration layer for backtesting and paper analysis.
