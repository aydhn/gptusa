from typing import Any, Dict
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeArtifactChainReference,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureRule,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFinalSafetyAudit,
    MLInputContract,
    MLKickoffReadinessGate,
    RegimeFinalClosureContext,
    RegimeFinalClosureFullReview
)

def regime_research_freeze_ingestion_result_to_text(item: RegimeResearchFreezeIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id}"

def regime_artifact_chain_reference_to_text(item: RegimeArtifactChainReference) -> str:
    return f"Reference {item.reference_id}"

def regime_artifact_chain_validation_result_to_text(item: RegimeArtifactChainValidationResult, limit: int = 300) -> str:
    return f"Validation {item.validation_id}"

def regime_final_closure_rule_to_text(item: RegimeFinalClosureRule) -> str:
    return f"Rule {item.rule_id}"

def regime_final_closure_result_to_text(item: RegimeFinalClosureResult, limit: int = 300) -> str:
    return f"Closure Result {item.closure_result_id}"

def regime_freeze_seal_to_text(item: RegimeFreezeSeal, limit: int = 300) -> str:
    return f"Seal {item.seal_id}"

def regime_final_safety_audit_to_text(item: RegimeFinalSafetyAudit, limit: int = 300) -> str:
    return f"Audit {item.audit_id}"

def ml_input_contract_to_text(item: MLInputContract, limit: int = 300) -> str:
    return f"Contract {item.contract_id}"

def ml_kickoff_readiness_gate_to_text(item: MLKickoffReadinessGate, limit: int = 300) -> str:
    return f"Gate {item.gate_id}"

def regime_final_closure_context_to_text(item: RegimeFinalClosureContext, limit: int = 300) -> str:
    return f"Context {item.context_id}"

def regime_final_closure_full_review_to_text(item: RegimeFinalClosureFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}"

def final_closure_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return str(summary)

def regime_final_closure_limitations_text() -> str:
    from usa_signal_bot.regime_classification.final_closure.final_closure_report import regime_final_closure_limitations_text as original
    return original()
