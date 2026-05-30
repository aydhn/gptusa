from typing import Any
from usa_signal_bot.core.enums import CompatibilityValidationRuleKind, CompatibilityValidationStatus
from usa_signal_bot.regime_classification.validation.phase132_models import (
    CompatibilityValidationRule,
    create_compatibility_validation_rule_id,
    _now_utc
)

def build_validation_rule(
    rule_kind: CompatibilityValidationRuleKind,
    passed: bool,
    observed_value: Any | None = None,
    expected_value: Any | None = None,
    rationale: str = ""
) -> CompatibilityValidationRule:
    status = CompatibilityValidationStatus.PASS if passed else CompatibilityValidationStatus.FAIL
    return CompatibilityValidationRule(
        rule_id=create_compatibility_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=rule_kind,
        name=rule_kind.value,
        status=status,
        required=True,
        passed=passed,
        expected_value=expected_value,
        observed_value=observed_value,
        rationale=rationale,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_compatibility_validation_rules() -> list[CompatibilityValidationRule]:
    # Creates skeleton rules
    kinds = [
        CompatibilityValidationRuleKind.ALIGNMENT_REVIEW_VALID,
        CompatibilityValidationRuleKind.COMPATIBILITY_RESULTS_AVAILABLE,
        CompatibilityValidationRuleKind.COMPATIBILITY_SCORE_RANGE_VALID,
        CompatibilityValidationRuleKind.COMPATIBILITY_CLASSIFICATION_VALID,
        CompatibilityValidationRuleKind.OVERLAY_RESULTS_AVAILABLE,
        CompatibilityValidationRuleKind.OVERLAY_SCORE_RANGE_VALID,
        CompatibilityValidationRuleKind.DIAGNOSTICS_PROFILES_AVAILABLE,
        CompatibilityValidationRuleKind.LOW_COMPATIBILITY_EXPLAINED,
        CompatibilityValidationRuleKind.UNCERTAIN_CONTEXT_EXPLAINED,
        CompatibilityValidationRuleKind.CONFLICTED_CONTEXT_EXPLAINED,
        CompatibilityValidationRuleKind.DATA_QUALITY_LIMITED_CONTEXT_EXPLAINED,
        CompatibilityValidationRuleKind.NO_SIGNAL_OUTPUT,
        CompatibilityValidationRuleKind.NO_ORDER_OUTPUT,
        CompatibilityValidationRuleKind.NO_PORTFOLIO_OUTPUT,
        CompatibilityValidationRuleKind.NO_EXECUTION_OUTPUT,
        CompatibilityValidationRuleKind.NO_MODEL_TRAINING,
    ]
    return [
        build_validation_rule(k, False, rationale="Default rule pending execution")
        for k in kinds
    ]

def validate_compatibility_validation_rules(rules: list[CompatibilityValidationRule]) -> list[str]:
    errors = []
    kinds_present = {r.rule_kind for r in rules}
    required = {
        CompatibilityValidationRuleKind.ALIGNMENT_REVIEW_VALID,
        CompatibilityValidationRuleKind.COMPATIBILITY_RESULTS_AVAILABLE,
        CompatibilityValidationRuleKind.COMPATIBILITY_SCORE_RANGE_VALID,
        CompatibilityValidationRuleKind.COMPATIBILITY_CLASSIFICATION_VALID,
        CompatibilityValidationRuleKind.OVERLAY_RESULTS_AVAILABLE,
        CompatibilityValidationRuleKind.OVERLAY_SCORE_RANGE_VALID,
        CompatibilityValidationRuleKind.DIAGNOSTICS_PROFILES_AVAILABLE,
        CompatibilityValidationRuleKind.LOW_COMPATIBILITY_EXPLAINED,
        CompatibilityValidationRuleKind.UNCERTAIN_CONTEXT_EXPLAINED,
        CompatibilityValidationRuleKind.CONFLICTED_CONTEXT_EXPLAINED,
        CompatibilityValidationRuleKind.DATA_QUALITY_LIMITED_CONTEXT_EXPLAINED,
        CompatibilityValidationRuleKind.NO_SIGNAL_OUTPUT,
        CompatibilityValidationRuleKind.NO_ORDER_OUTPUT,
        CompatibilityValidationRuleKind.NO_PORTFOLIO_OUTPUT,
        CompatibilityValidationRuleKind.NO_EXECUTION_OUTPUT,
        CompatibilityValidationRuleKind.NO_MODEL_TRAINING,
    }
    missing = required - kinds_present
    if missing:
        errors.append(f"Missing required rules: {[m.value for m in missing]}")
    return errors

def compatibility_validation_specs_summary(rules: list[CompatibilityValidationRule]) -> dict[str, Any]:
    return {
        "total_rules": len(rules),
        "passed_rules": sum(1 for r in rules if r.passed),
        "failed_rules": sum(1 for r in rules if not r.passed),
    }

def compatibility_validation_specs_to_text(rules: list[CompatibilityValidationRule], limit: int = 200) -> str:
    summary = compatibility_validation_specs_summary(rules)
    return f"Specs: {summary['total_rules']} total, {summary['passed_rules']} passed."
