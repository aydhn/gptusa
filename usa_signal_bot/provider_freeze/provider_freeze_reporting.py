from typing import Any, Dict
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderGovernanceIngestionResult,
    ProviderFreezeEvidenceItem,
    ProviderExpansionFreezeBundle,
    MultiProviderReviewItem,
    MultiProviderFinalReviewReport,
    DataLayerRehearsalScenario,
    DataLayerRehearsalStep,
    DataLayerRehearsalReport,
    DataLayerOutputContract,
    ProviderFreezeArtifactManifest,
    ProviderFreezeContext,
    ProviderFreezeFullReview
)
from usa_signal_bot.provider_freeze.provider_governance_ingestion import provider_governance_ingestion_to_text
from usa_signal_bot.provider_freeze.freeze_bundle_builder import provider_freeze_bundle_to_text
from usa_signal_bot.provider_freeze.multi_provider_review import multi_provider_review_to_text
from usa_signal_bot.provider_freeze.output_contract_checker import output_contract_to_text
from usa_signal_bot.provider_freeze.freeze_artifact_manifest import provider_freeze_artifact_manifest_to_text
from usa_signal_bot.provider_freeze.provider_freeze_report import provider_freeze_full_review_to_text, provider_freeze_limitations_text

def provider_governance_ingestion_result_to_text(item: ProviderGovernanceIngestionResult) -> str:
    return provider_governance_ingestion_to_text(item)

def provider_freeze_evidence_item_to_text(item: ProviderFreezeEvidenceItem) -> str:
    return f"Evidence: {item.evidence_name} (Valid: {item.valid}, Available: {item.available})"

def provider_expansion_freeze_bundle_to_text(item: ProviderExpansionFreezeBundle, limit: int = 300) -> str:
    return provider_freeze_bundle_to_text(item, limit)

def multi_provider_review_item_to_text(item: MultiProviderReviewItem) -> str:
    return f"Review Item: {item.name} [{item.status.value}] - {item.rationale}"

def multi_provider_final_review_report_to_text(item: MultiProviderFinalReviewReport, limit: int = 300) -> str:
    return multi_provider_review_to_text(item, limit)

def data_layer_rehearsal_scenario_to_text(item: DataLayerRehearsalScenario) -> str:
    return f"Scenario: {item.name} - {item.description}"

def data_layer_rehearsal_step_to_text(item: DataLayerRehearsalStep) -> str:
    return f"Step: {item.step_name} [{item.status.value}] - {item.message}"

def data_layer_rehearsal_report_to_text(item: DataLayerRehearsalReport, limit: int = 300) -> str:
    lines = [
        f"Rehearsal Report: {item.rehearsal_id}",
        f"Passed: {item.rehearsal_passed}",
        f"Scenarios: {item.total_scenarios} (Passed: {item.passed_scenarios}, Failed: {item.failed_scenarios})"
    ]
    for step in item.steps[:limit]:
        lines.append(f"  - {data_layer_rehearsal_step_to_text(step)}")
    return "\n".join(lines)

def data_layer_output_contract_to_text(item: DataLayerOutputContract) -> str:
    return output_contract_to_text(item)

def provider_freeze_artifact_manifest_to_text(item: ProviderFreezeArtifactManifest, limit: int = 200) -> str:
    return provider_freeze_artifact_manifest_to_text(item, limit)

def provider_freeze_context_to_text(item: ProviderFreezeContext, limit: int = 300) -> str:
    lines = [
        f"Provider Freeze Context: {item.context_id}",
        f"Status: {item.status.value}",
        f"Ready for Phase 115: {item.ready_for_phase115}",
        f"Execution Safe: {not item.activation_allowed and not item.broker_used and not item.produces_trade_signal}"
    ]
    return "\n".join(lines)

def provider_freeze_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return "Store Summary:\n" + "\n".join(f"  {k}: {v}" for k, v in summary.items())
