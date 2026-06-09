from typing import Any, Dict, List
from usa_signal_bot.release.phase159_models import (
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
    AdvancedAcceptanceContext,
    AdvancedAcceptanceFullReview
)

def phase158_integration_ingestion_result_to_text(item: Phase158IntegrationIngestionResult) -> str:
    from usa_signal_bot.release.phase158_integration_ingestion import phase158_integration_ingestion_to_text
    return phase158_integration_ingestion_to_text(item)

def advanced_acceptance_input_reference_to_text(item: AdvancedAcceptanceInputReference) -> str:
    return f"{item.source_artifact_name} ({item.input_kind.value}): Valid={item.valid}"

def acceptance_scenario_matrix_to_text(item: AcceptanceScenarioMatrix, limit: int = 300) -> str:
    from usa_signal_bot.release.acceptance_scenario_matrix import acceptance_scenario_matrix_to_text as to_text
    return to_text(item, limit)

def advanced_dry_run_steps_to_text(items: List[AdvancedDryRunStep], limit: int = 300) -> str:
    from usa_signal_bot.release.advanced_dry_run_rehearsal_executor import advanced_dry_run_rehearsal_to_text as to_text
    return to_text(items, limit)

def acceptance_evidence_bundle_to_text(item: AcceptanceEvidenceBundle, limit: int = 300) -> str:
    from usa_signal_bot.release.acceptance_evidence_bundle import acceptance_evidence_bundle_to_text as to_text
    return to_text(item, limit)

def acceptance_area_report_to_text(item: AcceptanceAreaReport, limit: int = 300) -> str:
    lines = [f"{item.title} [{item.status.value}]"]
    for f in item.findings[:limit]:
        lines.append(f" - {f}")
    return "\n".join(lines)

def release_candidate_risk_register_to_text(item: ReleaseCandidateRiskRegister, limit: int = 300) -> str:
    from usa_signal_bot.release.release_candidate_risk_register import release_candidate_risk_register_to_text as to_text
    return to_text(item, limit)

def release_candidate_audit_to_text(item: ReleaseCandidateAudit, limit: int = 300) -> str:
    from usa_signal_bot.release.release_candidate_audit import release_candidate_audit_to_text as to_text
    return to_text(item, limit)

def final_freeze_checklist_to_text(item: FinalFreezeChecklist, limit: int = 300) -> str:
    from usa_signal_bot.release.final_freeze_checklist import final_freeze_checklist_to_text as to_text
    return to_text(item, limit)

def final_freeze_boundary_to_text(item: FinalFreezeBoundaryResult, limit: int = 300) -> str:
    from usa_signal_bot.release.final_freeze_boundary import final_freeze_boundary_to_text as to_text
    return to_text(item, limit)

def final_freeze_certificate_to_text(item: FinalFreezeCertificate, limit: int = 300) -> str:
    from usa_signal_bot.release.final_freeze_certificate import final_freeze_certificate_to_text as to_text
    return to_text(item, limit)

def phase160_handoff_contract_to_text(item: Phase160HandoffContract, limit: int = 300) -> str:
    from usa_signal_bot.release.phase160_handoff_contract import phase160_handoff_contract_to_text as to_text
    return to_text(item, limit)

def phase160_handoff_package_to_text(item: Phase160HandoffPackage, limit: int = 300) -> str:
    from usa_signal_bot.release.phase160_handoff_package import phase160_handoff_package_to_text as to_text
    return to_text(item, limit)

def phase160_readiness_gate_to_text(item: Phase160ReadinessGate, limit: int = 300) -> str:
    from usa_signal_bot.release.phase160_readiness_gate import phase160_readiness_gate_to_text as to_text
    return to_text(item, limit)

def advanced_acceptance_context_to_text(item: AdvancedAcceptanceContext, limit: int = 300) -> str:
    return f"Advanced Acceptance Context: {item.context_id} [Status: {item.status.value}]"

def advanced_acceptance_full_review_to_text(item: AdvancedAcceptanceFullReview, limit: int = 300) -> str:
    from usa_signal_bot.release.advanced_acceptance_report import advanced_acceptance_full_review_to_text as to_text
    return to_text(item, limit)

def advanced_acceptance_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary.get('reviews', 0)} reviews"

def advanced_acceptance_limitations_text() -> str:
    from usa_signal_bot.release.advanced_acceptance_report import advanced_acceptance_limitations_text as to_text
    return to_text()
