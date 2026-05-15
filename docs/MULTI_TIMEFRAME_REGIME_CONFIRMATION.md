# Multi-Timeframe Regime Confirmation

## Purpose
The purpose of multi-timeframe regime confirmation is to evaluate the trend, volatility, momentum, and liquidity regimes of a symbol across multiple time horizons (daily, weekly, monthly) to establish a more robust and less noisy view of its current market state.

## Timeframes
- **Daily**: Fast response, higher noise.
- **Weekly**: Core trend and regime identifier.
- **Monthly**: Long-term structural view.

## Confirmation Statuses
- **CONFIRMED**: All evaluated timeframes agree on the directional regime.
- **PARTIAL**: Agreement exists, but some longer timeframes lack sufficient data.
- **DIVERGENT**: The shorter timeframe disagrees with the longer timeframe (e.g., Daily Uptrend vs. Weekly Downtrend).
- **CONFLICTED**: Strong opposition across timeframes.
- **INSUFFICIENT_DATA**: Not enough data to make a determination.

## Regimes Evaluated
- **Trend**: UPTREND, DOWNTREND, RANGE, CHOPPY
- **Volatility**: COMPRESSED, NORMAL, EXPANDING, HIGH, EXTREME
- **Momentum**: POSITIVE, NEGATIVE, EXHAUSTED
- **Liquidity**: DEEP, NORMAL, THINNING, ILLIQUID

## CLI Examples
```bash
python -m usa_signal_bot regime-map-info
python -m usa_signal_bot multi-timeframe-confirmation --symbol SPY --write
```

## Disclaimer
Regime maps are for historical research and dry-run execution environments only. They do NOT constitute investment advice, and a "CONFIRMED" status is NOT a live trading approval.
