import datetime
import hashlib

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    MonteCarloPolicy,
    MonteCarloPath,
    MonteCarloReplayResult,
    MonteCarloDistributionSummary,
    TailRiskDiagnostic,
    MonteCarloRobustnessReport,
    create_monte_carlo_robustness_report_id
)

def build_monte_carlo_robustness_report(policy: MonteCarloPolicy, paths: list[MonteCarloPath], results: list[MonteCarloReplayResult], distribution: MonteCarloDistributionSummary, tail_risk: list[TailRiskDiagnostic]) -> MonteCarloRobustnessReport:
    report = MonteCarloRobustnessReport(
        report_id=create_monte_carlo_robustness_report_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        policy=policy,
        paths=paths,
        replay_results=results,
        distribution_summary=distribution,
        tail_risk_diagnostics=tail_risk,
        report_hash=None,
        report_valid=True,
        monte_carlo_executed=True,
        deterministic=True,
        simulated_only=True,
        real_order_created=False,
        broker_execution_used=False,
        paper_state_mutated=False,
        strategy_activation_allowed=False,
        investment_advice=False,
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    report.report_hash = compute_monte_carlo_robustness_report_hash(report)
    return report

def compute_monte_carlo_robustness_report_hash(report: MonteCarloRobustnessReport) -> str:
    s = f"{report.policy.policy_id}:{report.distribution_summary.summary_hash}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
