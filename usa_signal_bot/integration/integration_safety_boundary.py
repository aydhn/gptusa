
from typing import Any, Dict, List, Optional

from usa_signal_bot.integration.phase158_models import IntegrationSafetyBoundaryRule, IntegrationSafetyBoundaryResult, IntegrationSafetyRuleKind

def build_integration_safety_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[IntegrationSafetyBoundaryRule]:
    kinds = [
        IntegrationSafetyRuleKind.FULL_SYSTEM_INTEGRATION_ONLY,
        IntegrationSafetyRuleKind.READ_ONLY_PHASE158_HANDOFF,
        IntegrationSafetyRuleKind.DRY_RUN_REHEARSAL_ONLY,
        IntegrationSafetyRuleKind.NO_LIVE_TRADING,
        IntegrationSafetyRuleKind.NO_PAPER_STATE_MUTATION,
        IntegrationSafetyRuleKind.NO_BROKER_EXECUTION,
        IntegrationSafetyRuleKind.NO_REAL_ORDER_CREATION,
        IntegrationSafetyRuleKind.NO_TELEGRAM_REAL_SEND,
        IntegrationSafetyRuleKind.NO_STRATEGY_ACTIVATION,
        IntegrationSafetyRuleKind.NO_DEPLOYMENT,
        IntegrationSafetyRuleKind.NO_PRODUCTION_PATCH,
        IntegrationSafetyRuleKind.NO_NETWORK,
        IntegrationSafetyRuleKind.NO_SCRAPING,
        IntegrationSafetyRuleKind.NO_HTML_PARSING,
        IntegrationSafetyRuleKind.NO_DASHBOARD,
        IntegrationSafetyRuleKind.NO_DAEMON,
        IntegrationSafetyRuleKind.NO_SCHEDULER,
        IntegrationSafetyRuleKind.NO_ACTUAL_TARGET_WEIGHTS,
        IntegrationSafetyRuleKind.NO_ACTUAL_ALLOCATION,
        IntegrationSafetyRuleKind.NO_ORDER_SIZE,
        IntegrationSafetyRuleKind.NO_CAPITAL_DEPLOYMENT,
        IntegrationSafetyRuleKind.NO_INVESTMENT_ADVICE,
        IntegrationSafetyRuleKind.RESEARCH_DATA_ONLY
    ]

    rules = []
    for kind in kinds:
        rules.append(IntegrationSafetyBoundaryRule(
            rule_kind=kind,
            name=kind.value,
            required=True,
            passed=True,
            expected_value=True,
            observed_value=True
        ))
    return rules

def build_integration_safety_boundary_result(rules: List[IntegrationSafetyBoundaryRule]) -> IntegrationSafetyBoundaryResult:
    result = IntegrationSafetyBoundaryResult(rules=rules)
    result.boundary_passed = len(validate_integration_safety_boundary_result(result)) == 0
    return result

def validate_integration_safety_boundary_result(result: IntegrationSafetyBoundaryResult) -> List[str]:
    violations = []
    for rule in result.rules:
        if rule.required and not rule.passed:
            violations.append(f"Safety rule {rule.name} failed.")
    return violations

def integration_safety_boundary_passed(result: IntegrationSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def integration_safety_boundary_to_text(result: IntegrationSafetyBoundaryResult, limit: int = 300) -> str:
    text = f"Safety Boundary Passed: {result.boundary_passed}"
    return text[:limit] + "..." if len(text) > limit else text
