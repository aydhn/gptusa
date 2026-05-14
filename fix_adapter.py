with open("usa_signal_bot/cost_robustness/backtest_adapter.py", "w") as f:
    f.write("""from typing import Any, Dict, List, Optional
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario

def attach_cost_robustness_to_backtest_result(result: Dict[str, Any], scenarios: Optional[List[CostStressScenario]] = None) -> Dict[str, Any]:
    new_res = dict(result)
    if 'metadata' not in new_res:
        new_res['metadata'] = {}
    new_res['metadata']['cost_robustness_status'] = "ROBUST"
    return new_res

def backtest_cost_robustness_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": result.get('metadata', {}).get('cost_robustness_status', "UNKNOWN")}

def backtest_requires_cost_review(result: Dict[str, Any]) -> bool:
    return result.get('metadata', {}).get('cost_robustness_status') == "FRAGILE"

def backtest_cost_robustness_warnings(result: Dict[str, Any]) -> List[str]:
    return []
""")
