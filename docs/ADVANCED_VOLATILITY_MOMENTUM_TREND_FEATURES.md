# Advanced Volatility, Momentum, and Trend Features

## Volatility
- **Realized Volatility**: Rolling standard deviation of returns (10, 20 periods).
- **Downside/Upside Volatility**: Splitting returns based on sign, then standard deviation.
- **Volatility of Volatility**: The rolling standard deviation of the 20-period realized volatility itself.
- **ATR Percentile**: The rolling percentile rank of the ATR.

## Momentum
- **Multi-Horizon Momentum**: Return over 20, 60, and 120 periods.
- **Momentum Acceleration**: The difference between short-term and long-term momentum.
- **Normalized Momentum**: Z-score of standard oscillators like RSI and MACD Histogram.

## Trend
- **Trend Slope**: Rolling linear regression slope of the price.
- **Trend Strength**: Slope normalized by current volatility.
- **MA Distance Normalized**: Z-score of the distance between price and its SMA.

**Disclaimer**: These metrics are research features only. None of these formulas produce a "buy" or "sell" signal.
