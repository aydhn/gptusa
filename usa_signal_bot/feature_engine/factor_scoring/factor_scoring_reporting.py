from typing import Any
from usa_signal_bot.feature_engine.factor_scoring.phase121_models import *

def factor_composition_ingestion_result_to_text(item: FactorCompositionIngestionResult) -> str:
    return str(item)

def factor_scoring_spec_to_text(item: FactorScoringSpec) -> str:
    return str(item)

def factor_scoring_request_to_text(item: FactorScoringRequest) -> str:
    return str(item)

def factor_normalization_result_to_text(item: FactorNormalizationResult) -> str:
    return str(item)

def factor_diagnostics_profile_to_text(item: FactorDiagnosticsProfile) -> str:
    return str(item)

def factor_scoring_result_to_text(item: FactorScoringResult) -> str:
    return str(item)

def factor_table_schema_to_text(item: FactorTableSchema) -> str:
    return str(item)

def factor_table_result_to_text(item: FactorTableResult) -> str:
    return str(item)

def factor_computation_audit_to_text(item: FactorComputationAudit) -> str:
    return str(item)

def factor_scoring_context_to_text(item: FactorScoringContext, limit: int = 300) -> str:
    return str(item)

def factor_scoring_full_review_to_text(item: FactorScoringFullReview, limit: int = 300) -> str:
    return str(item)

def factor_scoring_store_summary_to_text(summary: dict[str, Any]) -> str:
    return str(summary)

def factor_scoring_limitations_text() -> str:
    return "Phase 121 limitations text"
