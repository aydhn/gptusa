# Normalization and Ranking Features

## Purpose
Raw technical indicator values are often non-stationary and scale-dependent. Normalization transforms these into features suitable for cross-sectional comparison and factor modeling.

## Methods
- **Rolling Z-Score**: Standard normalization over a sliding window.
- **Rolling Robust Z-Score**: Uses median and MAD (Median Absolute Deviation) to ignore outliers.
- **Min-Max Scaling**: Scales features to a [0, 1] range based on recent highs and lows.
- **Percentile Rank**: Ranks the current value as a percentile against the historical window.
- **Winsorization**: Caps outliers at specified percentiles (e.g., 1st and 99th).

**Disclaimer**: Normalization does not produce trade signals or portfolio allocation rules.
