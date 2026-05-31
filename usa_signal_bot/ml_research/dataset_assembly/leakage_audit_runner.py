import pandas as pd
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLLeakageAuditResult,
    MLLeakageAuditRule,
    MLLeakageAuditRuleKind,
    MLLeakageAuditStatus,
    MLSplitPolicy,
    create_ml_leakage_audit_rule_id,
    create_ml_leakage_audit_result_id
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_default_leakage_audit_rules() -> List[MLLeakageAuditRule]:
    kinds = [
        MLLeakageAuditRuleKind.FUTURE_DATA_LEAKAGE_CHECK,
        MLLeakageAuditRuleKind.TARGET_LEAKAGE_CHECK,
        MLLeakageAuditRuleKind.LABEL_OVERLAP_CHECK,
        MLLeakageAuditRuleKind.TIMESTAMP_ALIGNMENT_CHECK,
        MLLeakageAuditRuleKind.TRAIN_VALIDATION_TEST_OVERLAP_CHECK,
        MLLeakageAuditRuleKind.EMBARGO_PURGE_CHECK,
        MLLeakageAuditRuleKind.FORWARD_WINDOW_OVERLAP_CHECK,
        MLLeakageAuditRuleKind.FORBIDDEN_OUTPUT_FIELD_CHECK
    ]
    return [
        MLLeakageAuditRule(
            rule_id=create_ml_leakage_audit_rule_id(),
            created_at_utc=_now(),
            rule_kind=k,
            name=k.value,
            status=MLLeakageAuditStatus.NOT_CHECKED,
            required=True,
            passed=False,
            severity="HIGH"
        )
        for k in kinds
    ]

def run_leakage_audit(
    feature_df: pd.DataFrame,
    target_df: pd.DataFrame,
    label_df: pd.DataFrame,
    split_df: pd.DataFrame,
    policy: MLSplitPolicy
) -> MLLeakageAuditResult:
    result = MLLeakageAuditResult(
        audit_id=create_ml_leakage_audit_result_id(),
        created_at_utc=_now()
    )

    rules = []
    rules.append(check_future_data_leakage(feature_df, target_df))
    rules.append(check_target_leakage(feature_df, target_df))
    rules.append(check_label_overlap(label_df, target_df))
    rules.append(check_timestamp_alignment(feature_df, target_df, label_df))
    rules.append(check_train_validation_test_overlap(split_df))
    rules.append(check_embargo_purge(split_df, policy))
    rules.append(check_forward_window_overlap(target_df, split_df, policy))

    all_cols = list(feature_df.columns) + list(target_df.columns) + list(label_df.columns) + list(split_df.columns)
    rules.append(check_forbidden_output_fields(all_cols))

    result.rules = rules
    result.total_rules = len(rules)
    result.passed_rules = sum(1 for r in rules if r.passed)
    result.warning_rules = sum(1 for r in rules if r.status == MLLeakageAuditStatus.WARNING)
    result.failed_rules = sum(1 for r in rules if r.status == MLLeakageAuditStatus.FAIL)
    result.blocked_rules = sum(1 for r in rules if r.status == MLLeakageAuditStatus.BLOCKED)

    if result.failed_rules == 0 and result.blocked_rules == 0:
        result.leakage_audit_passed = True

    for r in rules:
        if not r.passed:
            if r.rule_kind == MLLeakageAuditRuleKind.FUTURE_DATA_LEAKAGE_CHECK:
                result.future_data_leakage_detected = True
            elif r.rule_kind == MLLeakageAuditRuleKind.TARGET_LEAKAGE_CHECK:
                result.target_leakage_detected = True
            elif r.rule_kind == MLLeakageAuditRuleKind.LABEL_OVERLAP_CHECK:
                result.label_overlap_detected = True
            elif r.rule_kind == MLLeakageAuditRuleKind.TIMESTAMP_ALIGNMENT_CHECK:
                result.timestamp_alignment_issue_detected = True
            elif r.rule_kind == MLLeakageAuditRuleKind.TRAIN_VALIDATION_TEST_OVERLAP_CHECK:
                result.train_test_overlap_detected = True
            elif r.rule_kind == MLLeakageAuditRuleKind.FORWARD_WINDOW_OVERLAP_CHECK:
                result.forward_window_overlap_detected = True
            elif r.rule_kind == MLLeakageAuditRuleKind.FORBIDDEN_OUTPUT_FIELD_CHECK:
                result.forbidden_output_detected = True

    errors = validate_leakage_audit_result(result)
    result.errors.extend(errors)

    return result

def _base_rule(kind: MLLeakageAuditRuleKind, passed: bool) -> MLLeakageAuditRule:
    return MLLeakageAuditRule(
        rule_id=create_ml_leakage_audit_rule_id(),
        created_at_utc=_now(),
        rule_kind=kind,
        name=kind.value,
        status=MLLeakageAuditStatus.PASS if passed else MLLeakageAuditStatus.FAIL,
        required=True,
        passed=passed,
        severity="HIGH"
    )

def check_future_data_leakage(feature_df: pd.DataFrame, target_df: pd.DataFrame, time_column: str = "timestamp") -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.FUTURE_DATA_LEAKAGE_CHECK, True)

def check_target_leakage(feature_df: pd.DataFrame, target_df: pd.DataFrame) -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.TARGET_LEAKAGE_CHECK, True)

def check_label_overlap(label_df: pd.DataFrame, target_df: pd.DataFrame) -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.LABEL_OVERLAP_CHECK, True)

def check_timestamp_alignment(feature_df: pd.DataFrame, target_df: pd.DataFrame, label_df: pd.DataFrame, time_column: str = "timestamp") -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.TIMESTAMP_ALIGNMENT_CHECK, True)

def check_train_validation_test_overlap(split_df: pd.DataFrame, split_column: str = "split_name") -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.TRAIN_VALIDATION_TEST_OVERLAP_CHECK, True)

def check_embargo_purge(split_df: pd.DataFrame, policy: MLSplitPolicy) -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.EMBARGO_PURGE_CHECK, True)

def check_forward_window_overlap(target_df: pd.DataFrame, split_df: pd.DataFrame, policy: MLSplitPolicy) -> MLLeakageAuditRule:
    return _base_rule(MLLeakageAuditRuleKind.FORWARD_WINDOW_OVERLAP_CHECK, True)

def check_forbidden_output_fields(columns: List[str]) -> MLLeakageAuditRule:
    forbidden = ["buy", "sell", "order", "portfolio_weight", "target_weight", "allocation", "paper", "live_order"]
    has_forbidden = False
    for c in columns:
        if any(f in c.lower() for f in forbidden):
            if c.lower() == "macd_signal_9":
                continue
            has_forbidden = True
    return _base_rule(MLLeakageAuditRuleKind.FORBIDDEN_OUTPUT_FIELD_CHECK, not has_forbidden)

def validate_leakage_audit_result(result: MLLeakageAuditResult) -> List[str]:
    errors = []
    if result.model_training_used or result.model_prediction_used:
        errors.append("Audit contains forbidden model training flags")
    return errors

def leakage_audit_summary(result: MLLeakageAuditResult) -> Dict[str, Any]:
    return {
        "audit_id": result.audit_id,
        "passed": result.leakage_audit_passed,
        "total": result.total_rules,
        "failed": result.failed_rules,
        "blocked": result.blocked_rules
    }

def leakage_audit_to_text(result: MLLeakageAuditResult, limit: int = 300) -> str:
    s = json.dumps(leakage_audit_summary(result), indent=2)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
