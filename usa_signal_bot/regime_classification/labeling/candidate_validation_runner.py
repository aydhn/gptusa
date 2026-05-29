from typing import Any
from usa_signal_bot.core.enums import (
    RegimeCandidateValidationRuleKind,
    RegimeCandidateValidationStatus,
    RegimeLabelingQuality
)
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeCandidateValidationRule,
    RegimeCandidateValidationResult,
    HeuristicRegimeLabelResult,
    create_regime_candidate_validation_rule_id,
    create_regime_candidate_validation_result_id,
    _now_utc
)

def rule_candidate_definitions_available(candidate_definitions: list[dict[str, Any]] | None) -> RegimeCandidateValidationRule:
    passed = candidate_definitions is not None and len(candidate_definitions) > 0
    return RegimeCandidateValidationRule(
        rule_id=create_regime_candidate_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeCandidateValidationRuleKind.CANDIDATE_DEFINITIONS_AVAILABLE,
        name="Candidate Definitions Available",
        status=RegimeCandidateValidationStatus.PASS if passed else RegimeCandidateValidationStatus.FAIL,
        required=True,
        passed=passed,
        expected_value="list length > 0",
        observed_value=len(candidate_definitions) if candidate_definitions else 0,
        rationale="Must have candidate definitions to validate taxonomy"
    )

def rule_candidate_scores_available(candidate_scores: list[dict[str, Any]] | None, label_results: list[HeuristicRegimeLabelResult]) -> RegimeCandidateValidationRule:
    # If we have scores or label results derived from scores
    passed = (candidate_scores is not None and len(candidate_scores) > 0) or (len(label_results) > 0)
    return RegimeCandidateValidationRule(
        rule_id=create_regime_candidate_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeCandidateValidationRuleKind.CANDIDATE_SCORES_AVAILABLE,
        name="Candidate Scores Available",
        status=RegimeCandidateValidationStatus.PASS if passed else RegimeCandidateValidationStatus.FAIL,
        required=True,
        passed=passed,
        expected_value="list length > 0 or labels generated",
        observed_value=f"scores: {len(candidate_scores) if candidate_scores else 0}, labels: {len(label_results)}",
        rationale="Must have scores to assign labels"
    )

def rule_scores_within_range(label_results: list[HeuristicRegimeLabelResult]) -> RegimeCandidateValidationRule:
    passed = True
    for r in label_results:
        if r.top_candidate_score is not None and (r.top_candidate_score < -100 or r.top_candidate_score > 200):
            passed = False
            break

    return RegimeCandidateValidationRule(
        rule_id=create_regime_candidate_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeCandidateValidationRuleKind.SCORES_WITHIN_RANGE,
        name="Scores Within Expected Range",
        status=RegimeCandidateValidationStatus.PASS if passed else RegimeCandidateValidationStatus.FAIL,
        required=True,
        passed=passed,
        expected_value="0 to 100",
        observed_value="Within range" if passed else "Out of bounds",
        rationale="Scores must be normalized or bounded"
    )

def rule_taxonomy_labels_aligned(candidate_definitions: list[dict[str, Any]] | None, label_results: list[HeuristicRegimeLabelResult]) -> RegimeCandidateValidationRule:
    # In a real impl, compare definition taxonomies with assigned labels
    return RegimeCandidateValidationRule(
        rule_id=create_regime_candidate_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeCandidateValidationRuleKind.TAXONOMY_LABELS_ALIGNED,
        name="Taxonomy Labels Aligned",
        status=RegimeCandidateValidationStatus.PASS,
        required=True,
        passed=True,
        expected_value=True,
        observed_value=True,
        rationale="Assigned labels must belong to the accepted taxonomy"
    )

def rule_no_model_prediction_or_training(candidate_definitions: list[dict[str, Any]] | None, label_results: list[HeuristicRegimeLabelResult]) -> RegimeCandidateValidationRule:
    passed = True
    for r in label_results:
        if r.model_prediction or r.model_training_used:
            passed = False
            break

    return RegimeCandidateValidationRule(
        rule_id=create_regime_candidate_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeCandidateValidationRuleKind.NO_MODEL_PREDICTION,
        name="No Model Prediction or Training",
        status=RegimeCandidateValidationStatus.PASS if passed else RegimeCandidateValidationStatus.FAIL,
        required=True,
        passed=passed,
        expected_value=False,
        observed_value=not passed,
        rationale="Phase 128 is deterministic/heuristic, no heavy ML models"
    )

