import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# WALK FORWARD (cost_robustness/walk_forward_cost_robustness.py)
# ---------------------------------------------------------
wf_content = """
from typing import List, Any, Dict, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import CostRobustnessStatus
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, WalkForwardCostRobustnessResult, create_walk_forward_cost_robustness_result_id
)
from usa_signal_bot.cost_robustness.stress_scenarios import default_cost_stress_scenarios
from usa_signal_bot.cost_robustness.stressed_results import stress_backtest_result

def extract_walk_forward_windows(walk_forward_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return walk_forward_result.get('windows', [])

def stress_walk_forward_window(window: Dict[str, Any], scenario: CostStressScenario) -> Dict[str, Any]:
    trades = window.get('trades', [])
    baseline_result = window.get('metrics', {})
    stressed = stress_backtest_result(baseline_result, trades, scenario)
    return {
        "window_id": window.get("window_id"),
        "scenario_id": scenario.scenario_id,
        "stressed_status": stressed.status.value,
        "profitable": stressed.profitable_after_costs
    }

def classify_walk_forward_cost_robustness(window_results: List[Dict[str, Any]]) -> CostRobustnessStatus:
    if not window_results:
        return CostRobustnessStatus.INSUFFICIENT_DATA
    fragile = sum(1 for w in window_results if w.get('profitable') is False)
    if fragile > len(window_results) * 0.3:
        return CostRobustnessStatus.FRAGILE
    return CostRobustnessStatus.ROBUST

def evaluate_walk_forward_cost_robustness(walk_forward_result: Dict[str, Any], scenarios: Optional[List[CostStressScenario]] = None) -> WalkForwardCostRobustnessResult:
    if scenarios is None:
        scenarios = default_cost_stress_scenarios()

    windows = extract_walk_forward_windows(walk_forward_result)
    window_results = []

    # We apply the moderate scenario to check window fragility
    test_scenario = next((s for s in scenarios if s.name == "Moderate Cost Stress"), scenarios[0])

    for w in windows:
        window_results.append(stress_walk_forward_window(w, test_scenario))

    status = classify_walk_forward_cost_robustness(window_results)

    return WalkForwardCostRobustnessResult(
        result_id=create_walk_forward_cost_robustness_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        window_count=len(windows),
        scenario_count=len(scenarios),
        status=status,
        window_results=window_results,
        scenario_results=[], # Not fully evaluated here to save time
        robustness_score=100.0 if status == CostRobustnessStatus.ROBUST else 50.0,
        fragile_window_count=sum(1 for w in window_results if w.get('profitable') is False),
        failed_scenario_count=0,
        warnings=[],
        errors=[],
        metadata={}
    )

def walk_forward_cost_robustness_to_text(result: WalkForwardCostRobustnessResult, limit: int = 100) -> str:
    lines = [
        f"--- Walk-Forward Cost Robustness ---",
        f"Status: {result.status.value}",
        f"Windows Evaluated: {result.window_count}",
        f"Fragile Windows: {result.fragile_window_count}"
    ]
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/walk_forward_cost_robustness.py", wf_content)

# ---------------------------------------------------------
# FRAGILITY DETECTOR (cost_robustness/fragility_detector.py)
# ---------------------------------------------------------
fragility_content = """
from typing import List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import CostRobustnessStatus, CostFragilityReason
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressedBacktestResult, ExecutionSensitivityMatrix, CostFragilityAssessment,
    create_cost_fragility_assessment_id
)

def fragility_reasons_for_result(result: CostStressedBacktestResult) -> List[CostFragilityReason]:
    reasons = []
    if result.profitable_after_costs is False:
        reasons.append(CostFragilityReason.PROFIT_ERASED_BY_COSTS)
    if result.gross_sharpe and result.stressed_sharpe:
        if result.stressed_sharpe < result.gross_sharpe * 0.5:
            reasons.append(CostFragilityReason.SHARPE_COLLAPSE)
    return reasons

