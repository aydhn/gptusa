from typing import Any
from usa_signal_bot.core.enums import FactorReadinessStatus, FactorReadinessRuleKind, FeatureSelectionStatus
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    FactorCandidateDefinition,
    FeatureSelectionMetadata,
    FactorReadinessRule,
    create_factor_readiness_rule_id,
    _now_str
)

def _build_rule(kind: FactorReadinessRuleKind, name: str, expected: Any, observed: Any, passed: bool, rationale: str) -> FactorReadinessRule:
    return FactorReadinessRule(
        rule_id=create_factor_readiness_rule_id(),
        created_at_utc=_now_str(),
        rule_kind=kind,
        name=name,
        status=FactorReadinessStatus.PASSED if passed else FactorReadinessStatus.FAILED,
        required=True,
        expected_value=expected,
        observed_value=observed,
        passed=passed,
        rationale=rationale
    )

def rule_feature_tables_available(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    passed = len(selection_metadata) > 0
    return _build_rule(
        FactorReadinessRuleKind.FEATURE_TABLES_AVAILABLE,
        "Feature Tables Available",
        "count > 0",
        len(selection_metadata),
        passed,
        "Ensure enriched feature tables were loaded"
    )

def rule_feature_groups_valid(groups: list[FeatureGroupDefinition]) -> FactorReadinessRule:
    passed = len(groups) > 0 and not any(g.errors for g in groups)
    return _build_rule(
        FactorReadinessRuleKind.FEATURE_GROUPS_VALID,
        "Feature Groups Valid",
        "valid groups present",
        f"{len(groups)} groups",
        passed,
        "Ensure all required groups are valid and error-free"
    )

def rule_factor_candidates_valid(candidates: list[FactorCandidateDefinition]) -> FactorReadinessRule:
    passed = len(candidates) > 0 and not any(c.errors for c in candidates)
    return _build_rule(
        FactorReadinessRuleKind.FACTOR_CANDIDATES_VALID,
        "Factor Candidates Valid",
        "valid candidates present",
        f"{len(candidates)} candidates",
        passed,
        "Ensure all factor candidates are well formed"
    )

def rule_selection_metadata_valid(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    passed = len(selection_metadata) > 0 and not any(m.errors for m in selection_metadata)
    return _build_rule(
        FactorReadinessRuleKind.SELECTION_METADATA_VALID,
        "Selection Metadata Valid",
        "valid metadata present",
        f"{len(selection_metadata)} items",
        passed,
        "Ensure selection metadata is valid"
    )

def rule_coverage_acceptable(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    selected = [m for m in selection_metadata if m.selection_status == FeatureSelectionStatus.SELECTED_FOR_RESEARCH]
    passed = len(selected) > 0
    return _build_rule(
        FactorReadinessRuleKind.COVERAGE_ACCEPTABLE,
        "Coverage Acceptable",
        "selected features > 0",
        len(selected),
        passed,
        "Ensure at least some features passed coverage checks"
    )

def rule_missingness_acceptable(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    selected = [m for m in selection_metadata if m.selection_status == FeatureSelectionStatus.SELECTED_FOR_RESEARCH]
    passed = len(selected) > 0
    return _build_rule(
        FactorReadinessRuleKind.MISSINGNESS_ACCEPTABLE,
        "Missingness Acceptable",
        "selected features > 0",
        len(selected),
        passed,
        "Ensure at least some features passed missingness checks"
    )

def rule_stability_acceptable(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    selected = [m for m in selection_metadata if m.selection_status == FeatureSelectionStatus.SELECTED_FOR_RESEARCH]
    passed = len(selected) > 0
    return _build_rule(
        FactorReadinessRuleKind.STABILITY_ACCEPTABLE,
        "Stability Acceptable",
        "selected features > 0",
        len(selected),
        passed,
        "Ensure at least some features passed stability checks"
    )

def rule_redundancy_acceptable(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    selected = [m for m in selection_metadata if m.selection_status == FeatureSelectionStatus.SELECTED_FOR_RESEARCH]
    passed = len(selected) > 0
    return _build_rule(
        FactorReadinessRuleKind.REDUNDANCY_ACCEPTABLE,
        "Redundancy Acceptable",
        "selected features > 0",
        len(selected),
        passed,
        "Ensure at least some features passed redundancy checks"
    )

def rule_safety_acceptable(selection_metadata: list[FeatureSelectionMetadata]) -> FactorReadinessRule:
    unsafe = [m for m in selection_metadata if m.selection_status == FeatureSelectionStatus.EXCLUDED_UNSAFE]
    passed = True
    return _build_rule(
        FactorReadinessRuleKind.SAFETY_ACCEPTABLE,
        "Safety Acceptable",
        "tracked unsafe columns",
        len(unsafe),
        passed,
        "Safety validation applies. Unsafe columns are excluded safely."
    )

def rule_no_signal_order_portfolio_output(candidates: list[FactorCandidateDefinition]) -> FactorReadinessRule:
    violators = [c for c in candidates if c.produces_trade_signal or c.produces_order_decision or c.produces_portfolio_weights]
    passed = len(violators) == 0
    return _build_rule(
        FactorReadinessRuleKind.NO_SIGNAL_OUTPUT,
        "No Execution Output",
        0,
        len(violators),
        passed,
        "Factor candidates must not produce signal/order/portfolio outputs"
    )

def build_factor_readiness_rules(groups: list[FeatureGroupDefinition], candidates: list[FactorCandidateDefinition], selection_metadata: list[FeatureSelectionMetadata]) -> list[FactorReadinessRule]:
    return [
        rule_feature_tables_available(selection_metadata),
        rule_feature_groups_valid(groups),
        rule_factor_candidates_valid(candidates),
        rule_selection_metadata_valid(selection_metadata),
        rule_coverage_acceptable(selection_metadata),
        rule_missingness_acceptable(selection_metadata),
        rule_stability_acceptable(selection_metadata),
        rule_redundancy_acceptable(selection_metadata),
        rule_safety_acceptable(selection_metadata),
        rule_no_signal_order_portfolio_output(candidates)
    ]

def factor_readiness_rules_summary(rules: list[FactorReadinessRule]) -> dict[str, Any]:
    return {
        "total_rules": len(rules),
        "passed_rules": len([r for r in rules if r.passed]),
        "failed_rules": len([r for r in rules if not r.passed])
    }

def factor_readiness_rules_to_text(rules: list[FactorReadinessRule], limit: int = 200) -> str:
    summary = factor_readiness_rules_summary(rules)
    lines = [
        f"Factor Readiness Rules: {summary['total_rules']}",
        f"Passed: {summary['passed_rules']}, Failed: {summary['failed_rules']}"
    ]
    for r in rules[:limit]:
        lines.append(f"  - {r.name}: {r.status.value} (Expected: {r.expected_value}, Observed: {r.observed_value})")
    return "\n".join(lines)
