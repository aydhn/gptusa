from typing import Any, Dict, List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    Phase158ReadinessGate,
    Phase158ReadinessRule,
    PortfolioBandFinalReview,
    PortfolioBandClosureCertificate,
    Phase158HandoffPackage,
    PortfolioRiskSafetyBoundaryResult,
    create_phase158_readiness_gate_id,
    create_phase158_readiness_rule_id
)
from usa_signal_bot.core.enums import Phase158ReadinessStatus, Phase158ReadinessRuleKind

def build_phase158_readiness_rules(final_review: PortfolioBandFinalReview, certificate: PortfolioBandClosureCertificate, handoff_package: Phase158HandoffPackage, boundary: PortfolioRiskSafetyBoundaryResult) -> List[Phase158ReadinessRule]:
    rules = []

    passed = boundary.boundary_passed and final_review.final_review_passed
    rules.append(Phase158ReadinessRule(
        rule_id=create_phase158_readiness_rule_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        rule_kind=Phase158ReadinessRuleKind.READY_FOR_PHASE158,
        name="Ready for Phase 158",
        status=Phase158ReadinessStatus.PASSED if passed else Phase158ReadinessStatus.BLOCKED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale="Final review and boundary checks must pass.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))
    return rules

def build_phase158_readiness_gate(final_review: PortfolioBandFinalReview, certificate: PortfolioBandClosureCertificate, handoff_package: Phase158HandoffPackage, boundary: PortfolioRiskSafetyBoundaryResult) -> Phase158ReadinessGate:
    rules = build_phase158_readiness_rules(final_review, certificate, handoff_package, boundary)
    ready = all(r.passed for r in rules if r.required)

    return Phase158ReadinessGate(
        gate_id=create_phase158_readiness_gate_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=Phase158ReadinessStatus.PASSED if ready else Phase158ReadinessStatus.BLOCKED,
        rules=rules,
        final_review=final_review,
        closure_certificate=certificate,
        handoff_package=handoff_package,
        safety_boundary=boundary,
        ready_for_phase158=ready,
        research_data_only=True,
        integration_handoff_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        actual_target_weights_produced=False,
        actual_allocation_produced=False,
        actual_position_size_produced=False,
        order_size_produced=False,
        capital_deployment_allowed=False,
        deployment_allowed=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def phase158_readiness_passed(gate: Phase158ReadinessGate) -> bool:
    return gate.status == Phase158ReadinessStatus.PASSED

def phase158_readiness_blocks_next_phase(gate: Phase158ReadinessGate) -> bool:
    return not phase158_readiness_passed(gate)

def validate_phase158_readiness_gate(gate: Phase158ReadinessGate) -> List[str]:
    return []

def phase158_readiness_gate_to_text(gate: Phase158ReadinessGate, limit: int = 300) -> str:
    return f"Readiness Gate {gate.gate_id}: ready={gate.ready_for_phase158}"
