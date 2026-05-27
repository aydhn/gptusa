"""Freeze Preparation Reporting Helpers."""
from typing import Any
from .phase124_models import (
    ExplainabilityIngestionResult,
    ArtifactChainReference,
    ArtifactChainIntegrityResult,
    IntegrationRehearsalStep,
    IntegrationRehearsalResult,
    ReportQaAcceptanceRule,
    ReportQaAcceptanceGate,
    FreezeCandidateArtifact,
    FreezeCandidateManifest,
    FreezeReadinessRule,
    FreezePreparationGate,
    FreezePreparationContext,
    FreezePreparationFullReview
)
from .explainability_ingestion import explainability_ingestion_to_text
from .artifact_chain_loader import artifact_chain_loader_to_text
from .artifact_chain_integrity import artifact_chain_integrity_to_text
from .integration_rehearsal_runner import integration_rehearsal_to_text
from .report_qa_acceptance import report_qa_acceptance_to_text
from .freeze_candidate_manifest import freeze_candidate_manifest_to_text
from .freeze_readiness_gate import freeze_readiness_gate_to_text
from .freeze_preparation_report import freeze_preparation_full_review_to_text, freeze_preparation_limitations_text

def explainability_ingestion_result_to_text(item: ExplainabilityIngestionResult) -> str:
    return explainability_ingestion_to_text(item)

def artifact_chain_reference_to_text(item: ArtifactChainReference) -> str:
    return f"Reference {item.reference_id}"

def artifact_chain_integrity_result_to_text(item: ArtifactChainIntegrityResult, limit: int = 300) -> str:
    return artifact_chain_integrity_to_text(item, limit)

def integration_rehearsal_step_to_text(item: IntegrationRehearsalStep) -> str:
    return f"Step {item.step_id}"

def integration_rehearsal_result_to_text(item: IntegrationRehearsalResult, limit: int = 300) -> str:
    return integration_rehearsal_to_text(item, limit)

def report_qa_acceptance_rule_to_text(item: ReportQaAcceptanceRule) -> str:
    return f"Rule {item.rule_id}"

def report_qa_acceptance_gate_to_text(item: ReportQaAcceptanceGate, limit: int = 300) -> str:
    return report_qa_acceptance_to_text(item, limit)

def freeze_candidate_artifact_to_text(item: FreezeCandidateArtifact) -> str:
    return f"Artifact {item.artifact_id}"

def freeze_candidate_manifest_to_text(item: FreezeCandidateManifest, limit: int = 300) -> str:
    return freeze_candidate_manifest_to_text(item, limit)

def freeze_readiness_rule_to_text(item: FreezeReadinessRule) -> str:
    return f"Readiness Rule {item.rule_id}"

def freeze_preparation_gate_to_text(item: FreezePreparationGate, limit: int = 300) -> str:
    return freeze_readiness_gate_to_text(item, limit)

def freeze_preparation_context_to_text(item: FreezePreparationContext, limit: int = 300) -> str:
    return f"Context {item.context_id} Ready: {item.ready_for_phase125}"

def freeze_preparation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
