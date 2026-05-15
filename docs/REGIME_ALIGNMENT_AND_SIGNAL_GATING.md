# Regime Alignment and Signal Gating

## Purpose
To evaluate how an individual symbol's regime aligns with the broader cross-sectional market regime.

## Mechanisms
- **Rank Penalty**: Symbols that are "fighting" the broader market regime (e.g., buying a dip in a Risk-Off market) receive a penalty in the candidate ranking phase.
- **Candidate Suppression**: In cases of extreme conflict (e.g., CRITICAL transition risk or severe DIVERGENCE), candidates may be suppressed via metadata tagging.
- **Adapters**: Backtest, walk-forward, and paper trading modules append alignment metadata to their results.

## CLI Examples
```bash
python -m usa_signal_bot regime-alignment --symbol SPY
```

## Important Note
This module *does not* alter the fundamental direction of a generated signal, nor does it block broker orders (because this system has no live broker integration). All gating is done via metadata marking.
