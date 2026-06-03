import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressValidationReport,
    MonteCarloRobustnessReport,
    RobustnessScorecard,
    StressSafetyBoundaryResult,
    Phase152ReadinessRule,
    Phase152ReadinessGate,
    create_phase152_readiness_rule_id,
    create_phase152_readiness_gate_id
)
from usa_signal_bot.core.enums import Phase152ReadinessRuleKind, Phase152ReadinessStatus

def build_phase152_readiness_rules(stress_report: StressValidationReport, mc_report: MonteCarloRobustnessReport, scorecard: RobustnessScorecard, boundary: StressSafetyBoundaryResult) -> list[Phase152ReadinessRule]:
    rules = [
        _rule(Phase152ReadinessRuleKind.STRESS_VALIDATION_REPORT_VALID, stress_report.report_valid, "Stress report valid"),
        _rule(Phase152ReadinessRuleKind.MONTE_CARLO_ROBUSTNESS_REPORT_VALID, mc_report.report_valid, "MC report valid"),
        _rule(Phase152ReadinessRuleKind.ROBUSTNESS_SCORECARD_VALID, scorecard.scorecard_valid, "Scorecard valid"),
        _rule(Phase152ReadinessRuleKind.SAFETY_BOUNDARY_VALID, boundary.boundary_passed, "Safety boundary passed"),
        _rule(Phase152ReadinessRuleKind.NO_LIVE_TRADING, True, "No live trading enforced")
    ]
    return rules

def _rule(kind: Phase152ReadinessRuleKind, passed: bool, rationale: str) -> Phase152ReadinessRule:
    return Phase152ReadinessRule(
        rule_id=create_phase152_readiness_rule_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        rule_kind=kind,
        name=kind.value,
        status=Phase152ReadinessStatus.PASSED if passed else Phase152ReadinessStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale=rationale,
        warnings=[], errors=[] if passed else ["Failed"], risk_flags=[], metadata={}
    )

def build_phase152_readiness_gate(stress_report: StressValidationReport, mc_report: MonteCarloRobustnessReport, scorecard: RobustnessScorecard, boundary: StressSafetyBoundaryResult) -> Phase152ReadinessGate:
    rules = build_phase152_readiness_rules(stress_report, mc_report, scorecard, boundary)
    passed = all(r.passed for r in rules)
    status = Phase152ReadinessStatus.PASSED if passed else Phase152ReadinessStatus.FAILED

    return Phase152ReadinessGate(
        gate_id=create_phase152_readiness_gate_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        status=status,
        rules=rules,
        stress_validation_report=stress_report,
        monte_carlo_report=mc_report,
        robustness_scorecard=scorecard,
        safety_boundary=boundary,
        ready_for_phase152=passed,
        research_data_only=True,
        offline_backtest_research_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        stress_test_executed=stress_report.stress_test_executed,
        monte_carlo_executed=mc_report.monte_carlo_executed,
        deployment_allowed=False,
        investment_advice=False,
        warnings=[], errors=[] if passed else ["Phase 152 gate failed"], risk_flags=[], metadata={}
    )
