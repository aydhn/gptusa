# Momentum Feature Set

The Momentum Indicator Pack provides predefined indicator sets for easy calculation of related momentum features in bulk.

## Available Indicator Sets

*   **`basic_momentum`**: Includes standard basic momentum indicators: RSI, ROC, and simple Momentum.
*   **`oscillator_momentum`**: Focuses on bound oscillators: RSI, Stochastic, Williams %R, and CCI.
*   **`rate_of_change_momentum`**: Focuses on price change rates and their derivatives: ROC, Momentum, Momentum Slope, Momentum Acceleration, and Normalized Momentum.
*   **`full_momentum`**: Includes all available momentum indicators.

## CLI Usage

To view information about a specific indicator set:
```bash
python -m usa_signal_bot momentum-indicator-set-info --set full_momentum
```

To compute an indicator set from cached data:
```bash
python -m usa_signal_bot momentum-feature-compute-cache --symbols AAPL,MSFT --timeframes 1d --set basic_momentum --write
```

To view a summary of generated momentum features:
```bash
python -m usa_signal_bot momentum-feature-summary
```

*Note: Feature calculation strictly requires valid OHLCV data to be present in the local cache. No external network requests are made during feature generation.*
