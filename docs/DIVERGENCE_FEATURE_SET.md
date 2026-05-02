# Divergence Feature Sets

To simplify computation, divergence indicators are grouped into predefined sets. These sets allow the Feature Engine to compute multiple divergences in a single pass over cached data.

## Available Indicator Sets

*   **`basic_divergence`**: Includes standard divergence indicators: `rsi_divergence` and `macd_hist_divergence`.
*   **`oscillator_divergence`**: Focuses on oscillator-based divergences: `rsi_divergence`, `macd_hist_divergence`, and `roc_divergence`.
*   **`volume_divergence`**: Focuses on volume-weighted divergences: `mfi_divergence` and `obv_divergence`.
*   **`full_divergence`**: Includes the complete suite of divergence indicators.

## Divergence Feature Outputs

When a divergence indicator runs, it generates several standard columns prefixing its name (e.g., `rsi_`, `macd_hist_`):

*   `{prefix}_regular_bullish_divergence`: Binary (0/1)
*   `{prefix}_regular_bearish_divergence`: Binary (0/1)
*   `{prefix}_hidden_bullish_divergence`: Binary (0/1)
*   `{prefix}_hidden_bearish_divergence`: Binary (0/1)
*   `{prefix}_divergence_strength`: Float (0.0 to 100.0) based on the magnitude of price vs oscillator changes.
*   `{prefix}_latest_divergence_code`: Integer code summarizing the state:
    *   `1`: Regular Bullish
    *   `-1`: Regular Bearish
    *   `2`: Hidden Bullish
    *   `-2`: Hidden Bearish
    *   `0`: None

## CLI Usage

Compute divergence features from local cache:
```bash
python -m usa_signal_bot divergence-feature-compute-cache --symbols AAPL,MSFT --timeframes 1d --set basic_divergence --write
```

View summary of stored divergence outputs:
```bash
python -m usa_signal_bot divergence-feature-summary
```

*Note: Feature calculation strictly requires valid OHLCV data to be present in the local cache. No external network requests are made during feature generation.*
