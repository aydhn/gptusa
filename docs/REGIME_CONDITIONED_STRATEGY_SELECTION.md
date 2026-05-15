# Regime Conditioned Strategy Selection

## Overview
The Regime Conditioned Strategy Selection system provides a metadata-driven approach to strategy orchestration. It evaluates current market regimes against a strategy's preferred and avoided conditions.

## Strategy Families
- TREND_FOLLOWING
- MEAN_REVERSION
- MOMENTUM
- BREAKOUT
- VOLATILITY_EXPANSION
- RANGE_TRADING
- DIVERGENCE
- RISK_OFF_DEFENSIVE

## Compatibility Score
Strategies are evaluated against regimes (e.g. UPTREND, EXHAUSTED) to calculate a score from 0-100:
- >80: Strongly Compatible
- >60: Compatible
- <40: Weak or Incompatible

## CLI Examples
```bash
python -m usa_signal_bot strategy-adaptation-info
python -m usa_signal_bot strategy-profiles
python -m usa_signal_bot strategy-compatibility --strategy trend_following
```
