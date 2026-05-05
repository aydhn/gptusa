# Allocation Methods

The system supports several baseline (non-optimizer) allocation methods:

1. **Equal Weight (`EQUAL_WEIGHT`)**: Divides the `max_total_allocation_pct` equally among all eligible candidates.
2. **Rank Weighted (`RANK_WEIGHTED`)**: Allocates weight proportionally based on each candidate's `rank_score`.
3. **Risk-Score Weighted (`RISK_SCORE_WEIGHTED`)**: Allocates weight inversely to risk (lower `risk_score` gets higher weight).
4. **Volatility Adjusted (`VOLATILITY_ADJUSTED`)**: Allocates weight inversely to volatility.
5. **Notional From Risk Decision (`NOTIONAL_FROM_RISK_DECISION`)**: Directly adopts the `approved_notional` defined in the prior RiskEngine phase.
6. **Hybrid Baseline (`HYBRID_BASELINE`)**: A naive combination of (rank * confidence) / (risk * volatility) proportional weights.
7. **Zero Allocation (`ZERO_ALLOCATION`)**: Assigns 0% weight to everything.

## Normalization & Caps
If `normalize_weights` is enabled, the calculated raw weights are scaled down to precisely match `max_total_allocation_pct` if they exceed it.
Additionally, each weight is hard-capped by `max_candidate_weight` to prevent a single symbol from absorbing too much portfolio equity.

## Missing Prices
If a candidate has a missing price or a zero price, its allocation is automatically set to `REJECTED/ZERO` with an associated warning, as notionals and fractional shares cannot be computed.

## Non-Optimizer Nature
These methods are heuristic baseline strategies. They do not employ numerical solvers, covariance matrices, or dynamic programming to seek an "optimal" mix.

## CLI Example
```bash
python -m usa_signal_bot allocation-preview --method rank_weighted --equity 100000 --cash 100000
```
