# Multi-Timeframe Regime Confirmation

## Purpose
In trading and investment research, relying on a single timeframe (e.g. daily) for regime classification can lead to whipsaws and false signals. The Multi-Timeframe Regime Confirmation engine mitigates this risk by evaluating the market environment across multiple resolutions (Daily, Weekly, Monthly) and requiring alignment.

## Core Concepts

### Timeframe Resampler
Locally resamples daily OHLCV rows to weekly and monthly boundaries.
This ensures we don't need additional data pulls or external APIs.

### Regimes
- **Trend Regime:** Moving Averages (Short/Long) + Slope -> (STRONG_UPTREND, UPTREND, RANGE, DOWNTREND, STRONG_DOWNTREND, CHOPPY)
- **Volatility Regime:** Realized Volatility + ATR Percentile -> (COMPRESSED, NORMAL, EXPANDING, HIGH, EXTREME)
- **Momentum Regime:** Rate of Change + Acceleration -> (STRONG_POSITIVE, POSITIVE, NEUTRAL, NEGATIVE, STRONG_NEGATIVE, EXHAUSTED)
- **Liquidity Regime:** Dollar Volume + Thinning Score -> (DEEP, NORMAL, THINNING, THIN, ILLIQUID)

### Confirmation Status
- **CONFIRMED:** All timeframes agree on the primary trend direction.
- **PARTIAL:** Primary trend direction holds across most timeframes, but maybe missing data for one.
- **DIVERGENT:** One timeframe disagrees with the dominant trend.
- **CONFLICTED:** Hard conflicts between timeframes (e.g. Daily Strong Uptrend vs Weekly Strong Downtrend).

## Usage Examples

```bash
# Show configuration
python -m usa_signal_bot regime-map-info

# Run multi-timeframe confirmation for a specific symbol
python -m usa_signal_bot multi-timeframe-confirmation --symbol SPY --write
```
