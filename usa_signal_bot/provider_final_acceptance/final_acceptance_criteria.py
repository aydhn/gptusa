from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFinalAcceptanceCriterionKind,
    ProviderFinalAcceptanceCriterion,
    ProviderFinalAcceptanceCriterionStatus,
    ProviderFreezeIngestionResult,
    create_provider_final_acceptance_criterion_id,
    _utc_now
)

def required_provider_final_acceptance_criteria() -> list[ProviderFinalAcceptanceCriterionKind]:
    return [
        ProviderFinalAcceptanceCriterionKind.PHASE106_PROVIDER_ABSTRACTION_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE107_PROVIDER_RUNTIME_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE108_PROVIDER_CACHE_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE109_PROVIDER_QUALITY_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE110_PROVIDER_ORCHESTRATION_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE111_EVENT_METADATA_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE112_EVENT_IMPACT_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE113_GOVERNANCE_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.PHASE114_FREEZE_ACCEPTED,
        ProviderFinalAcceptanceCriterionKind.FINAL_NO_EXECUTION_BOUNDARY,
        ProviderFinalAcceptanceCriterionKind.FINAL_NO_SCRAPING_BOUNDARY,
        ProviderFinalAcceptanceCriterionKind.FINAL_NO_PAID_API_BOUNDARY,
        ProviderFinalAcceptanceCriterionKind.FINAL_NO_BROKER_ORDER_BOUNDARY,
        ProviderFinalAcceptanceCriterionKind.FINAL_DATA_CONTRACT_READY,
        ProviderFinalAcceptanceCriterionKind.PHASE116_KICKOFF_READY
    ]

def build_final_acceptance_criterion(kind: ProviderFinalAcceptanceCriterionKind, ingestion: ProviderFreezeIngestionResult) -> ProviderFinalAcceptanceCriterion:
    passed = False
    status = ProviderFinalAcceptanceCriterionStatus.UNKNOWN
    rationale = ""

    if not ingestion.valid_for_phase115:
        status = ProviderFinalAcceptanceCriterionStatus.FAIL
        rationale = "Ingestion is not valid for Phase 115"
    else:
        status = ProviderFinalAcceptanceCriterionStatus.PASS
        passed = True
        rationale = f"Evaluated positively via phase 114 ingestion: {ingestion.ingestion_id}"

    # For safety constraints
    if kind == ProviderFinalAcceptanceCriterionKind.FINAL_NO_EXECUTION_BOUNDARY:
        if ingestion.activation_allowed or ingestion.active_paper_enabled:
            passed = False
            status = ProviderFinalAcceptanceCriterionStatus.FAIL
            rationale = "Execution boundary violated"
    elif kind == ProviderFinalAcceptanceCriterionKind.FINAL_NO_SCRAPING_BOUNDARY:
        if ingestion.scraping_enabled or ingestion.html_parse_enabled:
            passed = False
            status = ProviderFinalAcceptanceCriterionStatus.FAIL
            rationale = "Scraping boundary violated"
    elif kind == ProviderFinalAcceptanceCriterionKind.FINAL_NO_PAID_API_BOUNDARY:
        if ingestion.paid_api_enabled:
            passed = False
            status = ProviderFinalAcceptanceCriterionStatus.FAIL
            rationale = "Paid API boundary violated"
    elif kind == ProviderFinalAcceptanceCriterionKind.FINAL_NO_BROKER_ORDER_BOUNDARY:
        if ingestion.broker_execution_enabled or ingestion.order_creation_enabled:
            passed = False
            status = ProviderFinalAcceptanceCriterionStatus.FAIL
            rationale = "Broker/Order boundary violated"

    return ProviderFinalAcceptanceCriterion(
        criterion_id=create_provider_final_acceptance_criterion_id(),
        created_at_utc=_utc_now(),
        criterion_kind=kind,
        name=kind.value,
        status=status,
        required=kind in required_provider_final_acceptance_criteria(),
        passed=passed,
        rationale=rationale,
        evidence_refs=[ingestion.ingestion_id] if ingestion.ingestion_id else [],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_final_acceptance_criteria(ingestion: ProviderFreezeIngestionResult) -> list[ProviderFinalAcceptanceCriterion]:
    return [build_final_acceptance_criterion(k, ingestion) for k in required_provider_final_acceptance_criteria()]

def final_acceptance_criteria_summary(criteria: list[ProviderFinalAcceptanceCriterion]) -> dict[str, Any]:
    return {
        "total": len(criteria),
        "passed": sum(1 for c in criteria if c.passed),
        "failed": sum(1 for c in criteria if not c.passed and c.status == ProviderFinalAcceptanceCriterionStatus.FAIL)
    }

def final_acceptance_criteria_to_text(criteria: list[ProviderFinalAcceptanceCriterion], limit: int = 200) -> str:
    summary = final_acceptance_criteria_summary(criteria)
    return f"Criteria: {summary['passed']}/{summary['total']} passed."
