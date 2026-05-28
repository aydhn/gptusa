# Regime Input Contract

The `Regime Input Contract` defines the frozen artifacts required to start Phase 126.

## Requirements
- Frozen factor table references (`factor_table_refs`)
- Factor diagnostics references (`factor_diagnostics_refs`)
- Schema, Lineage, and Safety contracts
- Research reports

## Usage Allowances
- **Allowed Use:** `regime_research_only`
- **Disallowed Uses:** `trade_signal`, `order_decision`, `strategy_activation`, `portfolio_weight`, `broker_execution`, `paper_mutation`, `investment_advice`.

This contract guarantees that the regime classification inputs cannot be used to accidentally execute live trades.
