import datetime
import hashlib

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    ScenarioReplayResult,
    MonteCarloDistributionSummary,
    TailRiskDiagnostic,
    CostLiquiditySensitivityResult,
    RobustnessScorecard,
    create_robustness_scorecard_id
)
from usa_signal_bot.core.enums import StressRobustnessQuality

def build_robustness_scorecard(scenario_results: list[ScenarioReplayResult], mc_summary: MonteCarloDistributionSummary, tail_risk: list[TailRiskDiagnostic], sensitivity: CostLiquiditySensitivityResult) -> RobustnessScorecard:
    scenario_pass = calculate_scenario_pass_rate(scenario_results)
    tail_score = calculate_tail_risk_score(mc_summary, tail_risk)

    scores = [s for s in [scenario_pass, tail_score, sensitivity.combined_sensitivity_score] if s is not None]
    overall = sum(scores) / len(scores) if scores else None

    scorecard = RobustnessScorecard(
        scorecard_id=create_robustness_scorecard_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        scenario_count=len(scenario_results),
        monte_carlo_path_count=mc_summary.path_count,
        scenario_pass_rate=scenario_pass,
        monte_carlo_loss_probability=mc_summary.loss_probability,
        monte_carlo_ruin_probability_approx=mc_summary.ruin_probability_approx,
        tail_risk_score=tail_score,
        cost_liquidity_sensitivity_score=sensitivity.combined_sensitivity_score,
        overall_robustness_score=overall,
        quality=infer_stress_robustness_quality(overall),
        scorecard_hash=None,
        scorecard_valid=True,
        not_investment_advice=True,
        not_strategy_activation=True,
        not_deployment_approval=True,
        research_data_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    scorecard.scorecard_hash = compute_robustness_scorecard_hash(scorecard)
    return scorecard

def calculate_scenario_pass_rate(results: list[ScenarioReplayResult]) -> float | None:
    if not results:
        return None
    # Assuming pass if stressed_equity > 0
    passed = sum(1 for r in results if r.final_stressed_equity is not None and r.final_stressed_equity > 0)
    return passed / len(results)

def calculate_tail_risk_score(mc_summary: MonteCarloDistributionSummary, tail_risk: list[TailRiskDiagnostic]) -> float | None:
    if mc_summary.ruin_probability_approx is None:
        return None
    # 1.0 is perfect (0 ruin), 0.0 is terrible (ruin > 10%)
    score = 1.0 - (mc_summary.ruin_probability_approx * 10)
    return max(0.0, score)

def infer_stress_robustness_quality(score: float | None) -> StressRobustnessQuality:
    if score is None:
        return StressRobustnessQuality.UNKNOWN
    if score > 0.8:
        return StressRobustnessQuality.HIGH
    if score > 0.5:
        return StressRobustnessQuality.ACCEPTABLE
    if score > 0.2:
        return StressRobustnessQuality.WARNING
    return StressRobustnessQuality.LOW

def compute_robustness_scorecard_hash(scorecard: RobustnessScorecard) -> str:
    s = f"{scorecard.overall_robustness_score}:{scorecard.scenario_pass_rate}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
