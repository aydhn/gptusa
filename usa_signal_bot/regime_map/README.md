# Regime Map Engine (Phase 58)

This directory contains the Regime Map system, which elevates single-symbol/single-timeframe regime detection to multi-timeframe confirmation and cross-sectional (universe-level) map analysis.

## Key Concepts
- **Timeframe Resampler:** Safely resamples OHLCV from Daily to Weekly/Monthly locally without external APIs.
- **Regime Confirmations:**
  - Trend
  - Volatility
  - Momentum
  - Liquidity
- **Multi-Timeframe Engine:** Ensures trend alignment across Daily, Weekly, and Monthly data.
- **Cross-Sectional Map:** Evaluates market breadth and return dispersion to classify the universe (e.g. Broad Uptrend, Rotation, Risk-Off).
- **Transition Detector & Risk:** Identifies potentially dangerous regime shifts (e.g. Trend to Range, Low to High Volatility).
- **Symbol Alignment:** Scores how well a specific symbol aligns with the broader universe regime.

## Critical Constraints
- **NO LIVE TRADING:** A "CONFIRMED" regime or "ALIGNED" status does not constitute a live trade approval.
- **NO INVESTMENT ADVICE:** The outputs of this module are operational heuristics for historical backtesting and local research only.
- **LOCAL COMPUTE ONLY:** No external breadth or sector APIs are used. Everything is calculated over the local SQLite/CSV datasets.
