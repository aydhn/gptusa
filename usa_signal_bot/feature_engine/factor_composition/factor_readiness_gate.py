from typing import Any
from usa_signal_bot.core.enums import FactorReadinessStatus
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    FactorCandidateDefinition,
    FeatureSelectionMetadata,
    FactorReadinessGate,
    create_factor_readiness_gate_id,
    validate_factor_readiness_gate,
    _now_str
)
from usa_signal_bot.feature_engine.factor_composition.factor_readiness_rules import build_factor_readiness_rules

def factor_readiness_gate_passed(gate: FactorReadinessGate) -> bool:
    return gate.status == FactorReadinessStatus.PASSED

def factor_readiness_gate_blocks_phase121(gate: FactorReadinessGate) -> bool:
    return not factor_readiness_gate_passed(gate)

def build_factor_readiness_gate(groups: list[FeatureGroupDefinition], candidates: list[FactorCandidateDefinition], selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessGate:
    rules = build_factor_readiness_rules(groups, candidates, selection_metadata)

    passed = all(r.passed for r in rules if r.required)
    status = FactorReadinessStatus.PASSED if passed else FactorReadinessStatus.FAILED

    gate = FactorReadinessGate(
        gate_id=create_factor_readiness_gate_id(),
        created_at_utc=_now_str(),
        status=status,
        rules=rules,
        factor_candidates=candidates,
        feature_groups=groups,
        selection_metadata_count=len(selection_metadata),
        ready_for_phase121=passed,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False
    )

    validate_factor_readiness_gate(gate)
    return gate

def factor_readiness_gate_summary(gate: FactorReadinessGate) -> dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status.value,
        "ready_for_phase121": gate.ready_for_phase121,
        "rule_count": len(gate.rules),
        "rules_passed": len([r for r in gate.rules if r.passed])
    }

def factor_readiness_gate_to_text(gate: FactorReadinessGate, limit: int = 300) -> str:
    summary = factor_readiness_gate_summary(gate)
    lines = [
        f"Factor Readiness Gate: {gate.gate_id}",
        f"Status: {summary['status']}",
        f"Ready for Phase 121: {summary['ready_for_phase121']}",
        f"Rules passed: {summary['rules_passed']} / {summary['rule_count']}"
    ]
    return "\n".join(lines)
