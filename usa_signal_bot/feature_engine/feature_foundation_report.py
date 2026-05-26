import datetime
from typing import Any
from usa_signal_bot.core.enums import FeatureFoundationStatus, FeatureFoundationDecision, FeatureFoundationReportType
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureFoundationContext, FeatureFoundationFullReview, create_feature_foundation_context_id,
    create_feature_foundation_full_review_id, FeatureRegistry
)
from usa_signal_bot.feature_engine.kickoff_gate_ingestion import ingest_feature_factor_kickoff_gate_payload
from usa_signal_bot.feature_engine.indicator_registry import build_default_indicator_definitions
from usa_signal_bot.feature_engine.feature_registry import build_default_feature_definitions
from usa_signal_bot.feature_engine.factor_registry import build_default_factor_definitions
from usa_signal_bot.feature_engine.feature_input_contract import build_feature_input_contract
from usa_signal_bot.feature_engine.feature_schema import build_feature_output_schema
from usa_signal_bot.feature_engine.feature_computation_planner import build_default_feature_computation_requests
from usa_signal_bot.feature_engine.feature_transform_pipeline import FeatureTransformPipeline
from usa_signal_bot.feature_engine.feature_safety_validator import validate_feature_foundation_context_safety

def build_feature_foundation_context() -> FeatureFoundationContext:
    ingestion = ingest_feature_factor_kickoff_gate_payload({"phase116_ready": True, "phase116_scope_allowed": True})

    indicators = build_default_indicator_definitions()
    features = build_default_feature_definitions(indicators)
    factors = build_default_factor_definitions(features)

    registry = FeatureRegistry(
        registry_id="reg_init",
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        indicators=indicators,
        features=features,
        factors=factors,
        total_indicators=len(indicators),
        total_features=len(features),
        total_factors=len(factors),
        registry_valid=True,
        warning_count=0,
        error_count=0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    input_contract = build_feature_input_contract()
    output_schema = build_feature_output_schema(features, factors)

    computation_requests = build_default_feature_computation_requests()

    pipeline = FeatureTransformPipeline(registry, input_contract, output_schema)
    computation_results = pipeline.plan_batch(computation_requests)

    ctx = FeatureFoundationContext(
        context_id=create_feature_foundation_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=FeatureFoundationStatus.CREATED,
        decision=FeatureFoundationDecision.BUILD_FEATURE_FOUNDATION,
        source_kickoff_gate_id=ingestion.source_gate_id,
        ingestion=ingestion,
        input_contract=input_contract,
        output_schema=output_schema,
        registry=registry,
        computation_requests=computation_requests,
        computation_results=computation_results,
        feature_foundation_ready=True,
        indicator_registry_ready=True,
        feature_registry_ready=True,
        factor_registry_ready=True,
        input_contract_ready=True,
        output_schema_ready=True,
        ready_for_phase117=True,
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
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    safety_errors = validate_feature_foundation_context_safety(ctx)
    if safety_errors:
        ctx.status = FeatureFoundationStatus.FAILED
        ctx.decision = FeatureFoundationDecision.BLOCK
        ctx.feature_foundation_ready = False
        ctx.ready_for_phase117 = False
        ctx.errors.extend(safety_errors)
    else:
        ctx.status = FeatureFoundationStatus.VALIDATED
        ctx.decision = FeatureFoundationDecision.CREATE_PHASE117_READY_GATE

    return ctx

def build_feature_foundation_full_review() -> FeatureFoundationFullReview:
    ctx = build_feature_foundation_context()

    return FeatureFoundationFullReview(
        review_id=create_feature_foundation_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        report_type=FeatureFoundationReportType.FULL_PHASE116_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        input_contract=ctx.input_contract,
        output_schema=ctx.output_schema,
        registry=ctx.registry,
        computation_requests=ctx.computation_requests,
        computation_results=ctx.computation_results,
        output_paths={},
        warnings=ctx.warnings,
        errors=ctx.errors
    )

def feature_foundation_full_review_summary(review: FeatureFoundationFullReview) -> dict[str, Any]:
    return {"status": review.context.status.value, "ready_for_phase117": review.context.ready_for_phase117}

def feature_foundation_limitations_text() -> str:
    return "This review is purely an architectural skeleton. It produces no trade signals, activates no trading, executes no orders, mutates no paper state, triggers no telegram messages, accesses no external networks, does not scrape, and is explicitly not investment advice."

def feature_foundation_full_review_to_text(review: FeatureFoundationFullReview, limit: int = 300) -> str:
    return f"Feature Foundation Review: {review.review_id}\nStatus: {review.context.status.value}\nPhase 117 Ready: {review.context.ready_for_phase117}\n" + feature_foundation_limitations_text()
