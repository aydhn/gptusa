# Constraint-Aware Scoring and Normalization

## Composite Scoring
Generates constraint-aware composite scores considering:
- Sizing Score
- Risk Score
- Robustness Score
- Liquidity Score
- Cost Score
- Diversification Score

## Normalization Process
The normalization engine iterates over derived composite factors and normalizes prototype weights.
- **Max Sandbox Cap:** Ensures no prototype weight breaches the global maximum bound limit.
- **Group Sandbox Cap:** Modulates segment allocations dynamically via fractional thresholds.
- **Sandbox-Only Behavior:** All calculations ensure modifications act uniformly and never translate directly to operational capital bounds.
