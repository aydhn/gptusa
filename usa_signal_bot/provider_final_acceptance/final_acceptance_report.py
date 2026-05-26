from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFinalAcceptanceContext,
    ProviderFinalAcceptanceFullReview,
    ProviderFinalAcceptanceReportType,
    ProviderFinalAcceptanceStatus,
    ProviderFinalAcceptanceDecision,
    ProviderFreezeIngestionResult,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureBundle,
    FeatureFactorDataContract,
    FeatureFactorEngineKickoffGate,
    create_provider_final_acceptance_context_id,
    create_provider_final_acceptance_full_review_id,
    _utc_now
)
from usa_signal_bot.provider_final_acceptance.provider_freeze_ingestion import ingest_provider_freeze_review_payload
from usa_signal_bot.provider_final_acceptance.final_acceptance_checker import build_data_provider_final_acceptance_report
from usa_signal_bot.provider_final_acceptance.provider_layer_closure import build_provider_layer_closure_bundle
from usa_signal_bot.provider_final_acceptance.final_data_contract_checker import build_feature_factor_data_contract
from usa_signal_bot.provider_final_acceptance.feature_factor_kickoff_gate import build_feature_factor_engine_kickoff_gate

def build_provider_final_acceptance_context(payload: dict[str, Any] = None) -> ProviderFinalAcceptanceContext:
    if payload is None:
        payload = {}

    ingestion = ingest_provider_freeze_review_payload(payload)
    acceptance_report = build_data_provider_final_acceptance_report(ingestion)
    closure_bundle = build_provider_layer_closure_bundle(ingestion)
    data_contract = build_feature_factor_data_contract()
    kickoff_gate = build_feature_factor_engine_kickoff_gate(acceptance_report, closure_bundle, data_contract)

    passed = acceptance_report.data_provider_layer_accepted and closure_bundle.closed and kickoff_gate.ready_for_phase116
    status = ProviderFinalAcceptanceStatus.ACCEPTED if passed else ProviderFinalAcceptanceStatus.FAILED
    decision = ProviderFinalAcceptanceDecision.ACCEPT_DATA_PROVIDER_LAYER if passed else ProviderFinalAcceptanceDecision.BLOCK

    return ProviderFinalAcceptanceContext(
        context_id=create_provider_final_acceptance_context_id(),
        created_at_utc=_utc_now(),
        status=status,
        decision=decision,
        source_provider_freeze_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        final_acceptance_report=acceptance_report,
        closure_bundle=closure_bundle,
        feature_factor_data_contract=data_contract,
        kickoff_gate=kickoff_gate,
        data_provider_layer_accepted=acceptance_report.data_provider_layer_accepted,
        provider_layer_closed=closure_bundle.closed,
        feature_factor_kickoff_ready=kickoff_gate.ready_for_phase116,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
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
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        ready_for_phase116=kickoff_gate.ready_for_phase116,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_provider_final_acceptance_full_review(payload: dict[str, Any] = None) -> ProviderFinalAcceptanceFullReview:
    ctx = build_provider_final_acceptance_context(payload)
    return ProviderFinalAcceptanceFullReview(
        review_id=create_provider_final_acceptance_full_review_id(),
        created_at_utc=_utc_now(),
        report_type=ProviderFinalAcceptanceReportType.FULL_PHASE115_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        final_acceptance_report=ctx.final_acceptance_report,
        closure_bundle=ctx.closure_bundle,
        feature_factor_data_contract=ctx.feature_factor_data_contract,
        kickoff_gate=ctx.kickoff_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def provider_final_acceptance_full_review_summary(review: ProviderFinalAcceptanceFullReview) -> dict[str, Any]:
    return {
        "status": review.context.status,
        "decision": review.context.decision,
        "ready_for_phase116": review.context.ready_for_phase116
    }

def provider_final_acceptance_limitations_text() -> str:
    return "Phase 115 is final data provider acceptance. It is NOT active paper trading or live deployment. Real execution, broker API, HTML scraping and Telegram sends are strictly blocked."

def provider_final_acceptance_full_review_to_text(review: ProviderFinalAcceptanceFullReview, limit: int = 300) -> str:
    s = provider_final_acceptance_full_review_summary(review)
    return f"Phase 115 Full Review [{s['status']}] - Ready for 116: {s['ready_for_phase116']}\n{provider_final_acceptance_limitations_text()}"
