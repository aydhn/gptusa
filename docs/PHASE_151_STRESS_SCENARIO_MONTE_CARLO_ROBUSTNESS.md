# Phase 151: Offline Stress Testing, Scenario Analysis, and Monte Carlo Robustness

## Overview
Phase 151 builds upon the walk-forward results from Phase 150. It conducts offline, deterministic, and simulated scenario analysis, stress testing, and Monte Carlo robustness checks to ensure a strategy can withstand adverse market environments before moving on to the final Phase 152 readiness closure and Phase 153 portfolio construction.

**WARNING:** This phase is strictly an **offline, research-only diagnostic** boundary.
- **NO** live trading.
- **NO** paper trading.
- **NO** broker execution.
- **NO** deployment or production patching.
- **NO** portfolio optimization or portfolio allocation output.
- Outputs of this phase do **NOT** constitute investment advice.

## Scenarios Implemented
- **Price Shock:** Stresses return series with severe to extreme multipliers.
- **Volatility Shock:** Magnifies volatility in returns.
- **Cost Shock:** Magnifies transaction costs.
- **Slippage Shock:** Magnifies slippage values.
- **Liquidity Shock:** Applies haircuts to positive returns representing low liquidity.
- **Missing Data:** Randomly zeroes out returns to simulate data loss.
- **Gap Risk:** Introduces severe single-day gaps.
- **Drawdown Shock:** Forces equity down to a specific floor.
- **Combined Adverse:** Combines multiple shocks.

## Monte Carlo Robustness
The system implements multiple resampling and perturbation methods:
- Return Bootstrap
- Block Bootstrap
- Return Permutation
- Path Perturbation
- Cost/Slippage Perturbation

Metrics generated include loss probability, ruin probability, and Left Tail diagnostics.

## CLI Usage (Simulated / Local Only)
```bash
python -m usa_signal_bot stress-robustness-info
python -m usa_signal_bot build-stress-scenario-policy --write
python -m usa_signal_bot run-scenario-replays --write
python -m usa_signal_bot run-monte-carlo-replays --write
python -m usa_signal_bot stress-robustness-review --write
```
