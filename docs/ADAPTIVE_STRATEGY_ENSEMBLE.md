# Adaptive Strategy Ensemble

## Overview
Adaptive Strategy Ensembles take gated strategy results and blend them based on regime appropriateness.

## Adaptive Weights
Weights are normalized dynamically. A SUPPRESSED strategy sees its weight reduced to 10% of its base, while an ALLOW strategy maintains or boosts its influence.

## Consensus Score
If multiple strategies agree (and are well-aligned with the regime), they form a STRONG_CONSENSUS. Conflicting families or directions reduce this to MIXED or CONFLICTED.

## Important Note
Strong consensus is purely an algorithmic heuristic and does **NOT** constitute certain success or an approval for live trading.

## CLI Examples
```bash
python -m usa_signal_bot adaptive-weights
python -m usa_signal_bot strategy-ensemble --symbol SPY --write
```
