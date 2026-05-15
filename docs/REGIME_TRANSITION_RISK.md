# Regime Transition Risk

## Purpose
To detect structural shifts in the market environment before they become fully established and to assign a risk score to these transitions.

## Key Transitions Detected
- **TREND_TO_RANGE**: Uptrend stalling into consolidation.
- **RANGE_TO_TREND**: Breakout from consolidation.
- **LOW_VOL_TO_HIGH_VOL**: Volatility expansion.
- **LIQUIDITY_NORMAL_TO_THIN**: Drying up of liquidity.
- **MOMENTUM_EXHAUSTION**: Strong momentum fading.
- **BREADTH_RISK_ON_TO_OFF**: Broad market deterioration.

## Risk Levels
- NONE, LOW, MODERATE, HIGH, CRITICAL.

## CLI Examples
```bash
python -m usa_signal_bot regime-transition-detect --symbol SPY
python -m usa_signal_bot regime-transition-risk
```

## Disclaimer
Transition risk scores are heuristics based on historical data. They are not certain predictions of future market states and do not constitute financial advice.
