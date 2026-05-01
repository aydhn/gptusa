# Price Action Indicators

The Price Action feature pack provides tools to extract meaningful shape, pattern, and structure data from OHLCV bars. These features are fundamentally descriptive and do not generate direct buy/sell signals on their own.

## Indicator Types

- **Candle Features**: Extracts `candle_body`, `full_range` (both absolute and percentage), and a `candle_direction_code` (1 for bullish, -1 for bearish, 0 for doji).
- **Wick Features**: Computes `upper_wick`, `lower_wick`, percentage versions, and a `wick_imbalance` metric.
- **Close Location Value (CLV)**: Measures where the close price falls within the bar's high-low range (0 to 1).
- **Gap Features**: Measures the percentage difference between the current open and the previous close, providing a `gap_direction_code`.
- **Breakout & Breakdown Distance**: Calculates the distance of the current close relative to a rolling window's high or low (shifted by 1 to prevent current bar lookahead leakage).
- **Inside/Outside Bar**: Binary flags and pattern codes indicating if a bar is inside or outside the previous bar's range.
- **Swing Points**: Detects confirmed swing highs and lows based on localized windows.
- **Market Structure**: Determines if the current confirmed swing forms a higher high (HH) or lower low (LL).
- **Range Expansion/Contraction**: Compares the current bar's range to a rolling average range.

## Important Note on Leakage

The **Swing Points** and **Market Structure** indicators rely on a `right_window` to confirm a high or low. This inherently uses future data relative to the peak or trough. The features are labeled as "confirmed" to denote this characteristic. When performing backtesting or predictive modeling, ensure you align these features at the point of confirmation, not at the time of the peak, to avoid lookahead bias.

## CLI Usage

List available price action indicators:
```bash
python -m usa_signal_bot price-action-indicator-list
```

View details for a specific indicator set:
```bash
python -m usa_signal_bot price-action-indicator-set-info --set full_price_action
```

Compute a price action set from cache and write output:
```bash
python -m usa_signal_bot price-action-feature-compute-cache --symbols AAPL,MSFT --timeframes 1d --set basic_price_action --write
```
