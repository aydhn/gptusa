# Volatility Indicators

This document provides details on the volatility indicator pack (Phase 16) added to the USA Signal Bot.

## Purpose
The Volatility Indicator Pack introduces a comprehensive suite of volatility and range-based features to augment price analysis. These features compute true range, average true ranges, various channels/bands, and rolling standard deviations. Importantly, they are strictly feature measurements and do not automatically generate buy or sell trading signals.

## Included Indicators

### 1. True Range (true_range)
Measures the greatest of the current high-low difference, the absolute current high minus the previous close, or the absolute current low minus the previous close.

### 2. Average True Range (atr)
The smoothed or moving average of the True Range. Supported methods: Wilder's smoothing (`wilder`), Simple Moving Average (`sma`), and Exponential Moving Average (`ema`).

### 3. Normalized ATR (normalized_atr)
The ATR value divided by the current close price. This provides a percentage-based volatility measure that can be compared across assets with different price scales.

### 4. Bollinger Bands (bollinger_bands)
A set of three bands: a middle Simple Moving Average, an upper band (SMA + N standard deviations), and a lower band (SMA - N standard deviations).

### 5. Bollinger Bandwidth (bollinger_bandwidth)
The difference between the upper and lower Bollinger Bands divided by the middle band, giving a measure of volatility contraction or expansion.

### 6. Bollinger Percent B (bollinger_percent_b)
A measure of where the closing price is in relation to the upper and lower Bollinger Bands.

### 7. Keltner Channels (keltner_channel)
Bands set above and below an Exponential Moving Average (EMA). The upper and lower bands are placed by adding and subtracting an ATR-derived value multiplied by a constant.

### 8. Donchian Channels (donchian_channel)
Formed by taking the highest high and the lowest low over a specified period. The middle band is the average of the upper and lower bands.

### 9. Rolling Volatility (rolling_volatility)
The rolling standard deviation of the percentage returns of the closing price. Can optionally be annualized.

### 10. Price Range Percentages (price_range)
Produces features measuring the high-low range as a percentage of the close (`high_low_range_pct`) and the body (open to close) range as a percentage of the true range (`body_range_pct`).

### 11. Volatility Compression (volatility_compression)
Measures the current Bollinger Bandwidth relative to the minimum bandwidth over a longer reference period. Values near 1.0 indicate a volatility squeeze.

### 12. Volatility Expansion (volatility_expansion)
Measures the current ATR relative to the maximum ATR over a reference period, highlighting when volatility is breaking out.

## Usage

List all registered volatility indicators:
```bash
python -m usa_signal_bot volatility-indicator-list
```

View the detailed parameters for a specific volatility indicator set:
```bash
python -m usa_signal_bot volatility-indicator-set-info --set full_volatility
```