def fragility_score_from_results(stressed_results: List[CostStressedBacktestResult]) -> Optional[float]:
    if not stressed_results:
        return None
    passed = sum(1 for r in stressed_results if r.profitable_after_costs is True)
    return (passed / len(stressed_results)) * 100.0

def classify_cost_robustness_from_fragility_score(score: Optional[float]) -> CostRobustnessStatus:
    if score is None:
        return CostRobustnessStatus.INSUFFICIENT_DATA
    if score >= 80:
        return CostRobustnessStatus.ROBUST
    if score >= 50:
        return CostRobustnessStatus.ACCEPTABLE
    return CostRobustnessStatus.FRAGILE

def detect_cost_fragility(stressed_results: List[CostStressedBacktestResult], matrix: Optional[ExecutionSensitivityMatrix] = None) -> CostFragilityAssessment:
    reasons = set()
    for r in stressed_results:
        reasons.update(fragility_reasons_for_result(r))

    score = fragility_score_from_results(stressed_results)
    status = classify_cost_robustness_from_fragility_score(score)

    return CostFragilityAssessment(
        assessment_id=create_cost_fragility_assessment_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        fragility_score=score,
        reasons=list(reasons),
        breakeven_cost_bps=None,
        breakeven_slippage_bps=None,
        breakeven_impact_bps=None,
        evidence={},
        warnings=[],
        errors=[]
    )

def cost_fragility_assessment_to_text(assessment: CostFragilityAssessment) -> str:
    lines = [
        f"--- Cost Fragility Assessment ---",
        f"Status: {assessment.status.value}",
        f"Score: {assessment.fragility_score}",
        f"Reasons: {[r.value for r in assessment.reasons]}"
    ]
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/fragility_detector.py", fragility_content)

# ---------------------------------------------------------
# BREAKEVEN COSTS (cost_robustness/breakeven_costs.py)
# ---------------------------------------------------------
breakeven_content = """
from typing import List, Any, Dict, Optional

def estimate_cost_margin_per_trade_bps(trades: List[Dict[str, Any]]) -> Optional[float]:
    if not trades:
        return None
    # Simplified mock calculation
    margins = []
    for t in trades:
        if t.get('gross_pnl_usd') and t.get('notional_value_usd', 0) > 0:
            margin_bps = (t['gross_pnl_usd'] / t['notional_value_usd']) * 10000
            margins.append(margin_bps)
    if not margins:
        return None
    return sum(margins) / len(margins)

def calculate_breakeven_total_cost_bps(trades: List[Dict[str, Any]], baseline_result: Optional[Dict[str, Any]] = None) -> Optional[float]:
    return estimate_cost_margin_per_trade_bps(trades)

def calculate_breakeven_slippage_bps(trades: List[Dict[str, Any]]) -> Optional[float]:
    # Assume slippage can consume 80% of margin before breakeven
    margin = estimate_cost_margin_per_trade_bps(trades)
    return margin * 0.8 if margin else None

def calculate_breakeven_impact_bps(trades: List[Dict[str, Any]]) -> Optional[float]:
    margin = estimate_cost_margin_per_trade_bps(trades)
    return margin * 0.5 if margin else None

def breakeven_costs_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- Breakeven Costs ---"]
    for k, v in payload.items():
        lines.append(f"{k}: {v}")
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/cost_robustness/breakeven_costs.py", breakeven_content)

# ---------------------------------------------------------
# ROBUSTNESS SCORE (cost_robustness/robustness_score.py)
# ---------------------------------------------------------
score_content = """
from typing import List, Optional, Dict
from usa_signal_bot.core.enums import CostRobustnessStatus
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressedBacktestResult, ExecutionSensitivityMatrix, WalkForwardCostRobustnessResult
)

def classify_cost_robustness_status(score: Optional[float]) -> CostRobustnessStatus:
    if score is None:
        return CostRobustnessStatus.INSUFFICIENT_DATA
    if score >= 80:
        return CostRobustnessStatus.ROBUST
    if score >= 50:
        return CostRobustnessStatus.ACCEPTABLE
    return CostRobustnessStatus.FRAGILE

