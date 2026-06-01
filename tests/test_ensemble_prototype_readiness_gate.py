from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_readiness_gate import build_ensemble_prototype_readiness_gate
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_scaffolding_ingestion import ingest_ensemble_scaffolding_review_payload
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_prototype_boundary import build_ensemble_prototype_boundary_result, build_ensemble_prototype_boundary_rules
from usa_signal_bot.ml_research.ensemble_evaluation.non_activation_ensemble_registry import build_non_activation_ensemble_registry

def test_build_ensemble_prototype_readiness_gate():
    ingestion = ingest_ensemble_scaffolding_review_payload({"report_type": "ENSEMBLE_SCAFFOLDING_FULL_REVIEW", "context": {"ready_for_phase143": True, "research_data_only": True, "offline_ml_research_only": True}})
    boundary = build_ensemble_prototype_boundary_result(build_ensemble_prototype_boundary_rules())
    registry = build_non_activation_ensemble_registry([], [], [])

    gate = build_ensemble_prototype_readiness_gate(ingestion, [], [], [], registry, boundary)
    assert gate.ready_for_phase144 is True
    assert gate.live_inference_enabled is False
    assert gate.deployment_allowed is False
