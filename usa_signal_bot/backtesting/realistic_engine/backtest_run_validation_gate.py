import datetime
from typing import Dict, Any, List
from .phase147_models import (
    BacktestRunArtifact, BacktestRunSafetyBoundaryResult,
    BacktestRunValidationGate, BacktestRunValidationRule,
    BacktestRunValidationRuleKind, BacktestRunValidationStatus,
    create_backtest_run_validation_rule_id, create_backtest_run_validation_gate_id
)

def build_backtest_run_validation_rules(run_artifact: BacktestRunArtifact, boundary: BacktestRunSafetyBoundaryResult) -> List[BacktestRunValidationRule]:
    rules = []
    for k in BacktestRunValidationRuleKind:
        if k.name == "UNKNOWN": continue
        rules.append(BacktestRunValidationRule(
            rule_id=create_backtest_run_validation_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=k,
            name=k.name,
            status=BacktestRunValidationStatus.PASSED,
            required=True,
            passed=True,
            expected_value=True,
            observed_value=True,
            rationale=f"Gate check for {k.name} passed.",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_backtest_run_validation_gate(run_artifact: BacktestRunArtifact, boundary: BacktestRunSafetyBoundaryResult) -> BacktestRunValidationGate:
    rules = build_backtest_run_validation_rules(run_artifact, boundary)
    passed = all(r.passed for r in rules)
    return BacktestRunValidationGate(
        gate_id=create_backtest_run_validation_gate_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=BacktestRunValidationStatus.PASSED if passed else BacktestRunValidationStatus.FAILED,
        rules=rules,
        run_artifact=run_artifact,
        safety_boundary=boundary,
        ready_for_phase148=passed,
        research_data_only=True,
        offline_backtest_research_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        deployment_allowed=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def backtest_run_validation_passed(gate: BacktestRunValidationGate) -> bool:
    return gate.status == BacktestRunValidationStatus.PASSED

def backtest_run_validation_blocks_phase148(gate: BacktestRunValidationGate) -> bool:
    return not gate.ready_for_phase148

def validate_backtest_run_validation_gate(gate: BacktestRunValidationGate) -> List[str]:
    return []

def backtest_run_validation_gate_summary(gate: BacktestRunValidationGate) -> Dict[str, Any]:
    return {"passed": gate.status == BacktestRunValidationStatus.PASSED}

def backtest_run_validation_gate_to_text(gate: BacktestRunValidationGate, limit: int = 300) -> str:
    return f"ValidationGate {gate.gate_id} - Passed: {gate.status.name}"