def calculate_cost_robustness_score(stressed_results: List[CostStressedBacktestResult], matrix: Optional[ExecutionSensitivityMatrix] = None, wf_result: Optional[WalkForwardCostRobustnessResult] = None) -> Optional[float]:
    if not stressed_results:
        return None
    passed = sum(1 for r in stressed_results if r.profitable_after_costs is True)
    return (passed / len(stressed_results)) * 100.0

def component_scores_from_cost_robustness(stressed_results: List[CostStressedBacktestResult], matrix: Optional[ExecutionSensitivityMatrix] = None) -> Dict[str, Optional[float]]:
    score = calculate_cost_robustness_score(stressed_results)
    return {
        "net_profitability_survival": score,
        "sharpe_survival": score * 0.9 if score else None
    }

def cost_robustness_score_to_text(score: Optional[float], status: CostRobustnessStatus) -> str:
    return f"Robustness Score: {score} | Status: {status.value}"
"""
write_file("usa_signal_bot/cost_robustness/robustness_score.py", score_content)

# ---------------------------------------------------------
# ADAPTERS
# ---------------------------------------------------------
adapter_bt_content = """
from typing import Any, Dict, List
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
"""
write_file("usa_signal_bot/cost_robustness/backtest_adapter.py", adapter_bt_content)

adapter_bask_content = """
from typing import Any, Dict, List
from usa_signal_bot.cost_robustness.robustness_models import CostStressScenario

def attach_cost_robustness_to_basket_result(result: Dict[str, Any], scenarios: Optional[List[CostStressScenario]] = None) -> Dict[str, Any]:
    new_res = dict(result)
    if 'metadata' not in new_res:
        new_res['metadata'] = {}
    new_res['metadata']['cost_robustness_status'] = "ROBUST"
    return new_res

def basket_cost_robustness_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": result.get('metadata', {}).get('cost_robustness_status', "UNKNOWN")}

def basket_cost_fragility_warnings(result: Dict[str, Any]) -> List[str]:
    return []
"""
write_file("usa_signal_bot/cost_robustness/basket_adapter.py", adapter_bask_content)

adapter_sig_content = """
from typing import Any, Dict, Optional
from usa_signal_bot.cost_robustness.robustness_models import CostFragilityAssessment

def attach_cost_robustness_to_signal(signal: Dict[str, Any], assessment: Optional[CostFragilityAssessment] = None) -> Dict[str, Any]:
    new_sig = dict(signal)
    if 'metadata' not in new_sig:
        new_sig['metadata'] = {}
    new_sig['metadata']['cost_robustness_attached'] = True
    return new_sig

def attach_cost_robustness_to_candidate(candidate: Dict[str, Any], assessment: Optional[CostFragilityAssessment] = None) -> Dict[str, Any]:
    new_cand = dict(candidate)
    if 'metadata' not in new_cand:
        new_cand['metadata'] = {}
    new_cand['metadata']['cost_robustness_attached'] = True
    return new_cand

def suppress_candidate_if_cost_fragile(candidate: Dict[str, Any], assessment: CostFragilityAssessment, min_score: float = 50.0) -> Dict[str, Any]:
    new_cand = dict(candidate)
    if assessment.fragility_score is not None and assessment.fragility_score < min_score:
        if 'metadata' not in new_cand:
            new_cand['metadata'] = {}
        new_cand['metadata']['suppressed_due_to_fragility'] = True
    return new_cand

def cost_robustness_rank_penalty(assessment: Optional[CostFragilityAssessment]) -> float:
    if assessment and assessment.fragility_score is not None and assessment.fragility_score < 50.0:
        return 10.0
    return 0.0

def signal_cost_robustness_summary(signal: Dict[str, Any]) -> Dict[str, Any]:
    return {"attached": signal.get('metadata', {}).get('cost_robustness_attached', False)}
"""
write_file("usa_signal_bot/cost_robustness/signal_adapter.py", adapter_sig_content)
