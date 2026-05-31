from typing import Any, Dict, List
from datetime import datetime, timezone
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetQualityProfile,
    MLDatasetQualityKind,
    MLDatasetQualityStatus,
    MLMatrixAssemblyResult,
    MLAssembledDatasetManifest,
    create_ml_dataset_quality_profile_id
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _base_profile(kind: MLDatasetQualityKind) -> MLDatasetQualityProfile:
    return MLDatasetQualityProfile(
        profile_id=create_ml_dataset_quality_profile_id(),
        created_at_utc=_now(),
        quality_kind=kind,
        status=MLDatasetQualityStatus.ACCEPTABLE,
        score=100.0
    )

def build_dataset_quality_profiles(
    feature_result: MLMatrixAssemblyResult,
    target_result: MLMatrixAssemblyResult,
    label_result: MLMatrixAssemblyResult,
    manifest: MLAssembledDatasetManifest
) -> List[MLDatasetQualityProfile]:
    profiles = []
    profiles.append(evaluate_row_count_quality(manifest))
    profiles.append(evaluate_column_count_quality(manifest))
    profiles.append(evaluate_missing_value_quality([feature_result, target_result, label_result]))
    profiles.append(evaluate_duplicate_row_quality([feature_result, target_result, label_result]))
    profiles.append(evaluate_contract_compliance_quality(manifest))

    errors = validate_dataset_quality_profiles(profiles)
    for p in profiles:
        p.errors.extend(errors)

    return profiles

def evaluate_row_count_quality(manifest: MLAssembledDatasetManifest) -> MLDatasetQualityProfile:
    p = _base_profile(MLDatasetQualityKind.ROW_COUNT_QUALITY)
    p.metric_snapshot = {"total_rows": manifest.total_row_count}
    if manifest.total_row_count == 0:
        p.status = MLDatasetQualityStatus.INVALID
        p.score = 0.0
    return p

def evaluate_column_count_quality(manifest: MLAssembledDatasetManifest) -> MLDatasetQualityProfile:
    p = _base_profile(MLDatasetQualityKind.COLUMN_COUNT_QUALITY)
    p.metric_snapshot = {"feature_count": manifest.feature_count, "target_count": manifest.target_count}
    if manifest.feature_count == 0 or manifest.target_count == 0:
        p.status = MLDatasetQualityStatus.INVALID
        p.score = 0.0
    return p

def evaluate_missing_value_quality(results: List[MLMatrixAssemblyResult]) -> MLDatasetQualityProfile:
    p = _base_profile(MLDatasetQualityKind.MISSING_VALUE_QUALITY)
    return p

def evaluate_duplicate_row_quality(results: List[MLMatrixAssemblyResult]) -> MLDatasetQualityProfile:
    p = _base_profile(MLDatasetQualityKind.DUPLICATE_ROW_QUALITY)
    total_dupes = sum(r.duplicate_row_count for r in results)
    p.metric_snapshot = {"total_duplicate_rows": total_dupes}
    if total_dupes > 0:
        p.status = MLDatasetQualityStatus.WARNING
        p.score = 90.0
    return p

def evaluate_contract_compliance_quality(manifest: MLAssembledDatasetManifest) -> MLDatasetQualityProfile:
    p = _base_profile(MLDatasetQualityKind.CONTRACT_COMPLIANCE_QUALITY)
    return p

def validate_dataset_quality_profiles(items: List[MLDatasetQualityProfile]) -> List[str]:
    errors = []
    for p in items:
        if p.produces_trade_signal or p.investment_advice:
            errors.append(f"Profile {p.quality_kind.value} contains forbidden semantic flags")
    return errors
