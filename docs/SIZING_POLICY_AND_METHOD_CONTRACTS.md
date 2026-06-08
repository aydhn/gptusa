# Sizing Policy and Method Contracts

## Sizing Policy
The `SizingPolicy` represents the macro limits for the research prototypes (e.g., max/min prototype fraction allowed, penalties enabled).

## Method Contracts
The `SizingMethodContract` describes the available deterministic sizing methodologies (e.g., fixed-fractional, volatility-adjusted). Contracts are specifically designed to explicitly disallow outputs like `produces_actual_position_size`, `produces_target_weight`, `produces_order_size`.
