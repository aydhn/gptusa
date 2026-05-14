1. **Explore Existing Codebase**: Read `usa_signal_bot/core/enums.py`, `usa_signal_bot/core/config_schema.py`, and `config/default.yaml` to ensure changes align with the existing codebase structure.
2. **Create/Update Enums (`usa_signal_bot/core/enums.py`)**: Add `TransactionCostComponent`, `TransactionSide`, `OrderSizeClass`, `SlippageCurveType`, `MarketImpactStatus`, `CostRealismStatus`, `CostAdjustmentStatus`, `FillSimulationStatus`, `TransactionCostReportType`. Add related entries to `NotificationType` and `AlertType`.
3. **Verify Enums Update**: Run syntax check / read file to verify the changes in `usa_signal_bot/core/enums.py`.
4. **Create Configuration Schema (`usa_signal_bot/core/config_schema.py`)**: Add dataclasses for config `TransactionCostModelConfig`, `FeeScheduleProxyConfig`, `DynamicSlippageConfig`, `MarketImpactConfig`, `CostAdjustedBacktestConfig`, `CostAdjustedPaperConfig`, `CostAwareSignalsConfig`, `TransactionCostNotificationsConfig`.
5. **Verify Configuration Schema Update**: Run syntax check / read file to verify the changes in `usa_signal_bot/core/config_schema.py`.
6. **Update Config File (`config/default.yaml`)**: Add the newly defined configs with their default values.
7. **Create Exceptions (`usa_signal_bot/core/exceptions.py`)**: Define all specific transaction cost exceptions like `TransactionCostModelError` etc.
8. **Create Core Data Classes and Cost Models (`usa_signal_bot/transaction_costs/cost_models.py`)**: Create `TransactionCostInput`, `TransactionCostBreakdown`, `FeeScheduleProxy`, `SlippageCurvePoint`, `SlippageCurve`, `MarketImpactEstimate`, `FillSimulationResult`, `CostAdjustedTradeResult`, `TransactionCostReview`. Along with `to_dict` and `validate_*` methods.
9. **Verify Cost Models**: Run syntax check to verify `usa_signal_bot/transaction_costs/cost_models.py`.
10. **Implement Fee Schedule (`usa_signal_bot/transaction_costs/fee_schedule.py`)**: Implement `default_zero_commission_equity_fee_schedule`, `conservative_fee_schedule_proxy`, config loader and text generator.
11. **Implement Commission Estimator (`usa_signal_bot/transaction_costs/commission_estimator.py`)**: Implement functions for calculating USD commission and regulatory fee proxy.
12. **Implement Spread Cost Estimator (`usa_signal_bot/transaction_costs/spread_cost.py`)**: Implement bps/usd spread calculations based on half-spread assumption.
13. **Implement Slippage Curves (`usa_signal_bot/transaction_costs/slippage_curves.py`)**: Implement default and conservative curves, evaluation based on participation rate and multipliers.
14. **Implement Slippage Curve Builder (`usa_signal_bot/transaction_costs/slippage_curve_builder.py`)**: Build liquidity-adjusted curves combining volatility, liquidity and spread proxies.
15. **Implement Participation Cost (`usa_signal_bot/transaction_costs/participation_cost.py`)**: Calculate participation cost via predefined heuristic curves based on participation rate.
16. **Implement Volatility/Gap Penalty (`usa_signal_bot/transaction_costs/volatility_penalty.py`)**: Implement bps calculation based on ATR and gap heuristics.
17. **Implement Market Impact (`usa_signal_bot/transaction_costs/market_impact.py`)**: Implement impact estimator using participation rate, ATR, and spread as proxies.
18. **Implement Fill Simulator (`usa_signal_bot/transaction_costs/fill_simulator.py`)**: Construct `FillSimulationResult` applying side-based markups/markdowns on reference price.
19. **Implement Cost Adjusted Trade (`usa_signal_bot/transaction_costs/cost_adjusted_trade.py`)**: Given gross trade metrics, build full cost breakdown and calculate net metrics.
20. **Implement Storage (`usa_signal_bot/transaction_costs/cost_store.py`)**: Methods to read/write models as JSON, managing paths under `data/transaction_costs`.
21. **Implement Validation (`usa_signal_bot/transaction_costs/cost_validation.py`)**: Create validators to detect live/guaranteed/broker terminology and secret leaking.
22. **Implement Reporting (`usa_signal_bot/transaction_costs/cost_reporting.py`)**: Methods returning string descriptions for all dataclasses, clearly disclaiming realistic simulation.
23. **Verify all new Python Modules**: Run syntax check on all new Python files created in `usa_signal_bot/transaction_costs/`.
24. **Update Backtesting Integration (`usa_signal_bot/backtesting/transaction_costs.py` & `backtest_engine.py` & `basket_simulation.py` & `backtest_models.py`)**: Create `backtest_adapter.py` and integrate cost models to subtract from backtest return and raise warnings on extreme costs.
25. **Update Basket Simulation Integration (`usa_signal_bot/transaction_costs/basket_adapter.py`)**: Adapt basket results to account for turnover costs.
26. **Update Paper Trading Integration (`usa_signal_bot/paper/paper_runtime.py`, `usa_signal_bot/transaction_costs/paper_adapter.py`)**: Apply cost adjustments to simulated fills without creating actual broker orders.
27. **Update Signal/Candidate Integration (`usa_signal_bot/strategies/candidate_selection.py`, `usa_signal_bot/strategies/ranking.py`, `usa_signal_bot/transaction_costs/signal_adapter.py`)**: Attach cost metadata, and suppress candidates if cost exceeds threshold.
28. **Integrate with Quality/Observability (`usa_signal_bot/quality/data_quality_evaluator.py`, `usa_signal_bot/observability/metrics_collector.py`)**: Expand scorecards to factor transaction cost realism and gather operational metrics.
29. **Implement Notifications (`usa_signal_bot/notifications/notification_templates.py`, `usa_signal_bot/notifications/notification_adapters.py`)**: Create text templates/messages to preview cost and slippage reviews safely in dry-run mode.
30. **Update Health Check (`usa_signal_bot/core/health.py`)**: Append functions verifying the integrity of the cost components.
31. **Update CLI (`usa_signal_bot/app/cli.py`)**: Register sub-commands reflecting the new capabilities under Phase 55.
32. **Write Tests - Core Models & Costs**: Create and run `tests/test_cost_models.py`, `tests/test_fee_schedule.py`, `tests/test_commission_estimator.py`, `tests/test_spread_cost.py`, `tests/test_slippage_curves.py`, `tests/test_slippage_curve_builder.py`, `tests/test_participation_cost.py`, `tests/test_volatility_penalty.py`.
33. **Write Tests - Simulation & Store**: Create and run `tests/test_market_impact.py`, `tests/test_fill_simulator.py`, `tests/test_cost_adjusted_trade.py`, `tests/test_cost_store.py`, `tests/test_cost_validation.py`, `tests/test_cost_reporting.py`.
34. **Write Tests - Adapters & Integrations**: Create and run `tests/test_transaction_cost_backtest_adapter.py`, `tests/test_transaction_cost_basket_adapter.py`, `tests/test_transaction_cost_paper_adapter.py`, `tests/test_transaction_cost_signal_adapter.py`.
35. **Write Tests - CLI**: Create and run `tests/test_cli.py` integrating new commands.
36. **Create Documentation**: Create `docs/TRANSACTION_COST_MODEL.md`, `docs/DYNAMIC_SLIPPAGE_CURVES.md`, `docs/MARKET_IMPACT_SIMULATION.md`, `docs/COST_ADJUSTED_BACKTEST_AND_PAPER.md`, `docs/TRANSACTION_COST_LIMITATIONS.md`, `docs/PHASE_55_SUMMARY.md`.
37. **Run the full test suite**: Run the full test suite (e.g., `pytest tests/` and `python -m usa_signal_bot smoke`) to verify all components and ensure no regressions.
38. **Pre-commit step**: Complete pre-commit steps to make sure proper testing, verifications, reviews and reflections are done.
