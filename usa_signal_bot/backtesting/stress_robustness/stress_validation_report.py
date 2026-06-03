import datetime
import hashlib

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressScenario,
    ScenarioReplayResult,
    ScenarioPerformanceMetric,
    ScenarioDrawdownDiagnostic,
    CostLiquiditySensitivityResult,
    RobustnessScorecard,
    StressValidationReport,
    create_stress_validation_report_id
)

def build_stress_validation_report(scenarios: list[StressScenario], scenario_results: list[ScenarioReplayResult], scenario_metrics: list[ScenarioPerformanceMetric], drawdown_diagnostics: list[ScenarioDrawdownDiagnostic], sensitivity: CostLiquiditySensitivityResult, scorecard: RobustnessScorecard) -> StressValidationReport:
    report = StressValidationReport(
        report_id=create_stress_validation_report_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        scenarios=scenarios,
        scenario_results=scenario_results,
        scenario_metrics=scenario_metrics,
        drawdown_diagnostics=drawdown_diagnostics,
        cost_liquidity_sensitivity=sensitivity,
        robustness_scorecard=scorecard,
        report_hash=None,
        report_valid=True,
        stress_test_executed=True,
        monte_carlo_executed=False, # Wait for MC report
        portfolio_optimization_enabled=False,
        strategy_activation_allowed=False,
        investment_advice=False,
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    report.report_hash = compute_stress_validation_report_hash(report)
    return report

def compute_stress_validation_report_hash(report: StressValidationReport) -> str:
    s = f"{len(report.scenarios)}:{report.robustness_scorecard.scorecard_hash}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
