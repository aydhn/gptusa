import pytest
from pathlib import Path
from usa_signal_bot.ml_research.dataset_assembly.dataset_source_resolver import resolve_source_reference
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import MLDatasetSourceResolutionStatus

def test_source_resolver_catches_path_traversal():
    payload = {"source_name": "test_src", "source_path": "../../../etc/passwd"}
    ref = resolve_source_reference(payload)

    assert ref.source_resolution_status == MLDatasetSourceResolutionStatus.BLOCKED
    assert any("traversal" in e.lower() for e in ref.errors)

def test_source_resolver_missing_file():
    payload = {"source_name": "test_src", "source_path": "does_not_exist.csv"}
    ref = resolve_source_reference(payload)

    assert ref.source_resolution_status == MLDatasetSourceResolutionStatus.MISSING