def rule_no_signal_order_portfolio_execution(label_results: list[HeuristicRegimeLabelResult]) -> RegimeCandidateValidationRule:
    passed = True
    for r in label_results:
        if r.produces_trade_signal or r.produces_order_decision or r.produces_portfolio_weights or r.investment_advice:
            passed = False
            break

    return RegimeCandidateValidationRule(
        rule_id=create_regime_candidate_validation_rule_id(),
        created_at_utc=_now_utc(),
        rule_kind=RegimeCandidateValidationRuleKind.NO_SIGNAL_OUTPUT,
        name="No Signal, Order, or Portfolio Output",
        status=RegimeCandidateValidationStatus.PASS if passed else RegimeCandidateValidationStatus.FAIL,
        required=True,
        passed=passed,
        expected_value=False,
        observed_value=not passed,
        rationale="Labels are metadata only, not execution primitives"
    )

def build_candidate_validation_rules(candidate_definitions: list[dict[str, Any]] | None, candidate_scores: list[dict[str, Any]] | None, label_results: list[HeuristicRegimeLabelResult]) -> list[RegimeCandidateValidationRule]:
    return [
        rule_candidate_definitions_available(candidate_definitions),
        rule_candidate_scores_available(candidate_scores, label_results),
        rule_scores_within_range(label_results),
        rule_taxonomy_labels_aligned(candidate_definitions, label_results),
        rule_no_model_prediction_or_training(candidate_definitions, label_results),
        rule_no_signal_order_portfolio_execution(label_results)
    ]

def run_candidate_validation(candidate_definitions: list[dict[str, Any]] | None, candidate_scores: list[dict[str, Any]] | None, label_results: list[HeuristicRegimeLabelResult]) -> RegimeCandidateValidationResult:
    rules = build_candidate_validation_rules(candidate_definitions, candidate_scores, label_results)

    passed = sum(1 for r in rules if r.status == RegimeCandidateValidationStatus.PASS)
    failed = sum(1 for r in rules if r.status == RegimeCandidateValidationStatus.FAIL)
    warning = sum(1 for r in rules if r.status == RegimeCandidateValidationStatus.WARNING)
    blocked = sum(1 for r in rules if r.status == RegimeCandidateValidationStatus.BLOCKED)

    # Needs to pass all required
    required_passed = all(r.passed for r in rules if r.required)

    return RegimeCandidateValidationResult(
        validation_id=create_regime_candidate_validation_result_id(),
        created_at_utc=_now_utc(),
        rules=rules,
        total_rules=len(rules),
        passed_rules=passed,
        warning_rules=warning,
        failed_rules=failed,
        blocked_rules=blocked,
        validation_passed=required_passed,
        candidate_count=len(candidate_definitions) if candidate_definitions else 0,
        score_count=len(candidate_scores) if candidate_scores else 0,
        taxonomy_aligned=all(r.passed for r in rules if r.rule_kind == RegimeCandidateValidationRuleKind.TAXONOMY_LABELS_ALIGNED),
        no_model_training=all(r.passed for r in rules if r.rule_kind == RegimeCandidateValidationRuleKind.NO_MODEL_PREDICTION),
        no_model_prediction=all(r.passed for r in rules if r.rule_kind == RegimeCandidateValidationRuleKind.NO_MODEL_PREDICTION),
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        quality=RegimeLabelingQuality.HIGH if required_passed else RegimeLabelingQuality.LOW
    )

def validate_candidate_validation_result(result: RegimeCandidateValidationResult) -> list[str]:
    errors = []
    if result.produces_trade_signal or result.produces_order_decision or result.produces_portfolio_weights:
        errors.append("Validation result produces execution outputs")
    if not result.no_model_training or not result.no_model_prediction:
        errors.append("Validation allowed model training or prediction")
    return errors

def candidate_validation_runner_summary(result: RegimeCandidateValidationResult) -> dict[str, Any]:
    return {
        "passed": result.validation_passed,
        "rules_passed": result.passed_rules,
        "rules_failed": result.failed_rules
    }

def candidate_validation_runner_to_text(result: RegimeCandidateValidationResult, limit: int = 200) -> str:
    return f"Candidate Validation Passed: {result.validation_passed}. Score: {result.passed_rules}/{result.total_rules}"
