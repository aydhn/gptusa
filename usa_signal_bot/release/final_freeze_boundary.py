from typing import Any, Dict, List, Optional
from usa_signal_bot.release.phase159_models import (
    FinalFreezeBoundaryResult,
    FinalFreezeBoundaryRule,
    AdvancedAcceptanceSafetyRuleKind,
    create_final_freeze_boundary_result_id,
    create_final_freeze_boundary_rule_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_final_freeze_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[FinalFreezeBoundaryRule]:
    # Mock reading values from context
    def safe_get(key: str, default: bool) -> bool:
        if not context_payload:
            return default
        return context_payload.get(key, default)

    rules_def = [
        (AdvancedAcceptanceSafetyRuleKind.ADVANCED_ACCEPTANCE_ONLY, "advanced_acceptance_only", True, True),
        (AdvancedAcceptanceSafetyRuleKind.READ_ONLY_PHASE158_REVIEW, "read_only_phase158_review", True, True),
        (AdvancedAcceptanceSafetyRuleKind.DRY_RUN_ONLY, "dry_run_only", True, True),
        (AdvancedAcceptanceSafetyRuleKind.LOCAL_FIXTURE_ONLY, "local_fixture_only", True, True),
        (AdvancedAcceptanceSafetyRuleKind.NO_LIVE_TRADING, "live_trading_enabled", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_PAPER_STATE_MUTATION, "paper_state_mutation_enabled", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_BROKER_EXECUTION, "broker_execution_enabled", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_REAL_ORDER_CREATION, "real_order_creation_enabled", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_TELEGRAM_REAL_SEND, "telegram_real_send_enabled", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_STRATEGY_ACTIVATION, "strategy_activation_allowed", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_DEPLOYMENT, "deployment_allowed", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_PRODUCTION_PATCH, "production_patch_allowed", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_NETWORK, "network_used", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_SCRAPING, "scraping_used", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_HTML_PARSING, "html_parsing_used", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_DASHBOARD, "dashboard_started", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_DAEMON, "daemon_started", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_SCHEDULER, "scheduler_enabled", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_ACTUAL_TARGET_WEIGHTS, "actual_target_weights_produced", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_ACTUAL_ALLOCATION, "actual_allocation_produced", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_ORDER_SIZE, "order_size_produced", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_CAPITAL_DEPLOYMENT, "capital_deployment_allowed", False, False),
        (AdvancedAcceptanceSafetyRuleKind.NO_INVESTMENT_ADVICE, "investment_advice", False, False),
        (AdvancedAcceptanceSafetyRuleKind.RESEARCH_DATA_ONLY, "research_data_only", True, True)
    ]

    rules = []
    for kind, key, expected, default_val in rules_def:
        observed = safe_get(key, default_val)
        passed = observed == expected
        rules.append(FinalFreezeBoundaryRule(
            rule_id=create_final_freeze_boundary_rule_id(),
            created_at_utc=generate_timestamp(),
            rule_kind=kind,
            name=key,
            required=True,
            passed=passed,
            expected_value=expected,
            observed_value=observed,
            rationale=f"Checking {key} == {expected}",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_final_freeze_boundary_result(rules: List[FinalFreezeBoundaryRule]) -> FinalFreezeBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    def _get(key):
        for r in rules:
            if r.name == key:
                return r.observed_value
        return False

    res = FinalFreezeBoundaryResult(
        boundary_id=create_final_freeze_boundary_result_id(),
        created_at_utc=generate_timestamp(),
        rules=rules,
        boundary_passed=passed,
        advanced_acceptance_only=_get("advanced_acceptance_only"),
        read_only_phase158_review=_get("read_only_phase158_review"),
        dry_run_only=_get("dry_run_only"),
        local_fixture_only=_get("local_fixture_only"),
        no_live_trading=not _get("live_trading_enabled"),
        no_paper_state_mutation=not _get("paper_state_mutation_enabled"),
        no_broker_execution=not _get("broker_execution_enabled"),
        no_real_order_creation=not _get("real_order_creation_enabled"),
        no_telegram_real_send=not _get("telegram_real_send_enabled"),
        no_strategy_activation=not _get("strategy_activation_allowed"),
        no_deployment=not _get("deployment_allowed"),
        no_production_patch=not _get("production_patch_allowed"),
        no_network=not _get("network_used"),
        no_scraping=not _get("scraping_used"),
        no_html_parsing=not _get("html_parsing_used"),
        no_dashboard=not _get("dashboard_started"),
        no_daemon=not _get("daemon_started"),
        no_scheduler=not _get("scheduler_enabled"),
        no_actual_target_weights=not _get("actual_target_weights_produced"),
        no_actual_allocation=not _get("actual_allocation_produced"),
        no_order_size=not _get("order_size_produced"),
        no_capital_deployment=not _get("capital_deployment_allowed"),
        no_investment_advice=not _get("investment_advice"),
        research_data_only=_get("research_data_only"),
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if not passed:
        res.risk_flags.append(AdvancedAcceptanceRiskFlag.FINAL_FREEZE_BOUNDARY_FAILED)

    return res

def validate_final_freeze_boundary_result(result: FinalFreezeBoundaryResult) -> List[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Boundary failed")
    for r in result.rules:
        if r.required and not r.passed:
            errors.append(f"Boundary rule failed: {r.name}")
    return errors

def final_freeze_boundary_passed(result: FinalFreezeBoundaryResult) -> bool:
    return result.boundary_passed

def final_freeze_boundary_to_text(result: FinalFreezeBoundaryResult, limit: int = 300) -> str:
    lines = [f"Freeze Boundary Passed: {result.boundary_passed}"]
    for r in result.rules[:limit]:
        lines.append(f" - [{ 'x' if r.passed else ' ' }] {r.name}: {r.observed_value} (Expected {r.expected_value})")
    return "\n".join(lines)
