# Factor Candidate Definitions

Factor Candidate Definitions specify composite formulas that combine grouped features. They represent standard market factors for research purposes.

## Pre-Registered Candidates
- Momentum, Trend, Volatility, Liquidity, Relative Strength
- Contextual Factors (Quality, Event, Calendar)
- Meta Factors (Data Confidence, Composite Research)

## Scope
- Defined by `FactorComponent` structures (which apply simple transforms like `standardized_z_score`).
- Targets are built using a compositional syntax (e.g., `linear_weighted_sum`).
- True factor calculation and normalization happen in **Phase 121**. Phase 120 simply maps the definitions and component mappings.

## Limitations
Factor Candidates do NOT represent investment advice.
