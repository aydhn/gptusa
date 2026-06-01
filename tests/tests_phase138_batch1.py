import pytest
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    create_ml_dataset_assembly_ingestion_id,
    MLDatasetAssemblyIngestionResult
)
from usa_signal_bot.ml_research.experiment_scaffolding.dataset_assembly_ingestion import (
    ingest_dataset_assembly_review_payload
)
from usa_signal_bot.ml_research.experiment_scaffolding.dataset_assembly_artifact_loader import (
    validate_dataset_assembly_artifacts,
    dataset_assembly_artifact_loader_summary
)
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_model_family_registry import (
    build_default_baseline_model_family_specs,
    validate_baseline_model_family_specs
)

def test_phase138_models_basic():
    id_val = create_ml_dataset_assembly_ingestion_id()
    assert id_val.startswith("dai_")

def test_dataset_assembly_ingestion():
    payload = {
        "ready_for_phase138": True,
        "research_data_only": True,
        "context": {
            "ml_foundation_ingested": True,
            "sources_resolved": True,
            "feature_matrix_assembled": True,
            "target_matrix_assembled": True,
            "label_matrix_assembled": True,
            "dataset_manifest_built": True,
            "split_policy_built": True,
            "split_assignment_built": True,
            "leakage_audit_completed": True,
            "dataset_quality_evaluated": True,
            "split_quality_evaluated": True,
            "readiness_gate_passed": True
        }
    }
    res = ingest_dataset_assembly_review_payload(payload)
    assert res.valid_for_phase138 is True

def test_dataset_assembly_artifact_loader():
    payloads = {
        "manifest": {"id": "1"},
        "splits": {"id": "2"},
        "leakage_audit": {"audit_passed": True},
        "readiness_gate": {"ready_for_phase138": True}
    }
    errors = validate_dataset_assembly_artifacts(payloads)
    assert len(errors) == 0

def test_baseline_model_family_registry():
    specs = build_default_baseline_model_family_specs()
    assert len(specs) >= 6
    errors = validate_baseline_model_family_specs(specs)
    assert len(errors) == 0
