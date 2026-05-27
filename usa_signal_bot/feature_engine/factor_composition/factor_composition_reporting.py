from typing import Any
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureEnrichmentIngestionResult, FeatureGroupDefinition, FeatureGroupProfile,
    FactorComponent, FactorCandidateDefinition, FactorCompositionSpec,
    FeatureCoverageProfile, FeatureRedundancyProfile, FeatureStabilityProfile,
    FeatureSelectionMetadata, FactorReadinessRule, FactorReadinessGate,
    FactorCompositionContext, FactorCompositionFullReview
)
from usa_signal_bot.feature_engine.factor_composition.feature_enrichment_ingestion import feature_enrichment_ingestion_to_text
from usa_signal_bot.feature_engine.factor_composition.feature_group_registry import feature_group_registry_to_text
from usa_signal_bot.feature_engine.factor_composition.feature_group_profiler import feature_group_profiler_to_text
from usa_signal_bot.feature_engine.factor_composition.factor_component_registry import factor_component_registry_to_text
from usa_signal_bot.feature_engine.factor_composition.factor_candidate_registry import factor_candidate_registry_to_text
from usa_signal_bot.feature_engine.factor_composition.factor_composition_specs import factor_composition_spec_to_text
from usa_signal_bot.feature_engine.factor_composition.feature_coverage_analyzer import feature_coverage_to_text
from usa_signal_bot.feature_engine.factor_composition.feature_redundancy_analyzer import feature_redundancy_to_text
from usa_signal_bot.feature_engine.factor_composition.feature_stability_analyzer import feature_stability_to_text
from usa_signal_bot.feature_engine.factor_composition.feature_selection_metadata import feature_selection_metadata_to_text
from usa_signal_bot.feature_engine.factor_composition.factor_readiness_rules import factor_readiness_rules_to_text
from usa_signal_bot.feature_engine.factor_composition.factor_readiness_gate import factor_readiness_gate_to_text
from usa_signal_bot.feature_engine.factor_composition.factor_composition_report import (
    factor_composition_full_review_to_text,
    factor_composition_limitations_text
)

# Wrapping standard functions for export
def feature_group_definition_to_text(item: FeatureGroupDefinition) -> str:
    return f"Group: {item.group_name} ({item.group_kind.value})"

def feature_group_profile_to_text(item: FeatureGroupProfile) -> str:
    return f"Profile for {item.group_name}: Coverage {item.coverage_ratio:.2%}, Quality {item.group_quality.value}"

def factor_component_to_text(item: FactorComponent) -> str:
    return f"Component: {item.component_name} (from {item.source_group_name})"

def factor_candidate_definition_to_text(item: FactorCandidateDefinition) -> str:
    return f"Candidate: {item.factor_name} -> {item.output_column}"

def feature_coverage_profile_to_text(item: FeatureCoverageProfile) -> str:
    return f"Coverage [{item.symbol}]: {item.average_coverage_ratio:.2%} avg"

def feature_redundancy_profile_to_text(item: FeatureRedundancyProfile) -> str:
    return f"Redundancy [{item.symbol}]: Score {item.redundancy_score:.1f}"

def feature_stability_profile_to_text(item: FeatureStabilityProfile) -> str:
    return f"Stability [{item.symbol}]: Score {item.average_stability_score:.1f}"

def factor_readiness_rule_to_text(item: FactorReadinessRule) -> str:
    return f"Rule: {item.name} -> {item.status.value}"

def factor_composition_context_to_text(item: FactorCompositionContext, limit: int = 300) -> str:
    lines = [
        f"Factor Composition Context: {item.context_id}",
        f"Status: {item.status.value}",
        f"Feature Groups Ready: {item.feature_groups_ready}",
        f"Factor Candidates Ready: {item.factor_candidates_ready}",
        f"Ready for Phase 121: {item.ready_for_phase121}"
    ]
    return "\n".join(lines)

def factor_composition_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "Factor Composition Store Summary:",
        f"  Contexts: {summary.get('context_count', 0)}",
        f"  Reviews: {summary.get('review_count', 0)}",
        f"  Feature Groups: {summary.get('feature_group_count', 0)}",
        f"  Factor Candidates: {summary.get('factor_candidate_count', 0)}"
    ]
    return "\n".join(lines)
