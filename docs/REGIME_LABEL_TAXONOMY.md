# Regime Label Taxonomy

The `RegimeLabelTaxonomy` standardizes the labels used in market state regime classification.

## Standard Labels
- `risk_on` / `risk_off`
- `high_volatility` / `low_volatility`
- `trending_up` / `trending_down`
- `range_bound`
- `liquidity_stress` / `normal_liquidity`
- `event_distorted`
- `data_quality_degraded`
- `mixed_regime`
- `unknown_regime`

## Safety Boundaries
These labels are strictly contextual descriptors. They are **NOT** trade directions. For instance, `risk_off` does not map to a `sell` signal, and `trending_up` does not act as an `entry` signal. `activation_allowed` is `False`.
