# Risk Budgeting Baseline

Risk budgeting in the portfolio construction engine assesses how much "weight" is allocated to predefined groups, triggering warnings or `NEEDS_REVIEW` states if limits are exceeded.

## Measured Budgets
- **Total Budget**: Sum of all target weights. Maximum limit via `max_total_budget_pct`.
- **Symbol Budget**: Combined weight assigned to a specific symbol. Maximum limit via `max_symbol_budget_pct`.
- **Strategy Budget**: Combined weight assigned to candidates derived from the same strategy. Maximum limit via `max_strategy_budget_pct`.
- **Timeframe Budget**: Combined weight assigned to candidates of a specific timeframe. Maximum limit via `max_timeframe_budget_pct`.
- **Single Candidate Budget**: Maximum weight for any single item. Maximum limit via `max_single_candidate_budget_pct`.
- **Cash Buffer**: Minimal residual cash left post-allocation. Minimum via `min_cash_buffer_pct`.

## Concentration Guards
The concentration guards process is responsible for *capping* allocations to respect the above budgets if `cap_breaches` is set. Limits that are purely descriptive vs prescriptive are marked in the final `ConcentrationReport`. Sector and Correlation guards are currently placeholders (reserved for future phases).

## Not a Target / Recommendation
A risk budget is purely a hard limit structure to guard against overly concentrated backtest executions. It should not be misconstrued as an automated investment target or risk parity optimization schema.
