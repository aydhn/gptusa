from typing import Any, Dict
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FreezePreparationIngestionResult, FinalClosureArtifactReference, FinalClosureRule,
    FinalClosureResult, FinalClosureManifest, FreezeSealMetadata,
    EngineReadinessCertificate, Phase126KickoffRequirement, Phase126KickoffGate,
    FinalClosureAudit, FinalClosureContext, FinalClosureFullReview
)
from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import freeze_preparation_ingestion_to_text as fp_to_text
from usa_signal_bot.feature_engine.final_closure.final_closure_checks import final_closure_checks_to_text
from usa_signal_bot.feature_engine.final_closure.freeze_seal_builder import freeze_seal_to_text
from usa_signal_bot.feature_engine.final_closure.engine_readiness_certificate import engine_readiness_certificate_to_text as erc_to_text
from usa_signal_bot.feature_engine.final_closure.phase126_kickoff_gate import phase126_kickoff_gate_to_text as p126_to_text
from usa_signal_bot.feature_engine.final_closure.final_closure_report import final_closure_full_review_to_text as fc_to_text
from usa_signal_bot.feature_engine.final_closure.final_closure_report import final_closure_limitations_text as fclt

def freeze_preparation_ingestion_result_to_text(item: FreezePreparationIngestionResult) -> str:
    return fp_to_text(item)

def final_closure_artifact_reference_to_text(item: FinalClosureArtifactReference) -> str:
    return f"ArtifactRef({item.artifact_name}): Available={item.available}"

def final_closure_rule_to_text(item: FinalClosureRule) -> str:
    return f"Rule({item.name}): {item.status.value}"

def final_closure_result_to_text(item: FinalClosureResult, limit: int = 300) -> str:
    return final_closure_checks_to_text(item, limit)

def final_closure_manifest_to_text(item: FinalClosureManifest, limit: int = 300) -> str:
    return f"Manifest({item.manifest_id}): Valid={item.final_manifest_valid}"

def freeze_seal_metadata_to_text(item: FreezeSealMetadata, limit: int = 200) -> str:
    return freeze_seal_to_text(item, limit)

def engine_readiness_certificate_to_text(item: EngineReadinessCertificate, limit: int = 300) -> str:
    return erc_to_text(item, limit)

def phase126_kickoff_requirement_to_text(item: Phase126KickoffRequirement) -> str:
    return f"Requirement({item.name}): Passed={item.passed}"

def phase126_kickoff_gate_to_text(item: Phase126KickoffGate, limit: int = 300) -> str:
    return p126_to_text(item, limit)

def final_closure_audit_to_text(item: FinalClosureAudit) -> str:
    return f"Audit({item.audit_id}): LocalOnly={item.local_only}"

def final_closure_context_to_text(item: FinalClosureContext, limit: int = 300) -> str:
    return f"Context({item.context_id}): Closed={item.feature_factor_engine_final_closed}"

def final_closure_full_review_to_text(item: FinalClosureFullReview, limit: int = 300) -> str:
    return fc_to_text(item, limit)

def final_closure_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews']} reviews"

def final_closure_limitations_text() -> str:
    return fclt()
