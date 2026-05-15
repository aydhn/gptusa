# Regime Alignment and Signal Gating

## Purpose
Evaluates how well an individual symbol's regime aligns with the broader cross-sectional market regime, and applies appropriate metadata (rank penalties or suppression) to candidate signals.

## Alignment Status
- `ALIGNED`
- `MOSTLY_ALIGNED`
- `MIXED`
- `DIVERGENT`
- `CONFLICTED`

## Impact on Strategy Candidates
1. **Rank Penalty:** `DIVERGENT` or `CONFLICTED` alignments incur a penalty score, moving the candidate lower down the selection queue.
2. **Suppression:** If configured, critically conflicted candidates are marked with a suppression flag (`regime_map_suppression: True`).
3. **No Modification to Core Signal:** The engine never reverses or alters the original signal direction (e.g. LONG remains LONG, just suppressed or penalized).

## Cost Robustness Integration
High regime transition risk triggers specific stress scenarios in the cost robustness engine (e.g. `Risk-Off Breadth Stress`, `Volatility Expansion Stress`).

## Usage Examples

```bash
# Evaluate alignment between SPY and the default universe map
python -m usa_signal_bot regime-alignment --symbol SPY
```
