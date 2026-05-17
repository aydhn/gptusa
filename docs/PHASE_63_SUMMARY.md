# Phase 63 Summary: Performance, Risk, and Signal Attribution

## Overview
Phase 63 establishes the core attribution framework for the USA Signal Bot. It provides deep analytics on local backtests and paper trading by decomposing overall performance and risk into fundamental dimensions like symbols, strategies, sectors, regimes, and individual signals.

## Implemented Features
- **Attribution Data Models:** Centralized dataclasses (`AttributionTradeEvent`, `AttributionContribution`, etc.) for managing structured analytics.
- **Trade Normalization:** An adapter capable of turning diverse backtest, paper, and rebalance outputs into normalized attribution events.
- **Performance Attribution:** Gross and net PnL decomposition with sample-size aware quality ratings.
- **Cost Attribution:** Slippage, impact, and fee proxy drag identification, specifically flagging cost-degraded groups.
- **Symbol & Strategy Attribution:** Identifying top/worst performers and tracking success rates locally.
- **Signal Contribution:** Classifying signal status (Contributive, Detrimental, Cost-Degraded).
- **Risk Attribution:** Simplified, dependency-free drawdown tracking and volatility/concentration risk proxies.
- **Adapters:** Integration into Backtest, Walk-Forward, Paper Analytics, Portfolio Construction, Rebalance, Allocation, and Risk layers.
- **Validation & Guards:** Strict verification blocking any broker IDs, live language, or guaranteed profit terminology.
- **CLI & Testing:** Comprehensive CLI support (`attribution-info`, `pnl-attribution`, etc.) and full test suite with no external/network calls.

## Prohibited Items (Strictly Enforced)
- **No Broker API / Live Trading:** The attribution logic evaluates simulated events. It does NOT generate or send live/demo orders.
- **No Heavy Dependencies:** Risk metrics rely exclusively on basic math using the Python standard library. (No scipy/statsmodels/cvxpy).
- **No Financial Advice:** Outputs explicitly state they do not offer investment advice or guarantee future performance.
