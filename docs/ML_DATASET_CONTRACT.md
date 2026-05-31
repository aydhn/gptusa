# ML Dataset Contract

Defines the structured boundaries for ML datasets, including source registry, features, targets, and labels.
- Forbidden outputs are strict (e.g., no buy_signal, sell_signal, portfolio_weight).
- Specifies required identifier (`symbol`) and time (`timestamp`) columns.
- Actual dataset assembly is deferred to Phase 137.
