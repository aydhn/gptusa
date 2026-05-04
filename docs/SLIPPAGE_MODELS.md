# Slippage Models

This document describes the slippage models implemented in Phase 26 of the USA Signal Bot.

## Purpose
Slippage models estimate the difference between the expected price of a trade (e.g., the open or close price of a bar) and the actual executed price. Since this is an offline simulated backtester, these models rely on simple heuristic formulas to penalize execution prices. **These are strictly estimates and do not guarantee live market liquidity or identical execution prices.**

## Supported Models

1. **NONE**: Zero slippage. Assumes perfect execution at the simulated base price.
2. **FIXED_BPS**: Applies a static basis points penalty to every trade. `Buy price = Base + Slippage`, `Sell price = Base - Slippage`.
3. **SPREAD_PROXY**: Simulates crossing the bid-ask spread by applying half the `spread_bps` parameter as slippage.
4. **VOLUME_PARTICIPATION**: Slippage scales with trade size relative to bar volume. Formula applies a base `fixed_bps` plus a dynamically scaled impact penalty. If bar volume is zero, a safe max slippage penalty is applied.
5. **VOLATILITY_ADJUSTED**: Measures the High-Low range of the bar to proxy current market volatility and inflates the `fixed_bps` accordingly.

## Configuration Options
- `max_slippage_bps`: A ceiling for slippage to prevent wildly unrealistic calculations (e.g., during highly volatile or zero-volume bars).
- `liquidity_bucket`: The system labels symbols automatically (`VERY_LIQUID`, `ILLIQUID`, etc.) based on dollar volume for reporting purposes.

## Warning
Slippage models adjust the `fill_price` directly. Double counting slippage is avoided by clearly distinguishing transaction costs (fees) from execution quality (slippage) in the `net_pnl` calculations.

## CLI Usage
To run a backtest with custom slippage applied:
```bash
python -m usa_signal_bot backtest-run-signals-advanced --signal-file data/signals/example.jsonl --symbols AAPL --timeframe 1d --slippage-bps 2
```
