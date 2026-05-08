# Paper Analytics Limitations

The Paper Analytics and Risk modules are strictly limited to local simulated runs. Users must be aware of the following fundamental limitations:

## Simulated Execution
- All analytics rely on local simulation. There is no connection to a broker or real exchange.
- Fills are generated using hypothetical models. Real-world issues such as slippage, liquidity constraints, spread widening, and partial fills are not completely modeled.
- Equity snapshots are calculated using cached daily closing prices.

## No Live Risk Mitigation
- The drawdown monitor and risk reporting modules **DO NOT** execute any live trades.
- If a risk limit is breached or a critical drawdown occurs, the system only generates a local warning or log output. It does not automatically sell or stop-loss.

## Not Investment Advice
- Any alerts, notifications, or Telegram messages regarding "strong performance" or "weak performance" are mechanical bucket classifications based on the local simulation.
- These notifications do not constitute investment advice.
- You must not interpret a high win rate or profit factor in this local report as a guarantee of future real-world profitability.

## No External Services
- No live broker API, demo broker API, or paid services are used to compile these reports.
- Dashboard views are entirely omitted in favor of text and JSON reporting.
