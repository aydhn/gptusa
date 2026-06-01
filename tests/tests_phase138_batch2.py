import pytest
from usa_signal_bot.ml_research.experiment_scaffolding.baseline_experiment_specs import build_default_baseline_experiment_specs, validate_baseline_experiment_specs
from usa_signal_bot.ml_research.experiment_scaffolding.evaluation_metric_specs import build_default_evaluation_metric_specs, validate_evaluation_metric_specs
from usa_signal_bot.ml_research.experiment_scaffolding.evaluation_harness_contract import build_evaluation_harness_contract, validate_evaluation_harness_contract
from usa_signal_bot.ml_research.experiment_scaffolding.prediction_output_boundary import build_prediction_output_boundary, validate_prediction_output_boundary
from usa_signal_bot.ml_research.experiment_scaffolding.model_card_draft_builder import build_model_card_draft_for_experiment, validate_model_card_draft

def test_baseline_experiment_specs():
    specs = build_default_baseline_experiment_specs()
    assert len(specs) > 0
    errors = validate_baseline_experiment_specs(specs)
    assert len(errors) == 0

def test_evaluation_metric_specs():
    specs = build_default_evaluation_metric_specs()
    assert len(specs) > 0
    errors = validate_evaluation_metric_specs(specs)
    assert len(errors) == 0

def test_evaluation_harness_contract():
    metrics = build_default_evaluation_metric_specs()
    contract = build_evaluation_harness_contract({"manifest_id": "1"}, {"assignment_id": "1"}, metrics)
    assert contract.contract_valid is True
    errors = validate_evaluation_harness_contract(contract)
    assert len(errors) == 0

def test_prediction_output_boundary():
    boundary = build_prediction_output_boundary()
    assert boundary.boundary_valid is True
    errors = validate_prediction_output_boundary(boundary)
    assert len(errors) == 0

def test_model_card_draft_builder():
    specs = build_default_baseline_experiment_specs()
    metrics = build_default_evaluation_metric_specs()
    contract = build_evaluation_harness_contract({}, {}, metrics)
    boundary = build_prediction_output_boundary()
    card = build_model_card_draft_for_experiment(specs[0], contract, boundary)

    assert card.draft_only is True
    assert card.training_not_started is True
    errors = validate_model_card_draft(card)
    assert len(errors) == 0
