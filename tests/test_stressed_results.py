
from usa_signal_bot.cost_robustness.stressed_results import stress_backtest_result
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario, CostStressType, CostStressSeverity, FillRealismMode

def test_stressed_result():
    scen = CostStressScenario("s1", "n1", CostStressType.COMBINED, CostStressSeverity.BASELINE, 1.0, 1.0, 1.0, 1.0, 1.0, None, FillRealismMode.BASELINE, True)
    res = stress_backtest_result({"gross_total_pnl_usd": 100.0}, [{"gross_pnl_usd": 100.0}], scen)
    assert res is not None
