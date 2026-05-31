from typing import Any, Dict
from datetime import datetime, timezone
from .phase136_models import (
    MLFoundationContext, MLFoundationFullReview, MLFoundationStatus, MLFoundationDecision,
    MLFoundationReportType, create_ml_foundation_context_id, create_ml_foundation_full_review_id
)
from .final_closure_ingestion import ingest_final_closure_review_payload
from .ml_source_registry_builder import build_ml_source_artifact_references, build_ml_source_registry
from .ml_feature_contract_builder import build_default_ml_feature_contracts
from .ml_target_contract_builder import build_default_ml_target_contracts
from .ml_label_contract_builder import build_default_ml_label_contracts
from .ml_dataset_contract_builder import build_ml_dataset_contract
from .leakage_guard_specs import build_default_ml_leakage_guard_rules, build_ml_leakage_guard_result
from .ml_non_activation_boundary import build_ml_non_activation_boundary_rules, build_ml_non_activation_boundary_result
from .ml_research_governance import build_ml_research_governance_rules, build_ml_research_governance_result
from .ml_foundation_readiness_gate import build_ml_foundation_readiness_gate

def build_ml_foundation_context() -> MLFoundationContext:
    now = datetime.now(timezone.utc).isoformat()
    ingestion = ingest_final_closure_review_payload({})
    refs = build_ml_source_artifact_references(None, None)
    registry = build_ml_source_registry(refs)
    feat_c = build_default_ml_feature_contracts(registry)
    tgt_c = build_default_ml_target_contracts()
    lbl_c = build_default_ml_label_contracts()
    ds_c = build_ml_dataset_contract(registry, feat_c, tgt_c, lbl_c)
    lg_rules = build_default_ml_leakage_guard_rules(ds_c)
    lg = build_ml_leakage_guard_result(lg_rules)
    nab_rules = build_ml_non_activation_boundary_rules()
    nab = build_ml_non_activation_boundary_result(nab_rules)
    gov_rules = build_ml_research_governance_rules()
    gov = build_ml_research_governance_result(gov_rules)
    gate = build_ml_foundation_readiness_gate(ingestion, registry, ds_c, lg, nab, gov)

    return MLFoundationContext(
        context_id=create_ml_foundation_context_id(),
        created_at_utc=now,
        status=MLFoundationStatus.VALIDATED if gate.ready_for_phase137 else MLFoundationStatus.BLOCKED,
        decision=MLFoundationDecision.BUILD_READINESS_GATE,
        source_final_closure_review_id=None,
        ingestion=ingestion,
        source_registry=registry,
        feature_contracts=feat_c,
        target_contracts=tgt_c,
        label_contracts=lbl_c,
        dataset_contract=ds_c,
        leakage_guard=lg,
        non_activation_boundary=nab,
        governance=gov,
        readiness_gate=gate,
        final_closure_ingested=True,
        final_closure_artifacts_loaded=True,
        source_registry_built=True,
        feature_contract_built=True,
        target_contract_built=True,
        label_contract_built=True,
        dataset_contract_built=True,
        leakage_guard_built=True,
        non_activation_boundary_validated=True,
        governance_built=True,
        readiness_gate_built=True,
        readiness_gate_passed=gate.ready_for_phase137,
        ready_for_phase137=gate.ready_for_phase137,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        daemon_started=False,
        scheduler_enabled=False,
        training_started=False,
        prediction_started=False,
        model_training_used=False,
        model_prediction_used=False,
        heavy_ml_dependency_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False
    )

def build_ml_foundation_full_review() -> MLFoundationFullReview:
    now = datetime.now(timezone.utc).isoformat()
    context = build_ml_foundation_context()
    return MLFoundationFullReview(
        review_id=create_ml_foundation_full_review_id(),
        created_at_utc=now,
        report_type=MLFoundationReportType.FULL_PHASE136_REVIEW,
        ingestion=context.ingestion,
        context=context,
        source_registry=context.source_registry,
        dataset_contract=context.dataset_contract,
        leakage_guard=context.leakage_guard,
        non_activation_boundary=context.non_activation_boundary,
        governance=context.governance,
        readiness_gate=context.readiness_gate,
        output_paths={}
    )

def ml_foundation_full_review_summary(review: MLFoundationFullReview) -> Dict[str, Any]:
    return {"ready_for_phase137": review.readiness_gate.ready_for_phase137}

def ml_foundation_limitations_text() -> str:
    return "Phase 136 is research foundation only. No training, no prediction, no execution."

def ml_foundation_full_review_to_text(review: MLFoundationFullReview, limit: int = 300) -> str:
    return f"Review {review.review_id} - Ready: {review.readiness_gate.ready_for_phase137}"
