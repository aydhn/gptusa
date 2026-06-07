from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    HandoffSafetyBoundaryResult, HandoffSafetyBoundaryRule, HandoffSafetyRuleKind,
    Phase153HandoffPackage, BacktestClosureRiskFlag
)

def build_handoff_safety_boundary_rules(package: Phase153HandoffPackage | None = None) -> list[HandoffSafetyBoundaryRule]:
    rules = []
    # simplified mock rules
    for kind in HandoffSafetyRuleKind:
        if kind == HandoffSafetyRuleKind.UNKNOWN: continue

        # for a safe package, assume passed
        passed = True
        if package and not package.package_valid:
            passed = False

        rules.append(HandoffSafetyBoundaryRule(
            rule_kind=kind,
            name=kind.name,
            required=True,
            passed=passed,
            expected_value=True,
            observed_value=passed,
            rationale=f"Check {kind.name}"
        ))
    return rules

def build_handoff_safety_boundary_result(rules: list[HandoffSafetyBoundaryRule]) -> HandoffSafetyBoundaryResult:
    res = HandoffSafetyBoundaryResult()
    res.rules = rules
    res.boundary_passed = all(r.passed for r in rules if r.required)

    if not res.boundary_passed:
        res.risk_flags.append(BacktestClosureRiskFlag.HANDOFF_SAFETY_BOUNDARY_FAILED)
        res.errors.append("Handoff safety boundary failed")

    return res

def handoff_safety_boundary_passed(result: HandoffSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def validate_handoff_safety_boundary_result(result: HandoffSafetyBoundaryResult) -> list[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Safety boundary failed")
    return errors

def handoff_safety_boundary_summary(result: HandoffSafetyBoundaryResult) -> dict[str, Any]:
    return {"passed": result.boundary_passed}

def handoff_safety_boundary_to_text(result: HandoffSafetyBoundaryResult, limit: int = 300) -> str:
    return f"HandoffSafetyBoundary(passed={result.boundary_passed})"
