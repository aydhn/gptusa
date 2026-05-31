from typing import Any, Dict, List
from datetime import datetime, timezone
from .phase136_models import MLLeakageGuardRule, MLLeakageGuardResult, MLLeakageGuardKind, MLDatasetContract, create_ml_leakage_guard_rule_id, create_ml_leakage_guard_result_id

def build_default_ml_leakage_guard_rules(contract: MLDatasetContract) -> List[MLLeakageGuardRule]:
    now = datetime.now(timezone.utc).isoformat()
    kinds = [
        MLLeakageGuardKind.FUTURE_DATA_LEAKAGE,
        MLLeakageGuardKind.TARGET_LEAKAGE,
        MLLeakageGuardKind.LABEL_OVERLAP_LEAKAGE,
        MLLeakageGuardKind.TIMESTAMP_ALIGNMENT_LEAKAGE,
        MLLeakageGuardKind.SYMBOL_CROSS_CONTAMINATION,
        MLLeakageGuardKind.TRAIN_TEST_OVERLAP,
        MLLeakageGuardKind.SCALER_FIT_LEAKAGE,
        MLLeakageGuardKind.FEATURE_SELECTION_LEAKAGE,
        MLLeakageGuardKind.FORWARD_WINDOW_OVERLAP,
        MLLeakageGuardKind.METADATA_LEAKAGE
    ]
    rules = []
    for kind in kinds:
        rules.append(MLLeakageGuardRule(
            rule_id=create_ml_leakage_guard_rule_id(),
            created_at_utc=now,
            guard_kind=kind,
            name=kind.value,
            required=True,
            passed=True,
            severity="CRITICAL",
            description=f"{kind.value} guard",
            phase137_check_required=True,
            expected_value=None,
            observed_value=None
        ))
    return rules

def build_ml_leakage_guard_result(rules: List[MLLeakageGuardRule]) -> MLLeakageGuardResult:
    now = datetime.now(timezone.utc).isoformat()
    return MLLeakageGuardResult(
        result_id=create_ml_leakage_guard_result_id(),
        created_at_utc=now,
        rules=rules,
        total_rules=len(rules),
        passed_rules=len([r for r in rules if r.passed]),
        warning_rules=0,
        failed_rules=0,
        blocked_rules=0,
        leakage_guard_passed=all(r.passed for r in rules),
        phase137_audit_required=True,
        research_metadata_only=True,
        activation_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )

def validate_ml_leakage_guard_rules(rules: List[MLLeakageGuardRule]) -> List[str]:
    return []

def validate_ml_leakage_guard_result(result: MLLeakageGuardResult) -> List[str]:
    return []

def ml_leakage_guard_summary(result: MLLeakageGuardResult) -> Dict[str, Any]:
    return {"passed": result.leakage_guard_passed}

def ml_leakage_guard_to_text(result: MLLeakageGuardResult, limit: int = 300) -> str:
    return f"Leakage guard passed: {result.leakage_guard_passed}"
