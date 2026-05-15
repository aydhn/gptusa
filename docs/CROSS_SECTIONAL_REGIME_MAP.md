# Cross-Sectional Regime Map

## Purpose
The Cross-Sectional Regime Map evaluates the overall market environment by analyzing the distribution of individual symbol regimes across a defined universe.

## Core Components
- **Breadth Proxy**: Evaluates the ratio of symbols in an uptrend vs. downtrend, and positive vs. negative momentum.
- **Dispersion Proxy**: Measures the standard deviation of returns and volatility across the universe to identify rotation or "stock-picker" markets.

## Cross-Sectional Regimes
- **BROAD_UPTREND**: High participation in uptrends.
- **SELECTIVE_UPTREND**: Overall uptrend but concentrated in fewer names.
- **ROTATION / DISPERSION_HIGH**: High dispersion, sector rotation occurring.
- **BROAD_DOWNTREND / RISK_OFF**: High participation in downtrends.

## CLI Examples
```bash
python -m usa_signal_bot breadth-proxy
python -m usa_signal_bot dispersion-proxy
python -m usa_signal_bot cross-sectional-regime-map --write
```
