# Portfolio Limitations

This phase builds a structural engine for mapping risk decisions to allocations to simulate portfolio constraints. Please note:

1. **No Portfolio Optimization**: The engine does not solve for maximum returns, minimum variance, or optimal Kelly bet sizing. It applies rigid, heuristic math.
2. **Missing Correlation Matrix**: Diversification heuristics exist, but formal correlation/covariance grids do not influence baseline allocations.
3. **No Sector/Industry Exposure**: Sector, Asset Class, and Correlation specific caps remain empty placeholders.
4. **Not Investment Advice**: Outputs, such as "target weight" or "target notional", are solely simulation data.
5. **No Execution Engine**: The resulting `PortfolioBasket` and `AllocationResult` objects are never routed to an Alpaca/IBKR/broker interface. There is no paper trading mechanism included.
6. **Bias & Quality Assumptions**: Surviviorship biases, data quality degradation, and backtesting anomalies are inherently assumed and not solved at the portfolio construction stage.
