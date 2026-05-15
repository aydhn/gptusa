# Strategy Gating

## Overview
Strategy Gating acts as a local signal quality gate. Based on compatibility scores and regime transition risks, strategies receive one of the following decisions:
- ALLOW: Full confidence, no penalties.
- ALLOW_WITH_PENALTY: Slightly discounted confidence.
- REVIEW: Significant misalignment, heavy penalties apply.
- SUPPRESS: Strongly misaligned, candidate metadata suppressed.
- BLOCK: Explicitly forbidden conditions (e.g., untradable).

## Penalties
Gating decisions automatically apply:
- Confidence Multipliers (0.0 to 1.0)
- Rank Penalties (0 to 100)

## CLI Example
```bash
python -m usa_signal_bot strategy-gate --strategy trend_following --symbol SPY --write
```
