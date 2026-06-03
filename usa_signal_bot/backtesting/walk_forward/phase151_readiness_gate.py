from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import Phase151ReadinessStatus, Phase151ReadinessRuleKind, WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardValidationReport,
    TemporalStabilityAuditReport,
    WalkForwardSafetyBoundaryResult,
    Phase151ReadinessRule,
    Phase151ReadinessGate,
    create_phase151_readiness_rule_id,
    create_phase151_readiness_gate_id,
    _now_utc
)

def _build_rule(kind: Phase151ReadinessRuleKind, passed: bool) -> Phase151ReadinessRule:
    return Phase151ReadinessRule(
        rule_id=create_phase151_readiness_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=kind,
        name=kind.value,
        status=Phase151ReadinessStatus.PASSED if passed else Phase151ReadinessStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale=f"Checking {kind.value}"
    )

def build_phase151_readiness_rules(
    validation_report: WalkForwardValidationReport,
    audit: TemporalStabilityAuditReport,
    boundary: WalkForwardSafetyBoundaryResult
) -> List[Phase151ReadinessRule]:
    return [
        _build_rule(Phase151ReadinessRuleKind.WALK_FORWARD_VALIDATION_REPORT_VALID, validation_report.report_valid),
        _build_rule(Phase151ReadinessRuleKind.TEMPORAL_STABILITY_AUDIT_VALID, audit.audit_passed),
        _build_rule(Phase151ReadinessRuleKind.SAFETY_BOUNDARY_VALID, boundary.boundary_passed),
        _build_rule(Phase151ReadinessRuleKind.NO_REAL_ORDER_OUTPUT, boundary.no_real_order_creation),
        _build_rule(Phase151ReadinessRuleKind.NO_PAPER_MUTATION, boundary.no_paper_state_mutation),
        _build_rule(Phase151ReadinessRuleKind.NO_LIVE_TRADING, boundary.no_live_trading),
        _build_rule(Phase151ReadinessRuleKind.NO_STRESS_MONTE_CARLO_YET, boundary.no_stress_test_phase150 and boundary.no_monte_carlo_phase150)
    ]

def build_phase151_readiness_gate(
    validation_report: WalkForwardValidationReport,
    audit: TemporalStabilityAuditReport,
    boundary: WalkForwardSafetyBoundaryResult
) -> Phase151ReadinessGate:
    rules = build_phase151_readiness_rules(validation_report, audit, boundary)
    passed = all(r.passed for r in rules if r.required)
    status = Phase151ReadinessStatus.PASSED if passed else Phase151ReadinessStatus.FAILED

    gate = Phase151ReadinessGate(
        gate_id=create_phase151_readiness_gate_id(),
        created_at_utc=_now_utc(),
        status=status,
        rules=rules,
        validation_report=validation_report,
        temporal_stability_audit=audit,
        safety_boundary=boundary,
        ready_for_phase151=passed,
        research_data_only=True,
        offline_backtest_research_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        walk_forward_executed=True,
        stress_test_executed=False,
        monte_carlo_executed=False,
        deployment_allowed=False,
        investment_advice=False
    )

    errors = validate_phase151_readiness_gate(gate)
    if errors:
        gate.ready_for_phase151 = False
        gate.status = Phase151ReadinessStatus.BLOCKED
        gate.errors = errors
        gate.risk_flags.append(WalkForwardRiskFlag.PHASE150_READINESS_GATE_FAILED)

    return gate

def phase151_readiness_passed(gate: Phase151ReadinessGate) -> bool:
    return gate.ready_for_phase151

def phase151_readiness_blocks_next_phase(gate: Phase151ReadinessGate) -> bool:
    return not gate.ready_for_phase151

def validate_phase151_readiness_gate(gate: Phase151ReadinessGate) -> List[str]:
    errors = []
    if not gate.safety_boundary.boundary_passed and gate.ready_for_phase151:
        errors.append("ready_for_phase151 cannot be True if safety boundary failed")
    failed_rules = [r.name for r in gate.rules if r.required and not r.passed]
    if failed_rules:
        errors.append(f"Phase 151 readiness gate failed rules: {failed_rules}")
    return errors

def phase151_readiness_gate_summary(gate: Phase151ReadinessGate) -> Dict[str, Any]:
    return {
        "status": gate.status.value,
        "ready": gate.ready_for_phase151,
        "failed_rules": sum(1 for r in gate.rules if not r.passed)
    }

def phase151_readiness_gate_to_text(gate: Phase151ReadinessGate, limit: int = 300) -> str:
    summary = phase151_readiness_gate_summary(gate)
    lines = [
        f"Phase 151 Readiness Gate:",
        f"  Status: {summary['status']}",
        f"  Ready for Phase 151: {summary['ready']}"
    ]
    return "\n".join(lines)[:limit]
