# Market Behavior Safety Guards

Phase 130 is strictly a research and diagnostic layer. It enforces multiple safety validators to ensure boundaries are maintained.

## Core Directives
1. **No Trade Signals**: Output columns/structs must not represent buy/sell signals.
2. **No Strategy Activation**: The `strategy_activation_allowed` flag must remain False.
3. **No Deployment**: No system patches or deployments are executed.
4. **No Order Decisions**: No target allocations or order definitions are produced.
5. **No Investment Advice**: Heuristics are for internal diagnostics only.
6. **No Broker/Paper Mutations**: The active_paper_enabled and paper_state_mutation_enabled flags remain False.
7. **No Model Training/Prediction**: `model_training_used` and `model_prediction_used` are set to False.
8. **No Network**: Paid API, web scraping, and HTML parsing remain disabled.
