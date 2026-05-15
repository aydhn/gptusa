# Cross-Sectional Regime Map

## Purpose
While the multi-timeframe confirmation operates on a single symbol, the Cross-Sectional Regime Map evaluates the entire universe simultaneously. This provides essential context: is a symbol's strength isolated, or is the broader market supporting it?

## Components

### Market Breadth Proxy
Calculates the ratio of symbols in an uptrend and with positive momentum.
Classifications: `BROAD_RISK_ON`, `RISK_ON`, `MIXED`, `DETERIORATING`, `RISK_OFF`.

### Dispersion Proxy
Measures the cross-sectional return and volatility dispersion across the universe. High dispersion often indicates rotation or selective leadership rather than broad trend participation.

### Cross-Sectional Regime
Combines Breadth and Dispersion into a single unified state:
- `BROAD_UPTREND`: Strong breadth, low/moderate dispersion.
- `SELECTIVE_UPTREND`: Moderate breadth, higher dispersion.
- `ROTATION`: High dispersion despite some breadth.
- `DISPERSION_HIGH`: Very high dispersion, chaotic market.
- `BROAD_DOWNTREND` / `RISK_OFF`: Poor breadth, downtrends dominate.
- `MIXED`: No clear cross-sectional trend.

## Usage Examples

```bash
# Calculate breadth proxy
python -m usa_signal_bot breadth-proxy

# Calculate dispersion proxy
python -m usa_signal_bot dispersion-proxy

# Build the cross-sectional regime map
python -m usa_signal_bot cross-sectional-regime-map --write
```
