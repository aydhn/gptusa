from typing import Any, Dict, List, Optional
from pathlib import Path
from usa_signal_bot.release.phase159_models import (
    AdvancedAcceptanceContext,
    AdvancedAcceptanceFullReview,
    AdvancedAcceptanceReportType,
    AdvancedAcceptanceStatus,
    AdvancedAcceptanceDecision,
    Phase158IntegrationIngestionResult,
    AdvancedAcceptanceInputReference,
    AcceptanceScenarioMatrix,
    AdvancedDryRunStep,
    AcceptanceEvidenceBundle,
    AcceptanceAreaReport,
    ReleaseCandidateRiskRegister,
    ReleaseCandidateAudit,
    FinalFreezeChecklist,
    FinalFreezeBoundaryResult,
    FinalFreezeCertificate,
    Phase160HandoffContract,
    Phase160HandoffPackage,
    Phase160ReadinessGate,
    create_advanced_acceptance_context_id,
    create_advanced_acceptance_full_review_id,
    generate_timestamp
)

def build_advanced_acceptance_context() -> AdvancedAcceptanceContext:
    # Factory for an empty/draft context
    return AdvancedAcceptanceContext(
        context_id=create_advanced_acceptance_context_id(),
        created_at_utc=generate_timestamp(),
        status=AdvancedAcceptanceStatus.DRAFT,
        decision=AdvancedAcceptanceDecision.LOAD_PHASE158_INTEGRATION_REVIEW,
        source_phase158_review_id=None,
        ingestion=None, # type: ignore
        input_references=[],
        scenario_matrix=None, # type: ignore
        dry_run_steps=[],
        evidence_bundle=None, # type: ignore
        area_reports=[],
        risk_register=None, # type: ignore
        release_candidate_audit=None, # type: ignore
        final_freeze_checklist=None, # type: ignore
        final_freeze_boundary=None, # type: ignore
        final_freeze_certificate=None, # type: ignore
        phase160_handoff_contract=None, # type: ignore
        phase160_handoff_package=None, # type: ignore
        phase160_readiness_gate=None, # type: ignore
        phase158_integration_review_ingested=False,
        artifacts_loaded=False,
        inputs_resolved=False,
        scenario_matrix_built=False,
        advanced_dry_run_executed=False,
        evidence_bundle_built=False,
        regression_acceptance_built=False,
        safety_acceptance_built=False,
        system_area_acceptance_built=False,
        release_candidate_audit_built=False,
        release_candidate_risk_register_built=False,
        final_freeze_checklist_built=False,
        final_freeze_boundary_validated=False,
        final_freeze_certificate_built=False,
        phase160_handoff_contract_built=False,
        phase160_handoff_package_built=False,
        phase160_readiness_gate_built=False,
        phase160_readiness_gate_passed=False,
        ready_for_phase160=False,
        research_data_only=True,
        advanced_acceptance_only=True,
        dry_run_only=True,
        local_fixture_only=True,
        deterministic=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        paper_state_mutation_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        telegram_real_send_enabled=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        production_patch_allowed=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        dashboard_started=False,
        daemon_started=False,
        scheduler_enabled=False,
        actual_target_weights_produced=False,
        actual_allocation_produced=False,
        order_size_produced=False,
        capital_deployment_allowed=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_advanced_acceptance_full_review(context: AdvancedAcceptanceContext) -> AdvancedAcceptanceFullReview:
    return AdvancedAcceptanceFullReview(
        review_id=create_advanced_acceptance_full_review_id(),
        created_at_utc=generate_timestamp(),
        report_type=AdvancedAcceptanceReportType.FULL_PHASE159_REVIEW,
        ingestion=context.ingestion,
        context=context,
        release_candidate_audit=context.release_candidate_audit,
        final_freeze_certificate=context.final_freeze_certificate,
        phase160_handoff_package=context.phase160_handoff_package,
        phase160_readiness_gate=context.phase160_readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def advanced_acceptance_full_review_summary(review: AdvancedAcceptanceFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "ready_for_phase160": review.phase160_readiness_gate.ready_for_phase160 if review.phase160_readiness_gate else False,
        "audit_passed": review.release_candidate_audit.audit_passed if review.release_candidate_audit else False,
        "frozen": review.final_freeze_certificate.frozen if review.final_freeze_certificate else False
    }

def advanced_acceptance_limitations_text() -> str:
    return (
        "Phase 159 is strictly an advanced acceptance rehearsal, release candidate audit and final freeze preparation phase.\n"
        "It does NOT represent a deployment approval.\n"
        "It does NOT represent a trading approval.\n"
        "It does NOT contain investment advice.\n"
        "All data and outputs must be treated as dry-run research data."
    )

def advanced_acceptance_full_review_to_text(review: AdvancedAcceptanceFullReview, limit: int = 300) -> str:
    lines = [
        f"Advanced Acceptance Full Review: {review.review_id}",
        advanced_acceptance_limitations_text(),
        f"Ready for Phase 160: {review.phase160_readiness_gate.ready_for_phase160 if review.phase160_readiness_gate else False}"
    ]
    return "\n".join(lines)
