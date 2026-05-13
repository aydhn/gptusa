# Execution Realism and Tradability Guard

This module provides liquidity, tradability, borrowability-proxy, and execution realism guards for the USA Signal Bot.

## Purpose
It aims to reduce blind spots regarding real-world tradability in signals, backtests, and paper trading results.

It implements checks for volume, dollar volume, price level, gap, spread proxy, slippage proxy, bar participation, stale data, minimum liquidity, and order size feasibility.

## Key Limitations
- It does not use any broker APIs.
- It does not send live or demo orders.
- The borrowability proxy is completely local and heuristic; it does not reflect real borrow availability.
- A PASS on the execution realism check is not an approval for live trading or investment advice.
- It is designed purely for research and paper/backtest realism enhancement.
