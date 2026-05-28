from usa_signal_bot.regime_classification.foundation.regime_foundation_report import build_regime_foundation_context, build_regime_foundation_full_review
from usa_signal_bot.regime_classification.foundation.final_closure_ingestion import ingest_final_closure_review_payload
from usa_signal_bot.regime_classification.foundation.frozen_artifact_loader import build_regime_research_input_bundle
from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import build_market_state_dataset_contract
from usa_signal_bot.regime_classification.foundation.market_state_dataset_skeleton import build_market_state_dataset_skeleton
from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import build_regime_label_taxonomy
from usa_signal_bot.regime_classification.foundation.regime_non_activation_boundary import build_regime_non_activation_boundary_result
from usa_signal_bot.core.enums import RegimeFoundationStatus

def test_build_regime_foundation_context_and_review():
    payload = {
        "review_id": "rev_123",
        "context": {
            "context_id": "ctx_123",
            "final_artifacts_ready": True,
            "final_checks_passed": True,
            "freeze_seal_ready": True,
            "feature_factor_engine_final_closed": True,
            "ready_for_phase126": True,
            "research_data_only": True,
            "activation_allowed": False
        },
        "engine_certificate": {"certificate_valid": True},
        "phase126_kickoff_gate": {"gate_passed": True}
    }
    ingestion = ingest_final_closure_review_payload(payload)
    bundle = build_regime_research_input_bundle("rev_123", [])
    contract = build_market_state_dataset_contract()
    skeleton = build_market_state_dataset_skeleton(contract)
    taxonomy = build_regime_label_taxonomy()
    boundary = build_regime_non_activation_boundary_result()

    ctx = build_regime_foundation_context(ingestion, bundle, contract, skeleton, taxonomy, boundary)
    assert ctx.ready_for_phase127 is False # Because frozen artifacts empty/missing
    assert ctx.status == RegimeFoundationStatus.CREATED

    review = build_regime_foundation_full_review(ctx)
    assert review.context.context_id == ctx.context_id
