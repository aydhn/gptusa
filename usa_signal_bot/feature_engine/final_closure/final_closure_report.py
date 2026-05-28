import datetime
from typing import Any, Dict
from pathlib import Path
from usa_signal_bot.core.enums import FeatureFactorFinalClosureStatus, FeatureFactorFinalClosureDecision, FinalClosureReportType
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureContext,
    FinalClosureFullReview,
    FinalClosureAudit,
    create_final_closure_context_id,
    create_final_closure_audit_id,
    create_final_closure_full_review_id
)
from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_latest_freeze_preparation_review_from_store
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
from usa_signal_bot.feature_engine.final_closure.final_closure_checks import run_final_closure_checks
from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import build_final_closure_manifest, build_freeze_seal_metadata
from usa_signal_bot.feature_engine.final_closure.engine_readiness_certificate import build_engine_readiness_certificate
from usa_signal_bot.feature_engine.final_closure.phase126_kickoff_gate import build_phase126_kickoff_gate
from usa_signal_bot.feature_engine.final_closure.final_closure_safety_validator import collect_final_closure_risk_flags

def build_final_closure_context() -> FinalClosureContext:
    ingestion = ingest_latest_freeze_preparation_review_from_store(Path("data"))
    artifacts = build_final_artifact_references()
    result = run_final_closure_checks(ingestion, artifacts)
    manifest = build_final_closure_manifest(artifacts)
    seal = build_freeze_seal_metadata(manifest)
    cert = build_engine_readiness_certificate(manifest, seal)
    gate = build_phase126_kickoff_gate(manifest, seal, cert)

    audit = FinalClosureAudit(
        audit_id=create_final_closure_audit_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        phase_range="116-125",
        artifact_hashes={},
        final_manifest_hash=manifest.manifest_hash,
        seal_hash=seal.seal_hash,
        certificate_id=cert.certificate_id,
        kickoff_gate_id=gate.gate_id,
        deterministic=True,
        local_only=True,
        no_network=True,
        no_broker=True,
        no_order=True,
        no_paper_mutation=True,
        no_trade_signal=True,
        no_portfolio_weights=True,
        no_investment_advice=True,
        no_deployment=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    all_ready = ingestion.valid_for_phase125 and result.closure_passed and manifest.final_manifest_valid and seal.sealed and cert.certified_for_research_handoff and gate.ready_for_phase126

    ctx = FinalClosureContext(
        context_id=create_final_closure_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=FeatureFactorFinalClosureStatus.FINAL_CLOSED if all_ready else FeatureFactorFinalClosureStatus.FAILED,
        decision=FeatureFactorFinalClosureDecision.BUILD_PHASE126_KICKOFF_GATE if all_ready else FeatureFactorFinalClosureDecision.BLOCK,
        source_freeze_preparation_review_id=ingestion.source_review_id,
        ingestion=ingestion,
        artifacts=artifacts,
        closure_result=result,
        final_manifest=manifest,
        freeze_seal=seal,
        readiness_certificate=cert,
        phase126_kickoff_gate=gate,
        audit=audit,
        final_artifacts_ready=True,
        final_checks_passed=result.closure_passed,
        freeze_seal_ready=seal.sealed,
        engine_certificate_ready=cert.certified_for_research_handoff,
        phase126_kickoff_gate_ready=gate.ready_for_phase126,
        feature_factor_engine_final_closed=all_ready,
        ready_for_phase126=gate.ready_for_phase126,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
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
        deployment_allowed=False,
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
        dashboard_started=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    ctx.risk_flags = collect_final_closure_risk_flags(ctx)
    return ctx

def build_final_closure_full_review() -> FinalClosureFullReview:
    ctx = build_final_closure_context()
    return FinalClosureFullReview(
        review_id=create_final_closure_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=FinalClosureReportType.FULL_PHASE125_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        closure_result=ctx.closure_result,
        final_manifest=ctx.final_manifest,
        freeze_seal=ctx.freeze_seal,
        readiness_certificate=ctx.readiness_certificate,
        phase126_kickoff_gate=ctx.phase126_kickoff_gate,
        audit=ctx.audit,
        output_paths={},
        warnings=[],
        errors=[]
    )

def final_closure_full_review_summary(review: FinalClosureFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase126": review.context.ready_for_phase126,
        "sealed": review.freeze_seal.sealed,
        "certified": review.readiness_certificate.certified_for_research_handoff
    }

def final_closure_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- Phase 125 is NOT an activation.\n"
        "- This is NOT a strategy or signal engine.\n"
        "- This is NOT a deployment.\n"
        "- No broker API, paper orders, or paper mutations are allowed.\n"
        "- No Telegram real sends, scraping, HTML parsing, dashboards, or paid APIs.\n"
        "- Test execution uses local mocked network data.\n"
        "- Freeze Seal is NOT investment advice.\n"
        "- Phase 126 Kickoff Gate is NOT a trading decision.\n"
    )

def final_closure_full_review_to_text(review: FinalClosureFullReview, limit: int = 300) -> str:
    s = final_closure_full_review_summary(review)
    return f"Review({s['review_id']}): Phase126Ready={s['ready_for_phase126']}, Sealed={s['sealed']}, Certified={s['certified']}\n\n{final_closure_limitations_text()}"
