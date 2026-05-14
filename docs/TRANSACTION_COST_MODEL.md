# Transaction Cost Model

This module implements heuristic transaction cost components to increase the realism of backtests and paper trading within USA Signal Bot.

## Cost Components
*   **Commission Proxy**: Estimates commissions based on configured fee schedules (default is zero commission).
*   **Regulatory Fee Proxy**: Estimates SEC and FINRA TAF fees on sell/short executions.
*   **Spread Cost**: Estimates the cost of crossing the spread using heuristic crossing fractions (default half-spread).
*   **Slippage**: Uses dynamic convex curves to penalize large orders based on participation rate.
*   **Market Impact**: Calculates slippage, spread, and volatility penalties combined.

## CLI Usage

```bash
python -m usa_signal_bot transaction-cost-info
python -m usa_signal_bot fee-schedule
python -m usa_signal_bot commission-estimate --side sell --quantity 10 --notional 1000
```
