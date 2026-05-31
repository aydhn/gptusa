import pytest
from usa_signal_bot.ml_research.foundation.ml_dataset_contract_builder import (
    build_ml_dataset_contract, default_forbidden_ml_output_fields
)
from usa_signal_bot.ml_research.foundation.ml_source_registry_builder import build_ml_source_artifact_references, build_ml_source_registry

def test_build_ml_dataset_contract():
    refs = build_ml_source_artifact_references(None)
    reg = build_ml_source_registry(refs)
    ds = build_ml_dataset_contract(reg, [], [], [])
    assert ds.contract_valid is True
    assert "buy_signal" in ds.forbidden_output_fields
    assert ds.split_design_deferred_to_phase137 is True
