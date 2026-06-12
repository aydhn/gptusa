🧪 [testing improvement] Add missing error path tests for validate_market_impact_report

🎯 **What:** The `validate_market_impact_report` function from `usa_signal_bot/transaction_costs/cost_validation.py` handles exceptions from `validate_market_impact_estimate` and generates a report indicating failure, but there were no tests covering these error paths.
📊 **Coverage:** This PR adds tests covering the three main error paths (ValueError) triggered from `validate_market_impact_estimate`:
- Missing or empty `symbol`.
- Negative `impact_bps`.
- Negative `impact_usd`.
✨ **Result:** Test coverage improved, giving more reliability for the error handling code inside the transaction cost validation logic.
