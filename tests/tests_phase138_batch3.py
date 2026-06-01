import pytest
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_experiment_specs import build_default_baseline_experiment_specs
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_model_family_registry import build_default_baseline_model_family_specs
from usa_signal_bot.ml_research.experiment_scaffolding.evaluation_metric_specs import build_default_evaluation_metric_specs
from usa_signal_bot.ml_research.experiment_scaffolding.evaluation_harness_contract import build_evaluation_harness_contract
from usa_signal_bot.ml_research.experiment_scaffolding.prediction_output_boundary import build_prediction_output_boundary
from usa_signal_bot.ml_research.experiment_scaffolding.model_card_draft_builder import build_model_card_draft_for_experiment
from usa_signal_bot.ml_research.experiment_scaffolding.experiment_registry_builder import build_baseline_experiment_registry, validate_baseline_experiment_registry
from usa_signal_bot.ml_research.experiment_scaffolding.non_activation_evaluation_boundary import build_non_activation_evaluation_boundary_rules, build_non_activation_evaluation_boundary_result
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_experiment_readiness_gate import build_baseline_experiment_readiness_gate
from usa_signal_bot.ml_research.experiment_scaffolding.dataset_assembly_ingestion import ingest_dataset_assembly_review_payload

def test_experiment_registry_builder():
    model_families = build_default_baseline_model_family_specs()
    specs = build_default_baseline_experiment_specs(None, None, model_families)
    metrics = build_default_evaluation_metric_specs()
    contract = build_evaluation_harness_contract(None, None, metrics)
    boundary = build_prediction_output_boundary()

    cards = [build_model_card_draft_for_experiment(s, contract, boundary) for s in specs]

    reg = build_baseline_experiment_registry(specs, model_families, metrics, cards)
    assert reg.registry_valid is True
    errors = validate_baseline_experiment_registry(reg)
    assert len(errors) == 0

def test_non_activation_evaluation_boundary():
    rules = build_non_activation_evaluation_boundary_rules({})
    res = build_non_activation_evaluation_boundary_result(rules)
    assert res.boundary_passed is True

def test_baseline_experiment_readiness_gate():
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
    ingestion = ingest_dataset_assembly_review_payload(payload)

    model_families = build_default_baseline_model_family_specs()
    specs = build_default_baseline_experiment_specs(None, None, model_families)
    metrics = build_default_evaluation_metric_specs()
    contract = build_evaluation_harness_contract(None, None, metrics)
    boundary = build_prediction_output_boundary()
    cards = [build_model_card_draft_for_experiment(s, contract, boundary) for s in specs]
    reg = build_baseline_experiment_registry(specs, model_families, metrics, cards)

    rules = build_non_activation_evaluation_boundary_rules({})
    na_boundary = build_non_activation_evaluation_boundary_result(rules)

    gate = build_baseline_experiment_readiness_gate(ingestion, reg, contract, boundary, na_boundary)
    assert gate.ready_for_phase139 is True
