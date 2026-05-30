from typing import Any
from usa_signal_bot.core.enums import RegimeContextAcceptanceRuleKind, RegimeContextAcceptanceStatus
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeAlignmentIngestionResult,
    CompatibilityValidationResult,
    ConditionalDiagnosticResult,
    ConditionalDiagnosticsProfile,
    RegimeContextAcceptanceRule,
    RegimeAwareAcceptanceGate,
    create_regime_context_acceptance_rule_id,
    create_regime_aware_acceptance_gate_id,
    _now_utc
)

def build_regime_context_acceptance_rules(
    ingestion: RegimeAlignmentIngestionResult,
    validation: CompatibilityValidationResult,
    diagnostics: list[ConditionalDiagnosticResult],
    profiles: list[ConditionalDiagnosticsProfile]
) -> list[RegimeContextAcceptanceRule]:
    rules = []

    def _make_rule(kind: RegimeContextAcceptanceRuleKind, passed: bool, rationale: str) -> RegimeContextAcceptanceRule:
        return RegimeContextAcceptanceRule(
            rule_id=create_regime_context_acceptance_rule_id(),
            created_at_utc=_now_utc(),
            rule_kind=kind,
            name=kind.value,
            status=RegimeContextAcceptanceStatus.ACCEPTED if passed else RegimeContextAcceptanceStatus.REJECTED,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=rationale,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.ALIGNMENT_VALID,
        ingestion.valid_for_phase132,
        "Ingestion must be valid"
    ))

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.COMPATIBILITY_VALIDATION_PASSED,
        validation.validation_passed,
        "Compatibility validation must pass"
    ))

    diag_errs = [d for d in diagnostics if d.recommended_action_type not in ["research_review", "data_quality_review", "documentation_review", "monitor_context", "none"]]
    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.CONDITIONAL_DIAGNOSTICS_VALID,
        len(diag_errs) == 0,
        "Diagnostics must only contain valid action types"
    ))

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.LOW_COMPATIBILITY_WITH_EXPLANATION_ALLOWED,
        validation.low_compatibility_count == validation.explained_low_compatibility_count,
        "Low comp must be explained"
    ))

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.UNCERTAIN_CONTEXT_WITH_EXPLANATION_ALLOWED,
        validation.uncertain_count == validation.explained_uncertain_count,
        "Uncertain context must be explained"
    ))

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.CONFLICTED_CONTEXT_REVIEWED,
        validation.conflicted_count == validation.explained_conflicted_count,
        "Conflicted context must be explained"
    ))

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.DATA_QUALITY_LIMITS_DOCUMENTED,
        validation.data_quality_limited_count == validation.explained_data_quality_limited_count,
        "Data quality limits must be explained"
    ))

    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.CROSS_SYMBOL_VALIDATION_ACCEPTABLE,
        all(p.blocking_count == 0 for p in profiles),
        "No blocking cross symbol diagnostics"
    ))

    # Safety
    rules.append(_make_rule(RegimeContextAcceptanceRuleKind.NO_SIGNAL_OUTPUT, not ingestion.produces_trade_signal, "Safe"))
    rules.append(_make_rule(RegimeContextAcceptanceRuleKind.NO_ORDER_OUTPUT, not ingestion.produces_order_decision, "Safe"))
    rules.append(_make_rule(RegimeContextAcceptanceRuleKind.NO_PORTFOLIO_OUTPUT, not ingestion.produces_portfolio_weights, "Safe"))
    rules.append(_make_rule(RegimeContextAcceptanceRuleKind.NO_EXECUTION_OUTPUT, not (ingestion.activation_allowed or ingestion.broker_execution_enabled), "Safe"))
    rules.append(_make_rule(RegimeContextAcceptanceRuleKind.NO_MODEL_TRAINING, not (ingestion.model_training_used or ingestion.model_prediction_used), "Safe"))

    all_passed = all(r.passed for r in rules)
    rules.append(_make_rule(
        RegimeContextAcceptanceRuleKind.READY_FOR_PHASE133,
        all_passed,
        "All rules passed"
    ))

    return rules

def build_regime_aware_acceptance_gate(
    ingestion: RegimeAlignmentIngestionResult,
    validation: CompatibilityValidationResult,
    diagnostics: list[ConditionalDiagnosticResult],
    profiles: list[ConditionalDiagnosticsProfile]
) -> RegimeAwareAcceptanceGate:
    rules = build_regime_context_acceptance_rules(ingestion, validation, diagnostics, profiles)
    all_passed = all(r.passed for r in rules)

    return RegimeAwareAcceptanceGate(
        gate_id=create_regime_aware_acceptance_gate_id(),
        created_at_utc=_now_utc(),
        status=RegimeContextAcceptanceStatus.ACCEPTED if all_passed else RegimeContextAcceptanceStatus.REJECTED,
        rules=rules,
        compatibility_validation=validation,
        conditional_diagnostics=diagnostics,
        diagnostics_profiles=profiles,
        ready_for_phase133=all_passed,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=list(validation.risk_flags),
        metadata={}
    )

def regime_context_acceptance_passed(gate: RegimeAwareAcceptanceGate) -> bool:
    return gate.status in [RegimeContextAcceptanceStatus.ACCEPTED, RegimeContextAcceptanceStatus.WARNING_ACCEPTED]

def regime_context_acceptance_blocks_phase133(gate: RegimeAwareAcceptanceGate) -> bool:
    return not gate.ready_for_phase133

def validate_regime_aware_acceptance_gate(gate: RegimeAwareAcceptanceGate) -> list[str]:
    errors = []
    if not gate.research_data_only:
        errors.append("Must be research data only")
    if gate.produces_trade_signal or gate.produces_order_decision or gate.produces_portfolio_weights:
        errors.append("Cannot produce execution outputs")
    if gate.activation_allowed or gate.strategy_activation_allowed or gate.deployment_allowed:
        errors.append("Cannot allow deployment/activation")
    return errors

def regime_acceptance_gate_summary(gate: RegimeAwareAcceptanceGate) -> dict[str, Any]:
    return {"passed": regime_context_acceptance_passed(gate), "ready_for_phase133": gate.ready_for_phase133}

def regime_acceptance_gate_to_text(gate: RegimeAwareAcceptanceGate, limit: int = 300) -> str:
    s = regime_acceptance_gate_summary(gate)
    return f"Acceptance Gate Passed: {s['passed']}, Ready for Phase 133: {s['ready_for_phase133']}"
