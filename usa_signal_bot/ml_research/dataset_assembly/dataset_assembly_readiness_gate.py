from typing import Any, Dict, List
from datetime import datetime, timezone
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetAssemblyReadinessGate,
    MLDatasetAssemblyReadinessRule,
    MLDatasetAssemblyReadinessRuleKind,
    MLDatasetAssemblyReadinessStatus,
    MLFoundationIngestionResult,
    MLAssembledDatasetManifest,
    MLSplitPolicy,
    MLSplitAssignment,
    MLLeakageAuditResult,
    MLDatasetQualityProfile,
    MLSplitQualityProfile,
    create_ml_dataset_assembly_readiness_rule_id,
    create_ml_dataset_assembly_readiness_gate_id,
    MLDatasetAssemblyRiskFlag
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _base_rule(kind: MLDatasetAssemblyReadinessRuleKind, passed: bool) -> MLDatasetAssemblyReadinessRule:
    return MLDatasetAssemblyReadinessRule(
        rule_id=create_ml_dataset_assembly_readiness_rule_id(),
        created_at_utc=_now(),
        rule_kind=kind,
        name=kind.value,
        status=MLDatasetAssemblyReadinessStatus.PASSED if passed else MLDatasetAssemblyReadinessStatus.FAILED,
        required=True,
        passed=passed
    )

def build_dataset_assembly_readiness_rules(
    ingestion: MLFoundationIngestionResult,
    manifest: MLAssembledDatasetManifest,
    split_policy: MLSplitPolicy,
    split_assignment: MLSplitAssignment,
    leakage_audit: MLLeakageAuditResult,
    dataset_quality_profiles: List[MLDatasetQualityProfile],
    split_quality_profile: MLSplitQualityProfile
) -> List[MLDatasetAssemblyReadinessRule]:

    rules = []

    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.ML_FOUNDATION_VALID, ingestion.ready_for_phase137))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.DATASET_MANIFEST_VALID, manifest.manifest_valid))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.FEATURE_MATRIX_VALID, manifest.feature_matrix.assembly_valid))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.TARGET_MATRIX_VALID, manifest.target_matrix.assembly_valid))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.LABEL_MATRIX_VALID, manifest.label_matrix.assembly_valid))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.SPLIT_POLICY_VALID, len(split_policy.errors) == 0))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.SPLIT_ASSIGNMENT_VALID, split_assignment.split_assignment_valid))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.LEAKAGE_AUDIT_PASSED, leakage_audit.leakage_audit_passed))

    dq_passed = all(p.status.value in ["HIGH", "ACCEPTABLE"] for p in dataset_quality_profiles)
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.DATASET_QUALITY_ACCEPTABLE, dq_passed))

    sq_passed = split_quality_profile.status.value in ["HIGH", "ACCEPTABLE"]
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.SPLIT_QUALITY_ACCEPTABLE, sq_passed))

    # Non-execution constraints
    exec_passed = not (manifest.activation_allowed or manifest.deployment_allowed)
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.NO_EXECUTION_OUTPUT, exec_passed))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.NO_SIGNAL_OUTPUT, not manifest.produces_trade_signal))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.NO_ORDER_OUTPUT, not manifest.produces_order_decision))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.NO_PORTFOLIO_OUTPUT, not manifest.produces_portfolio_weights))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.NO_MODEL_TRAINING, not manifest.model_training_used))
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.NO_MODEL_PREDICTION, not manifest.model_prediction_used))

    all_passed = all(r.passed for r in rules)
    rules.append(_base_rule(MLDatasetAssemblyReadinessRuleKind.READY_FOR_PHASE138, all_passed))

    return rules

def build_dataset_assembly_readiness_gate(
    ingestion: MLFoundationIngestionResult,
    manifest: MLAssembledDatasetManifest,
    split_policy: MLSplitPolicy,
    split_assignment: MLSplitAssignment,
    leakage_audit: MLLeakageAuditResult,
    dataset_quality_profiles: List[MLDatasetQualityProfile],
    split_quality_profile: MLSplitQualityProfile
) -> MLDatasetAssemblyReadinessGate:

    rules = build_dataset_assembly_readiness_rules(
        ingestion, manifest, split_policy, split_assignment, leakage_audit, dataset_quality_profiles, split_quality_profile
    )

    status = MLDatasetAssemblyReadinessStatus.PASSED if all(r.passed for r in rules) else MLDatasetAssemblyReadinessStatus.FAILED

    gate = MLDatasetAssemblyReadinessGate(
        gate_id=create_ml_dataset_assembly_readiness_gate_id(),
        created_at_utc=_now(),
        status=status,
        rules=rules,
        dataset_manifest=manifest,
        split_policy=split_policy,
        split_assignment=split_assignment,
        leakage_audit=leakage_audit,
        dataset_quality_profiles=dataset_quality_profiles,
        split_quality_profile=split_quality_profile,
        ready_for_phase138=(status == MLDatasetAssemblyReadinessStatus.PASSED)
    )

    gate.errors.extend(validate_dataset_assembly_readiness_gate(gate))
    return gate

def dataset_assembly_readiness_passed(gate: MLDatasetAssemblyReadinessGate) -> bool:
    return gate.status == MLDatasetAssemblyReadinessStatus.PASSED

def dataset_assembly_readiness_blocks_phase138(gate: MLDatasetAssemblyReadinessGate) -> bool:
    return not gate.ready_for_phase138

def validate_dataset_assembly_readiness_gate(gate: MLDatasetAssemblyReadinessGate) -> List[str]:
    errors = []
    if gate.training_started or gate.prediction_started:
        errors.append("Gate contains forbidden training/prediction flags")
    if gate.activation_allowed or gate.deployment_allowed:
        errors.append("Gate contains forbidden deployment flags")
    return errors

def dataset_assembly_readiness_gate_summary(gate: MLDatasetAssemblyReadinessGate) -> Dict[str, Any]:
    return {
        "gate_id": gate.gate_id,
        "status": gate.status.value,
        "ready_for_phase138": gate.ready_for_phase138,
        "total_rules": len(gate.rules),
        "passed_rules": sum(1 for r in gate.rules if r.passed)
    }

def dataset_assembly_readiness_gate_to_text(gate: MLDatasetAssemblyReadinessGate, limit: int = 300) -> str:
    s = json.dumps(dataset_assembly_readiness_gate_summary(gate), indent=2)
    if len(s) > limit:
        return s[:limit] + "..."
    return s
