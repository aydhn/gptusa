# Market Structure Features

The Market Structure capabilities focus on mapping the higher-level price dynamics that define trends and ranges over time. By combining individual price action characteristics (such as swings and breakouts), the system attempts to categorize the underlying market state.

## Core Components

1. **Swing Points**: Identifies local maximums (Swing Highs) and minimums (Swing Lows) within an N-bar window.
2. **Higher Highs (HH) / Lower Lows (LL)**: Evaluates the sequence of confirmed swing points to determine directional thrust.
3. **Inside / Outside Bars**: Tracks localized consolidation or expansion relative to the immediate prior bar.
4. **Breakout / Breakdown Distances**: Contextualizes the current close relative to recent rolling extremes.

## Lookahead Bias Awareness (Leakage)

A fundamental challenge in market structure analysis is the need for confirmation. A peak is only known to be a peak *after* price drops away from it.

*   **Right Window Dependency**: Features like `confirmed_swing_high` rely on the `right_window` parameter. This means the feature value at index `T` uses data up to index `T + right_window`.
*   **Mitigation**: The calculated flags are shifted forward by `right_window` steps in the final output. Therefore, the flag for a swing high that occurred at `T` will only appear as `1` at `T + right_window`. This design ensures that these features can be safely used in downstream backtesting without introducing lookahead bias.

## CLI Usage

To evaluate the structure features on cached data:
```bash
python -m usa_signal_bot price-action-feature-compute-cache --symbols AAPL --timeframes 1d --set structure_price_action --write
```

To list existing outputs:
```bash
python -m usa_signal_bot price-action-feature-summary
```
