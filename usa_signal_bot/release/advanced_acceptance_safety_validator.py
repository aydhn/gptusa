from typing import Any, Dict, List, Optional


from usa_signal_bot.release.phase159_models import (
    AdvancedAcceptanceContext,
    AdvancedDryRunStep,
    ReleaseCandidateAudit,
    FinalFreezeCertificate,
    Phase160HandoffPackage,
    Phase160ReadinessGate,
    AdvancedAcceptanceRiskFlag
)
from usa_signal_bot.release.advanced_acceptance_input_resolver import detect_forbidden_advanced_acceptance_fields

def validate_advanced_acceptance_context_safety(context: AdvancedAcceptanceContext) -> List[str]:
    errors = []
    if context.live_trading_enabled:
        errors.append("live_trading_enabled must be False")
    if context.paper_trading_enabled:
        errors.append("paper_trading_enabled must be False")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled must be False")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled must be False")
    if context.real_order_creation_enabled:
        errors.append("real_order_creation_enabled must be False")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled must be False")
    if context.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be False")
    if context.deployment_allowed:
        errors.append("deployment_allowed must be False")
    if context.production_patch_allowed:
        errors.append("production_patch_allowed must be False")
    if context.network_used:
        errors.append("network_used must be False")
    if context.paid_api_used:
        errors.append("paid_api_used must be False")
    if context.scraping_used:
        errors.append("scraping_used must be False")
    if context.html_parsing_used:
        errors.append("html_parsing_used must be False")
    if context.dashboard_started:
        errors.append("dashboard_started must be False")
    if context.daemon_started:
        errors.append("daemon_started must be False")
    if context.scheduler_enabled:
        errors.append("scheduler_enabled must be False")
    if context.actual_target_weights_produced:
        errors.append("actual_target_weights_produced must be False")
    if context.actual_allocation_produced:
        errors.append("actual_allocation_produced must be False")
    if context.order_size_produced:
        errors.append("order_size_produced must be False")
    if context.capital_deployment_allowed:
        errors.append("capital_deployment_allowed must be False")
    if context.investment_advice:
        errors.append("investment_advice must be False")
    return errors

def validate_advanced_dry_run_steps_safety(items: List[AdvancedDryRunStep]) -> List[str]:
    errors = []
    for s in items:
        if s.executed_real_side_effect:
            errors.append(f"Step {s.step_id} executed_real_side_effect")
        if s.used_network:
            errors.append(f"Step {s.step_id} used_network")
        if s.mutated_paper_state:
            errors.append(f"Step {s.step_id} mutated_paper_state")
        if s.used_broker:
            errors.append(f"Step {s.step_id} used_broker")
        if s.created_order:
            errors.append(f"Step {s.step_id} created_order")
        if s.sent_telegram:
            errors.append(f"Step {s.step_id} sent_telegram")
        if s.deployed:
            errors.append(f"Step {s.step_id} deployed")
        if s.production_patch_applied:
            errors.append(f"Step {s.step_id} production_patch_applied")
    return errors

def validate_release_candidate_audit_safety(audit: ReleaseCandidateAudit) -> List[str]:
    errors = []
    if not audit.not_deployment_approval:
        errors.append("not_deployment_approval must be True")
    if not audit.not_trading_approval:
        errors.append("not_trading_approval must be True")
    if not audit.not_investment_advice:
        errors.append("not_investment_advice must be True")
    return errors

def validate_final_freeze_certificate_safety(certificate: FinalFreezeCertificate) -> List[str]:
    errors = []
    if not certificate.not_deployment_approval:
        errors.append("not_deployment_approval must be True")
    if not certificate.not_trading_approval:
        errors.append("not_trading_approval must be True")
    if not certificate.not_investment_advice:
        errors.append("not_investment_advice must be True")
    return errors

def validate_phase160_handoff_package_safety(package: Phase160HandoffPackage) -> List[str]:
    errors = []
    if not package.read_only:
        errors.append("read_only must be True")
    if not package.final_delivery_handoff_only:
        errors.append("final_delivery_handoff_only must be True")
    if package.live_trading_enabled:
        errors.append("live_trading_enabled must be False")
    return errors

def validate_phase160_readiness_gate_safety(gate: Phase160ReadinessGate) -> List[str]:
    errors = []
    if not gate.dry_run_only:
        errors.append("dry_run_only must be True")
    if gate.live_trading_enabled:
        errors.append("live_trading_enabled must be False")
    return errors

def validate_advanced_acceptance_dataframe_output_safety(df: Any) -> List[str]:
    from usa_signal_bot.release.advanced_acceptance_schema_validator import validate_no_forbidden_advanced_acceptance_columns
    return validate_no_forbidden_advanced_acceptance_columns(df.columns.tolist())

def advanced_acceptance_text_has_trade_or_execution_language(text: str) -> bool:
    forbidden_terms = [
        "broker_order", "live_order", "sent_to_broker", "strategy_active",
        "deployment_enabled", "live_signal", "target_weight",
        "portfolio_weight", "actual_target_weight", "actual_allocation",
        "capital_allocation", "position_size", "real_order"
    ]
    text_lower = text.lower()
    for term in forbidden_terms:
        if term in text_lower:
            return True
    return False

def advanced_acceptance_payload_has_forbidden_fields(payload: Dict[str, Any]) -> bool:
    forbidden = detect_forbidden_advanced_acceptance_fields(payload)
    return len(forbidden) > 0

def collect_advanced_acceptance_risk_flags(context: Optional[AdvancedAcceptanceContext] = None) -> List[AdvancedAcceptanceRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
        if context.risk_register:
            flags.extend(context.risk_register.risk_flags)
        if context.release_candidate_audit:
            flags.extend(context.release_candidate_audit.risk_flags)
        if context.final_freeze_certificate:
            flags.extend(context.final_freeze_certificate.risk_flags)
        if context.phase160_handoff_package:
            flags.extend(context.phase160_handoff_package.risk_flags)
        if context.phase160_readiness_gate:
            flags.extend(context.phase160_readiness_gate.risk_flags)
    return list(set(flags))

def advanced_acceptance_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def advanced_acceptance_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Safety Validation: PASSED"
    lines = ["Safety Validation: FAILED"]
    for e in errors:
        lines.append(f" - {e}")
    return "\n".join(lines)
