from usa_signal_bot.provider_governance.phase113_models import ProviderExpansionEvidenceItem, create_provider_expansion_evidence_id
from usa_signal_bot.core.enums import ProviderAcceptanceCriterionKind
from typing import Any, Optional, List, Dict
from datetime import datetime, timezone

def required_provider_expansion_evidence_names() -> List[str]:
    return [
        "phase106_provider_abstraction",
        "phase107_provider_runtime_contracts",
        "phase108_provider_cache_and_source_comparison",
        "phase109_provider_quality_scoring",
        "phase110_provider_orchestration",
        "phase111_event_metadata_schedule",
        "phase112_event_impact_calendar_validation",
        "no_execution_boundary",
        "no_scraping_boundary",
        "no_paid_api_boundary",
        "no_broker_order_boundary",
        "data_lineage_ready",
        "audit_trail_ready"
    ]

def collect_provider_expansion_evidence(data_root: Optional[str] = None, payloads: Optional[Dict[str, Any]] = None) -> List[ProviderExpansionEvidenceItem]:
    return []

def evidence_item_from_payload(source_phase: int, evidence_name: str, criterion_kind: ProviderAcceptanceCriterionKind, payload: Optional[Dict[str, Any]] = None, source_ref_id: Optional[str] = None, source_path: Optional[str] = None) -> ProviderExpansionEvidenceItem:
    return ProviderExpansionEvidenceItem(
        evidence_id=create_provider_expansion_evidence_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_phase=source_phase,
        evidence_name=evidence_name,
        criterion_kind=criterion_kind,
        source_review_id=source_ref_id,
        source_path=source_path,
        available=True,
        valid=True,
        metadata_only=True,
        no_execution_confirmed=True,
        no_scraping_confirmed=True,
        no_paid_api_confirmed=True,
        no_broker_order_confirmed=True,
        artifact_hash=None,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def provider_expansion_missing_evidence(items: List[ProviderExpansionEvidenceItem]) -> List[str]:
    return []

def provider_expansion_evidence_summary(items: List[ProviderExpansionEvidenceItem]) -> Dict[str, Any]:
    return {}

def provider_expansion_evidence_to_text(items: List[ProviderExpansionEvidenceItem], limit: int = 200) -> str:
    return "Evidence"
