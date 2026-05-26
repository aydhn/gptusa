from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFreezeIngestionResult,
    ProviderFinalAcceptanceCriterion,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureItem,
    ProviderLayerClosureBundle,
    FeatureFactorDataContract,
    FeatureFactorKickoffRule,
    FeatureFactorKickoffAssertion,
    FeatureFactorEngineKickoffGate,
    ProviderFinalAcceptanceContext,
    ProviderFinalAcceptanceFullReview
)
from usa_signal_bot.provider_final_acceptance.provider_freeze_ingestion import provider_freeze_ingestion_to_text
from usa_signal_bot.provider_final_acceptance.final_acceptance_checker import data_provider_final_acceptance_report_to_text
from usa_signal_bot.provider_final_acceptance.provider_layer_closure import provider_layer_closure_to_text
from usa_signal_bot.provider_final_acceptance.final_data_contract_checker import feature_factor_data_contract_to_text
from usa_signal_bot.provider_final_acceptance.feature_factor_kickoff_gate import feature_factor_kickoff_gate_to_text
from usa_signal_bot.provider_final_acceptance.final_acceptance_report import provider_final_acceptance_full_review_to_text, provider_final_acceptance_limitations_text

def provider_final_acceptance_criterion_to_text(item: ProviderFinalAcceptanceCriterion) -> str:
    return f"Criterion {item.name}: {item.status}"

def provider_layer_closure_item_to_text(item: ProviderLayerClosureItem) -> str:
    return f"Closure Item {item.closure_name}: {item.status}"

def feature_factor_kickoff_rule_to_text(item: FeatureFactorKickoffRule) -> str:
    return f"Rule {item.rule_name}: {item.status}"

def feature_factor_kickoff_assertion_to_text(item: FeatureFactorKickoffAssertion) -> str:
    return f"Assertion {item.assertion_name}: {item.status}"

def provider_final_acceptance_context_to_text(item: ProviderFinalAcceptanceContext, limit: int = 300) -> str:
    return f"Context [{item.status}] - Ready for 116: {item.ready_for_phase116}"

def final_acceptance_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews_count']} reviews."
