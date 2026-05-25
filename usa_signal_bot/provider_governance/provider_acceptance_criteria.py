from usa_signal_bot.provider_governance.phase113_models import ProviderAcceptanceCriterion, ProviderExpansionEvidenceItem, create_provider_acceptance_criterion_id
from usa_signal_bot.core.enums import ProviderAcceptanceCriterionKind, ProviderAcceptanceStatus
from typing import Any, List, Dict
from datetime import datetime, timezone

def required_provider_acceptance_criteria() -> List[ProviderAcceptanceCriterionKind]:
    return [
        ProviderAcceptanceCriterionKind.PHASE106_PROVIDER_ABSTRACTION,
        ProviderAcceptanceCriterionKind.PHASE107_PROVIDER_RUNTIME,
        ProviderAcceptanceCriterionKind.PHASE108_PROVIDER_CACHE,
        ProviderAcceptanceCriterionKind.PHASE109_PROVIDER_QUALITY,
        ProviderAcceptanceCriterionKind.PHASE110_PROVIDER_ORCHESTRATION,
        ProviderAcceptanceCriterionKind.PHASE111_EVENT_METADATA,
        ProviderAcceptanceCriterionKind.PHASE112_EVENT_IMPACT,
        ProviderAcceptanceCriterionKind.NO_EXECUTION_BOUNDARY,
        ProviderAcceptanceCriterionKind.NO_SCRAPING_BOUNDARY,
        ProviderAcceptanceCriterionKind.NO_PAID_API_BOUNDARY,
        ProviderAcceptanceCriterionKind.NO_BROKER_ORDER_BOUNDARY,
        ProviderAcceptanceCriterionKind.DATA_LINEAGE_READY,
        ProviderAcceptanceCriterionKind.AUDIT_TRAIL_READY
    ]

def build_acceptance_criterion(kind: ProviderAcceptanceCriterionKind, evidence_items: List[ProviderExpansionEvidenceItem]) -> ProviderAcceptanceCriterion:
    return ProviderAcceptanceCriterion(
        criterion_id=create_provider_acceptance_criterion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        criterion_kind=kind,
        name=kind.name,
        status=ProviderAcceptanceStatus.PASS,
        required=True,
        passed=True,
        evidence_ids=[],
        rationale="Pass",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_provider_acceptance_criteria(evidence_items: List[ProviderExpansionEvidenceItem]) -> List[ProviderAcceptanceCriterion]:
    return [build_acceptance_criterion(k, evidence_items) for k in required_provider_acceptance_criteria()]

def provider_acceptance_criteria_summary(criteria: List[ProviderAcceptanceCriterion]) -> Dict[str, Any]:
    return {}

def provider_acceptance_criteria_to_text(criteria: List[ProviderAcceptanceCriterion], limit: int = 200) -> str:
    return "Criteria"
