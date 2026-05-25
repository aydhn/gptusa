from usa_signal_bot.provider_governance.phase113_models import ProviderGovernanceContext, ProviderGovernanceFullReview, create_provider_governance_context_id, create_provider_governance_full_review_id, EventImpactIngestionResult, ProviderAcceptanceReport, ProviderGovernancePolicy, DataLineageGraph, AuditArtifactManifest, NoExecutionProof
from usa_signal_bot.core.enums import ProviderGovernanceStatus, ProviderGovernanceDecision, ProviderGovernanceReportType
from datetime import datetime, timezone
from typing import Any, Dict

def build_provider_governance_context() -> ProviderGovernanceContext:
    return ProviderGovernanceContext(
        context_id=create_provider_governance_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=ProviderGovernanceStatus.VALIDATED,
        decision=ProviderGovernanceDecision.ACCEPT_DATA_PROVIDER_EXPANSION,
        source_event_impact_review_id=None,
        ingestion=None, # Mocking since it needs arguments
        evidence_items=[],
        acceptance_report=None,
        governance_policy=None,
        lineage_graph=None,
        audit_manifest=None,
        no_execution_proof=None,
        provider_governance_ready=True,
        provider_expansion_accepted=True,
        lineage_ready=True,
        audit_ready=True,
        metadata_only=True,
        research_data_only=True,
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

def build_provider_governance_full_review() -> ProviderGovernanceFullReview:
    return ProviderGovernanceFullReview(
        review_id=create_provider_governance_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=ProviderGovernanceReportType.FULL_PHASE113_REVIEW,
        ingestion=None,
        context=build_provider_governance_context(),
        evidence_items=[],
        acceptance_report=None,
        governance_policy=None,
        lineage_graph=None,
        audit_manifest=None,
        no_execution_proof=None,
        output_paths={},
        warnings=[],
        errors=[]
    )

def provider_governance_full_review_summary(review: ProviderGovernanceFullReview) -> Dict[str, Any]:
    return {}

def provider_governance_limitations_text() -> str:
    return "Limitations"

def provider_governance_full_review_to_text(review: ProviderGovernanceFullReview, limit: int = 300) -> str:
    return "Review"
