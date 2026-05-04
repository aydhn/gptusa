# Slippage Models

The USA Signal Bot engine includes slippage models to simulate the adverse price impact encountered when executing orders in live markets.

**Important:** These models are estimates. Actual slippage depends on real-time order book dynamics, broker routing, and market conditions. This engine does not route live orders.

## Available Models

- **NONE**: No slippage is applied. Orders fill exactly at the simulated base price.
- **FIXED_BPS**: A constant percentage (in basis points) is added to buy prices and subtracted from sell prices.
- **VOLUME_PARTICIPATION**: Slippage scales exponentially if the order quantity exceeds a configured percentage of the bar's total volume.
- **SPREAD_PROXY**: Calculates slippage based on a static spread assumption.
- **VOLATILITY_ADJUSTED**: Increases the baseline slippage during periods of high volatility (measured by the bar's high-low range).

## Price Impact

- **BUY Orders**: Slippage increases the fill price.
- **SELL Orders**: Slippage decreases the fill price (cannot drop below 0).

## Liquidity Bucket

Fills are categorized into liquidity buckets (VERY_LIQUID to VERY_ILLIQUID) based on the dollar volume of the bar in which they were executed. This helps analyze slippage performance across different liquidity regimes.

## Max Slippage Guard

To prevent catastrophic outliers (especially in the volume and volatility models), a `max_slippage_bps` parameter acts as a hard cap on the applied slippage.

## CLI Usage

Override slippage during an advanced backtest run:

```bash
python -m usa_signal_bot backtest-run-signals-advanced --signal-file data/signals/example.jsonl --symbols AAPL --timeframe 1d --slippage-bps 2
```
