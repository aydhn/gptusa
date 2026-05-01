# Momentum Indicators

USA Signal Bot includes a robust momentum indicator pack designed to provide standard momentum features without generating trade signals directly.

## Available Indicators

*   **RSI (Relative Strength Index)**: Measures the magnitude of recent price changes to evaluate overbought or oversold conditions.
    *   Parameters: `window` (default 14), `column` (default "close").
    *   Outputs: `{column}_rsi_{window}`.
*   **Stochastic Oscillator**: Compares a particular closing price to a range of its prices over a certain period of time.
    *   Parameters: `k_window` (default 14), `d_window` (default 3).
    *   Outputs: `stoch_k_{k_window}`, `stoch_d_{k_window}_{d_window}`.
*   **ROC (Rate of Change)**: Measures the percentage change in price between the current price and the price a certain number of periods ago.
    *   Parameters: `window` (default 12), `column` (default "close").
    *   Outputs: `{column}_roc_{window}`.
*   **Momentum**: Measures the absolute change in price between the current price and the price a certain number of periods ago.
    *   Parameters: `window` (default 10), `column` (default "close").
    *   Outputs: `{column}_momentum_{window}`.
*   **Williams %R**: A momentum indicator that is the inverse of the Fast Stochastic Oscillator. Also reflects the level of the close relative to the highest high for the look-back period.
    *   Parameters: `window` (default 14).
    *   Outputs: `williams_r_{window}`.
*   **CCI (Commodity Channel Index)**: Measures the current price level relative to an average price level over a given period of time.
    *   Parameters: `window` (default 20), `constant` (default 0.015).
    *   Outputs: `cci_{window}`.
*   **Momentum Slope**: Calculates the linear regression slope of a base momentum indicator (e.g., RSI, ROC) over a given window.
    *   Parameters: `base_indicator` (default "rsi"), `window` (default 14), `slope_window` (default 5), `column` (default "close").
    *   Outputs: `{base_indicator}_{window}_slope_{slope_window}`.
*   **Momentum Acceleration**: Calculates the rate of change (slope) of the momentum slope over a given window.
    *   Parameters: `base_indicator` (default "roc"), `window` (default 12), `slope_window` (default 5), `column` (default "close").
    *   Outputs: `{base_indicator}_{window}_acceleration_{slope_window}`.
*   **Normalized Momentum**: Normalizes raw momentum values to a 0-100 scale using a rolling min/max approach over a specified normalization window.
    *   Parameters: `window` (default 20), `normalization_window` (default 100), `column` (default "close").
    *   Outputs: `{column}_normalized_momentum_{window}_{normalization_window}`.

## CLI Usage

List all registered momentum indicators:
```bash
python -m usa_signal_bot momentum-indicator-list
```

These indicators are strictly for feature engineering and do not generate direct buy/sell signals.
