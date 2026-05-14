
from usa_signal_bot.cost_robustness.sensitivity_matrix import run_execution_sensitivity_matrix
def test_matrix():
    mat = run_execution_sensitivity_matrix({"gross_total_pnl_usd": 100.0}, [{"gross_pnl_usd": 100.0}])
    assert mat is not None
