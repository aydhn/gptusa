# Phase 118: Advanced Volatility, Momentum, Trend, Normalization and Cross-Sectional Feature Expansion

Phase 118 extends the core indicator foundation set in Phase 117 by adding advanced statistical, time-series, and cross-sectional features to the dataset. These include complex indicators like volatility-of-volatility, multi-horizon momentum, trend acceleration, Z-scores, percentile ranks, and cross-sectional rankings.

## Critical Limitation
Phase 118 is strictly an offline, local research data extension.
- **NO trade signals.**
- **NO order decisions.**
- **NO portfolio weights.**
- **NO broker execution.**
- **NO paper trading state mutations.**
- **NO real Telegram sends.**

## Key Components
- `advanced_volatility_features.py`: Computes realized, upside/downside volatility.
- `advanced_momentum_features.py`: Multi-horizon ROC, momentum acceleration.
- `advanced_trend_features.py`: Linear slope and distance-to-SMA z-scores.
- `normalization_features.py`: Standard Z-score, Min-Max, Robust Z-score.
- `cross_sectional_features.py`: Normalizations applied across a symbol universe at the same timestamp.

## CLI Usage
```bash
python -m usa_signal_bot advanced-features-info
python -m usa_signal_bot build-multi-symbol-advanced-feature-table --write
python -m usa_signal_bot advanced-feature-review --write
```
