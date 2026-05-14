from typing import Optional, List, Dict, Any

from usa_signal_bot.cost_robustness.backtest_adapter import attach_cost_robustness_to_backtest_result, backtest_requires_cost_review
from usa_signal_bot.cost_robustness.signal_adapter import attach_cost_robustness_to_candidate, suppress_candidate_if_cost_fragile
from usa_signal_bot.cost_robustness.robustness_models import CostFragilityAssessment
from usa_signal_bot.core.enums import CostRobustnessStatus

def test_backtest_adapter():
    res = {"metrics": {}}
    res2 = attach_cost_robustness_to_backtest_result(res)
    assert res2['metadata']['cost_robustness_status'] == "ROBUST"
    assert not backtest_requires_cost_review(res2)

def test_signal_adapter():
    cand = {"symbol": "AAPL"}
    ass = CostFragilityAssessment("id", "now", CostRobustnessStatus.FRAGILE, 30.0, [], None, None, None, {}, [], [])
    cand2 = attach_cost_robustness_to_candidate(cand, ass)
    assert cand2['metadata']['cost_robustness_attached']

    cand3 = suppress_candidate_if_cost_fragile(cand2, ass)
    assert cand3['metadata']['suppressed_due_to_fragility']
