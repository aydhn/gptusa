# Risk Attribution

## Overview
The Risk Attribution module offers heuristic proxies to understand the sources of risk and drawdowns during backtesting and local paper trading. It is completely local and does not utilize external risk engines or quantitative optimization APIs.

## Key Risk Proxies
- **Drawdown Contribution:** Tracks running equity and assigns negative PnL periods to underlying dimensions (e.g. which symbols contributed most to the overall peak-to-trough decline).
- **Volatility Proxy:** Calculates the absolute PnL contribution percentage of a given dimension to proxy its contribution to overall return variance.
- **Exposure/Concentration:** Analyzes the notional allocation given to symbols, sectors, or regimes to find concentration risks.
- **Liquidity & Cost Fragility:** Flags strategies or symbols whose performance is severely degraded by slippage or impact estimations.

## Limitations
These calculations are proxies and heuristics. They are NOT professional financial risk models and should not be treated as a guarantee of future stability.

## CLI Usage
```bash
python -m usa_signal_bot drawdown-attribution --starting-equity 100000
python -m usa_signal_bot risk-attribution --dimension strategy
```
