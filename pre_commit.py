import subprocess
print("Pre-commit check: running tests")
res = subprocess.run(["python", "-m", "pytest", "tests/test_cost_models.py", "tests/test_cli.py", "tests/test_fee_schedule.py", "tests/test_commission_estimator.py", "tests/test_spread_cost.py", "tests/test_slippage_curves.py", "tests/test_slippage_curve_builder.py", "tests/test_participation_cost.py", "tests/test_volatility_penalty.py", "tests/test_market_impact.py", "tests/test_fill_simulator.py", "tests/test_cost_adjusted_trade.py", "tests/test_transaction_cost_backtest_adapter.py", "tests/test_transaction_cost_basket_adapter.py", "tests/test_transaction_cost_paper_adapter.py", "tests/test_transaction_cost_signal_adapter.py", "tests/test_cost_store.py", "tests/test_cost_validation.py", "tests/test_cost_reporting.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("All tests passed.")
else:
    print("Tests failed.")
