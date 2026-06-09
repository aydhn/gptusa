from typing import List, Dict, Any, Optional
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalSafetyBoundaryResult,
    FinalSafetyBoundaryRule,
    FinalSafetyRuleKind,
    FinalClosureRiskFlag,
    create_final_safety_boundary_rule_id,
    create_final_safety_boundary_result_id,
    generate_timestamp
)

def build_final_safety_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[FinalSafetyBoundaryRule]:
    # In a real environment, this validates against actual environment flags.
    # We default to safe mock data.
    unsafe = context_payload and context_payload.get("unsafe", False)

    rules = []

    kinds = [
        FinalSafetyRuleKind.FINAL_AUDIT_ONLY,
        FinalSafetyRuleKind.READ_ONLY_PHASE160_HANDOFF,
        FinalSafetyRuleKind.NO_LIVE_TRADING,
        FinalSafetyRuleKind.NO_PAPER_STATE_MUTATION,
        FinalSafetyRuleKind.NO_BROKER_EXECUTION,
        FinalSafetyRuleKind.NO_REAL_ORDER_CREATION,
        FinalSafetyRuleKind.NO_TELEGRAM_REAL_SEND,
        FinalSafetyRuleKind.NO_STRATEGY_ACTIVATION,
        FinalSafetyRuleKind.NO_DEPLOYMENT,
        FinalSafetyRuleKind.NO_PRODUCTION_PATCH,
        FinalSafetyRuleKind.NO_NETWORK,
        FinalSafetyRuleKind.NO_SCRAPING,
        FinalSafetyRuleKind.NO_HTML_PARSING,
        FinalSafetyRuleKind.NO_DASHBOARD,
        FinalSafetyRuleKind.NO_DAEMON,
        FinalSafetyRuleKind.NO_SCHEDULER,
        FinalSafetyRuleKind.NO_ACTUAL_TARGET_WEIGHTS,
        FinalSafetyRuleKind.NO_ACTUAL_ALLOCATION,
        FinalSafetyRuleKind.NO_ORDER_SIZE,
        FinalSafetyRuleKind.NO_CAPITAL_DEPLOYMENT,
        FinalSafetyRuleKind.NO_INVESTMENT_ADVICE,
        FinalSafetyRuleKind.RESEARCH_DATA_ONLY,
        FinalSafetyRuleKind.PROJECT_CLOSURE_ONLY
    ]

    for kind in kinds:
        passed = not unsafe
        rules.append(FinalSafetyBoundaryRule(
            rule_id=create_final_safety_boundary_rule_id(),
            created_at_utc=generate_timestamp(),
            rule_kind=kind,
            name=f"Rule {kind.value}",
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale="Safety check",
            warnings=[],
            errors=["Failed safety boundary check"] if not passed else [],
            risk_flags=[FinalClosureRiskFlag.FINAL_SAFETY_BOUNDARY_FAILED] if not passed else [],
            metadata={}
        ))

    return rules

def build_final_safety_boundary_result(rules: List[FinalSafetyBoundaryRule]) -> FinalSafetyBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    errors = []
    risk_flags = []
    if not passed:
        errors.append("Safety boundary validation failed.")
        risk_flags.append(FinalClosureRiskFlag.FINAL_SAFETY_BOUNDARY_FAILED)

    return FinalSafetyBoundaryResult(
        boundary_id=create_final_safety_boundary_result_id(),
        created_at_utc=generate_timestamp(),
        rules=rules,
        boundary_passed=passed,
        final_audit_only=passed,
        read_only_phase160_handoff=passed,
        no_live_trading=passed,
        no_paper_state_mutation=passed,
        no_broker_execution=passed,
        no_real_order_creation=passed,
        no_telegram_real_send=passed,
        no_strategy_activation=passed,
        no_deployment=passed,
        no_production_patch=passed,
        no_network=passed,
        no_scraping=passed,
        no_html_parsing=passed,
        no_dashboard=passed,
        no_daemon=passed,
        no_scheduler=passed,
        no_actual_target_weights=passed,
        no_actual_allocation=passed,
        no_order_size=passed,
        no_capital_deployment=passed,
        no_investment_advice=passed,
        research_data_only=passed,
        project_closure_only=passed,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

def validate_final_safety_boundary_result(result: FinalSafetyBoundaryResult) -> List[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary failed.")
    return errors

def final_safety_boundary_passed(result: FinalSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def final_safety_boundary_to_text(result: FinalSafetyBoundaryResult, limit: int = 300) -> str:
    return f"Final Safety Boundary: Passed={result.boundary_passed}"
