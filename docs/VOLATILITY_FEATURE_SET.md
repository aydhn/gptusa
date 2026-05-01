# Volatility Feature Sets

The USA Signal Bot groups multiple volatility indicators into logically categorized **Indicator Sets** for easy execution via the Feature Engine.

## Included Sets

### `basic_volatility`
A simple set covering standard volatility measures:
- `true_range`
- `atr`
- `normalized_atr`
- `rolling_volatility`
- `price_range`

### `band_volatility`
Focuses strictly on Bollinger Band measurements:
- `bollinger_bands`
- `bollinger_bandwidth`
- `bollinger_percent_b`

### `channel_volatility`
Focuses on channel-based volatility indicators:
- `keltner_channel`
- `donchian_channel`

### `compression_volatility`
Designed to identify volatility squeezes and breakouts:
- `bollinger_bandwidth`
- `volatility_compression`
- `volatility_expansion`
- `normalized_atr`

### `full_volatility`
Computes all 12 volatility indicators concurrently.

## Execution and Storage

The Feature Engine can read local cached OHLCV data to compute these indicator sets. Results are validated against rules (e.g., negative ATR checks, invalid band ordering) and written to the local feature store in JSONL/CSV formats.

*Note: Volatility features are structural measurements only. They do not constitute trading advice or buy/sell signals.*

## CLI Commands

To compute the basic volatility set for cached symbols and write the result:
```bash
python -m usa_signal_bot volatility-feature-compute-cache --symbols AAPL,MSFT --timeframes 1d --set basic_volatility --write
```

To list and summarize the stored volatility feature metadata:
```bash
python -m usa_signal_bot volatility-feature-summary
```
