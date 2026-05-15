# Regime Transition Risk

## Purpose
Markets are most dangerous during transitions. This subsystem detects structural shifts in the regime map and assigns a risk score.

## Detected Transitions
- **Trend:** `TREND_TO_RANGE`, `RANGE_TO_TREND`, `UPTREND_TO_DOWNTREND`, `DOWNTREND_TO_UPTREND`
- **Volatility:** `LOW_VOL_TO_HIGH_VOL`, `HIGH_VOL_TO_LOW_VOL`
- **Liquidity:** `LIQUIDITY_NORMAL_TO_THIN`
- **Breadth:** `BREADTH_RISK_ON_TO_OFF`
- **Momentum:** `MOMENTUM_EXHAUSTION`
- **Cross-Sectional:** `REGIME_BREAK`

## Risk Scoring
Each transition carries a base weight. The engine aggregates these to produce a unified risk level:
- `NONE`, `LOW`, `MODERATE`, `HIGH`, `CRITICAL`

*Note: Risk scores are heuristic approximations, not definitive predictions of future market moves.*

## Usage Examples

```bash
# Detect transition for a single symbol
python -m usa_signal_bot regime-transition-detect --symbol SPY

# Calculate aggregate transition risk
python -m usa_signal_bot regime-transition-risk
```
