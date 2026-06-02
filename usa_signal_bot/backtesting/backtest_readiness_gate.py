from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestReadinessRule,
    BacktestReadinessGate,
    AdvancedMLClosureIngestionResult,
    BacktestDatasetContract,
    BacktestResearchInputContract,
    MarketSimulationContract,
    BacktestSafetyBoundaryResult,
    create_backtest_readiness_rule_id,
    create_backtest_readiness_gate_id
)
from usa_signal_bot.core.enums import BacktestReadinessRuleKind, BacktestReadinessStatus

def build_backtest_readiness_rules(
    ingestion: AdvancedMLClosureIngestionResult,
    dataset_contract: BacktestDatasetContract,
    research_contract: BacktestResearchInputContract,
    market_contract: MarketSimulationContract,
    safety_boundary: BacktestSafetyBoundaryResult
) -> list[BacktestReadinessRule]:

    def make_rule(kind: BacktestReadinessRuleKind, name: str, passed: bool) -> BacktestReadinessRule:
        status = BacktestReadinessStatus.PASSED if passed else BacktestReadinessStatus.FAILED
        return BacktestReadinessRule(
            rule_id=create_backtest_readiness_rule_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            rule_kind=kind,
            name=name,
            status=status,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=f"Checking {name}",
            warnings=[],
            errors=[] if passed else [f"Failed {name}"],
            risk_flags=[],
            metadata={}
        )

    rules = [
        make_rule(BacktestReadinessRuleKind.ADVANCED_ML_CLOSURE_VALID, "Advanced ML Closure Valid", ingestion.ready_for_phase146),
        make_rule(BacktestReadinessRuleKind.DATASET_CONTRACT_VALID, "Dataset Contract Valid", dataset_contract.contract_valid),
        make_rule(BacktestReadinessRuleKind.RESEARCH_INPUT_BOUNDARY_VALID, "Research Input Boundary Valid", research_contract.contract_valid),
        make_rule(BacktestReadinessRuleKind.MARKET_SIMULATION_CONTRACT_VALID, "Market Simulation Contract Valid", market_contract.simulation_contract_valid),
        make_rule(BacktestReadinessRuleKind.SAFETY_BOUNDARY_VALID, "Safety Boundary Valid", safety_boundary.boundary_passed),
        make_rule(BacktestReadinessRuleKind.NO_LIVE_TRADING, "No Live Trading", safety_boundary.no_live_trading),
        make_rule(BacktestReadinessRuleKind.NO_PAPER_MUTATION, "No Paper Mutation", safety_boundary.no_paper_state_mutation),
        make_rule(BacktestReadinessRuleKind.NO_FULL_BACKTEST_RUN, "No Full Backtest Run", safety_boundary.no_full_backtest_run_phase146)
    ]

    return rules

def build_backtest_readiness_gate(
    ingestion: AdvancedMLClosureIngestionResult,
    dataset_contract: BacktestDatasetContract,
    research_contract: BacktestResearchInputContract,
    market_contract: MarketSimulationContract,
    safety_boundary: BacktestSafetyBoundaryResult
) -> BacktestReadinessGate:

    rules = build_backtest_readiness_rules(ingestion, dataset_contract, research_contract, market_contract, safety_boundary)
    passed = all(r.passed for r in rules)

    status = BacktestReadinessStatus.PASSED if passed else BacktestReadinessStatus.BLOCKED

    return BacktestReadinessGate(
        gate_id=create_backtest_readiness_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        rules=rules,
        dataset_contract=dataset_contract,
        research_input_contract=research_contract,
        market_simulation_contract=market_contract,
        safety_boundary=safety_boundary,
        ready_for_phase147=passed,
        research_data_only=True,
        offline_backtest_research_only=True,
        live_trading_enabled=not safety_boundary.no_live_trading,
        paper_trading_enabled=not safety_boundary.no_paper_trading,
        broker_execution_enabled=not safety_boundary.no_broker_execution,
        order_creation_enabled=not safety_boundary.no_order_creation,
        paper_state_mutation_enabled=not safety_boundary.no_paper_state_mutation,
        full_backtest_run_executed=not safety_boundary.no_full_backtest_run_phase146,
        walk_forward_executed=not safety_boundary.no_walk_forward_phase146,
        stress_test_executed=not safety_boundary.no_stress_test_phase146,
        monte_carlo_executed=not safety_boundary.no_monte_carlo_phase146,
        deployment_allowed=not safety_boundary.no_deployment,
        investment_advice=ingestion.investment_advice,
        warnings=[],
        errors=[] if passed else ["Readiness gate blocked. Phase 146 not ready for Phase 147."],
        risk_flags=[],
        metadata={}
    )

def backtest_readiness_passed(gate: BacktestReadinessGate) -> bool:
    return gate.status == BacktestReadinessStatus.PASSED

def backtest_readiness_blocks_phase147(gate: BacktestReadinessGate) -> bool:
    return not gate.ready_for_phase147

def validate_backtest_readiness_gate(gate: BacktestReadinessGate) -> list[str]:
    errors = []
    if gate.status != BacktestReadinessStatus.PASSED:
        errors.append("Readiness gate did not pass.")
    return errors

def backtest_readiness_gate_summary(gate: BacktestReadinessGate) -> dict[str, Any]:
    return {"passed": gate.status == BacktestReadinessStatus.PASSED, "ready": gate.ready_for_phase147}

def backtest_readiness_gate_to_text(gate: BacktestReadinessGate, limit: int = 300) -> str:
    return f"ReadinessGate(status={gate.status.value}, ready_for_phase147={gate.ready_for_phase147})"
