import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_readiness_gate import build_ensemble_readiness_gate
from usa_signal_bot.ml_research.ensemble_scaffolding.ensemble_governance import build_ensemble_governance_result
from usa_signal_bot.ml_research.ensemble_scaffolding.non_activation_ensemble_boundary import build_non_activation_ensemble_boundary_result, build_non_activation_ensemble_boundary_rules
from usa_signal_bot.ml_research.ensemble_scaffolding.calibration_diagnostics_ingestion import ingest_calibration_diagnostics_review_payload

def test_build_gate():
    gov = build_ensemble_governance_result([], [], [])
    rules = build_non_activation_ensemble_boundary_rules()
    bound = build_non_activation_ensemble_boundary_result(rules)
    ingest = ingest_calibration_diagnostics_review_payload({})

    gate = build_ensemble_readiness_gate(ingest, [], gov, bound)
    assert gate.ready_for_phase143 is False # since ingest is not ready
