import pytest
from usa_signal_bot.regime_classification.foundation.frozen_artifact_loader import (
    build_frozen_artifact_references_from_final_closure,
    build_regime_research_input_bundle,
    validate_frozen_artifact_references
)

def test_build_frozen_artifact_references():
    payload = {
        "output_paths": {
            "factor_table_1": "/fake/path/factor1.csv",
            "diagnostics_1": "/fake/path/diag1.json"
        }
    }
    refs = build_frozen_artifact_references_from_final_closure(payload)
    assert len(refs) == 2
    assert refs[0].artifact_name == "factor_table_1"
    assert refs[1].artifact_name == "diagnostics_1"

def test_build_regime_research_input_bundle():
    payload = {
        "output_paths": {
            "factor_table_1": "/fake/path/factor1.csv",
            "schema_contract_1": "/fake/path/schema1.json"
        }
    }
    refs = build_frozen_artifact_references_from_final_closure(payload)
    bundle = build_regime_research_input_bundle("rev_123", refs)
    assert bundle.bundle_valid is True
    assert bundle.source_final_closure_review_id == "rev_123"
    assert len(bundle.factor_table_refs) == 1
    assert len(bundle.schema_contract_refs) == 1

def test_validate_frozen_artifact_references():
    payload = {
        "output_paths": {
            "factor_table_1": "/fake/../path/factor1.csv"
        }
    }
    refs = build_frozen_artifact_references_from_final_closure(payload)
    errors = validate_frozen_artifact_references(refs)
    assert len(errors) == 1
    assert "Path traversal detected" in errors[0]
