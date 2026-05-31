import pytest
from usa_signal_bot.ml_research.dataset_assembly.dataset_manifest_builder import build_assembled_dataset_manifest
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLMatrixAssemblyResult,
    MLMatrixKind,
    MLAssemblyMode
)

def test_manifest_builder_computes_hash():
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

    manifest = build_assembled_dataset_manifest(feat, targ, lab, [])

    assert manifest.manifest_valid is True
    assert manifest.manifest_hash is not None
    assert manifest.total_row_count == 100
