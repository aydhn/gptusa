import pytest
from usa_signal_bot.ml_research.dataset_assembly.dataset_quality_evaluator import build_dataset_quality_profiles
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLMatrixAssemblyResult,
    MLAssembledDatasetManifest,
    MLMatrixKind,
    MLAssemblyMode,
    MLDatasetQualityStatus
)

def test_dataset_quality_profiles_row_column_count():
    feat = MLMatrixAssemblyResult(
        result_id="f1", created_at_utc="now", matrix_kind=MLMatrixKind.FEATURE_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=100, column_count=10, assembly_valid=True
    )
    targ = MLMatrixAssemblyResult(
        result_id="t1", created_at_utc="now", matrix_kind=MLMatrixKind.TARGET_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=100, column_count=2, assembly_valid=True
    )
    lab = MLMatrixAssemblyResult(
        result_id="l1", created_at_utc="now", matrix_kind=MLMatrixKind.LABEL_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=100, column_count=2, assembly_valid=True
    )

    manifest = MLAssembledDatasetManifest(
        manifest_id="m1", created_at_utc="now", manifest_version="1",
        feature_matrix=feat, target_matrix=targ, label_matrix=lab,
        total_row_count=100, feature_count=10, target_count=2, label_count=2,
        manifest_valid=True
    )

    profiles = build_dataset_quality_profiles(feat, targ, lab, manifest)

    assert len(profiles) == 5
    for p in profiles:
        assert p.status == MLDatasetQualityStatus.ACCEPTABLE

def test_dataset_quality_profiles_invalid_empty():
    feat = MLMatrixAssemblyResult(
        result_id="f1", created_at_utc="now", matrix_kind=MLMatrixKind.FEATURE_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=0, column_count=0, assembly_valid=True
    )
    targ = MLMatrixAssemblyResult(
        result_id="t1", created_at_utc="now", matrix_kind=MLMatrixKind.TARGET_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=0, column_count=0, assembly_valid=True
    )
    lab = MLMatrixAssemblyResult(
        result_id="l1", created_at_utc="now", matrix_kind=MLMatrixKind.LABEL_MATRIX,
        assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=0, column_count=0, assembly_valid=True
    )

    manifest = MLAssembledDatasetManifest(
        manifest_id="m1", created_at_utc="now", manifest_version="1",
        feature_matrix=feat, target_matrix=targ, label_matrix=lab,
        total_row_count=0, feature_count=0, target_count=0, label_count=0,
        manifest_valid=True
    )

    profiles = build_dataset_quality_profiles(feat, targ, lab, manifest)

    row_count_profile = next(p for p in profiles if p.quality_kind.value == "ROW_COUNT_QUALITY")
    assert row_count_profile.status == MLDatasetQualityStatus.INVALID
    assert row_count_profile.score == 0.0
