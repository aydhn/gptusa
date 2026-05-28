from typing import Any
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    FinalClosureIngestionResult,
    FrozenArtifactReference,
    RegimeResearchInputBundle,
    MarketStateColumnContract,
    MarketStateDatasetContract,
    MarketStateDatasetSkeleton,
    RegimeLabelDefinition,
    RegimeLabelTaxonomy,
    RegimeBoundaryRule,
    RegimeNonActivationBoundaryResult,
    RegimeFoundationContext,
    RegimeFoundationFullReview
)
from usa_signal_bot.regime_classification.foundation.final_closure_ingestion import final_closure_ingestion_to_text
from usa_signal_bot.regime_classification.foundation.frozen_artifact_loader import frozen_artifact_loader_to_text
from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import market_state_dataset_contract_to_text
from usa_signal_bot.regime_classification.foundation.market_state_dataset_skeleton import market_state_dataset_skeleton_to_text
from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import regime_label_taxonomy_to_text
from usa_signal_bot.regime_classification.foundation.regime_non_activation_boundary import regime_boundary_to_text
from usa_signal_bot.regime_classification.foundation.regime_foundation_report import regime_foundation_full_review_to_text, regime_foundation_limitations_text

def final_closure_ingestion_result_to_text(item: FinalClosureIngestionResult) -> str:
    return final_closure_ingestion_to_text(item)

def frozen_artifact_reference_to_text(item: FrozenArtifactReference) -> str:
    return f"Artifact Reference: {item.artifact_name} (Kind: {item.artifact_kind})"

def regime_research_input_bundle_to_text(item: RegimeResearchInputBundle, limit: int = 300) -> str:
    return frozen_artifact_loader_to_text(item, limit)

def market_state_column_contract_to_text(item: MarketStateColumnContract) -> str:
    return f"Column: {item.column_name} (Kind: {item.column_kind.value}, Dtype: {item.dtype})"

def market_state_dataset_contract_to_text_helper(item: MarketStateDatasetContract, limit: int = 300) -> str:
    return market_state_dataset_contract_to_text(item, limit)

def market_state_dataset_skeleton_to_text_helper(item: MarketStateDatasetSkeleton, limit: int = 200) -> str:
    return market_state_dataset_skeleton_to_text(item, limit)

def regime_label_definition_to_text(item: RegimeLabelDefinition) -> str:
    return f"Label: {item.label_name} (Kind: {item.label_kind.value})"

def regime_label_taxonomy_to_text_helper(item: RegimeLabelTaxonomy, limit: int = 300) -> str:
    return regime_label_taxonomy_to_text(item, limit)

def regime_boundary_rule_to_text(item: RegimeBoundaryRule) -> str:
    return f"Rule: {item.name} - Passed: {item.passed}"

def regime_non_activation_boundary_result_to_text(item: RegimeNonActivationBoundaryResult, limit: int = 300) -> str:
    return regime_boundary_to_text(item, limit)

def regime_foundation_context_to_text(item: RegimeFoundationContext, limit: int = 300) -> str:
    lines = [
        f"Regime Foundation Context: {item.context_id}",
        f"Status: {item.status.value}",
        f"Ready for Phase 127: {item.ready_for_phase127}"
    ]
    if item.errors:
        lines.append("Errors:")
        for err in item.errors:
            lines.append(f"  - {err}")
    return "\n".join(lines)

def regime_foundation_full_review_to_text_helper(item: RegimeFoundationFullReview, limit: int = 300) -> str:
    return regime_foundation_full_review_to_text(item, limit)

def regime_foundation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in summary.items()])
