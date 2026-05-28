from typing import Any, List
from usa_signal_bot.core.enums import RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    RegimeFoundationContext,
    RegimeResearchInputBundle,
    MarketStateDatasetContract,
    RegimeLabelTaxonomy
)
from usa_signal_bot.regime_classification.foundation.market_state_dataset_schema import validate_market_state_dataset_contract
from usa_signal_bot.regime_classification.foundation.regime_taxonomy_validator import validate_regime_taxonomy
from usa_signal_bot.regime_classification.foundation.regime_non_activation_boundary import check_safe_columns, check_safe_language

def regime_foundation_text_has_trade_or_execution_language(text: str) -> bool:
    return not check_safe_language(text)

def validate_regime_columns_safety(columns: List[str]) -> List[str]:
    errors = []
    if not check_safe_columns(columns):
        errors.append("Forbidden columns found in column list")
    return errors

def validate_regime_input_bundle_safety(bundle: RegimeResearchInputBundle) -> List[str]:
    errors = []
    if not bundle.research_data_only:
        errors.append("Bundle is not marked as research_data_only")
    if bundle.activation_allowed or bundle.strategy_activation_allowed or bundle.deployment_allowed:
        errors.append("Bundle allows activation or deployment")
    if bundle.produces_trade_signal or bundle.produces_order_decision or bundle.produces_portfolio_weights:
        errors.append("Bundle produces execution outputs")
    if bundle.investment_advice:
        errors.append("Bundle contains investment advice")
    return errors

def validate_market_state_dataset_contract_safety(contract: MarketStateDatasetContract) -> List[str]:
    return validate_market_state_dataset_contract(contract)

def validate_regime_taxonomy_safety(taxonomy: RegimeLabelTaxonomy) -> List[str]:
    return validate_regime_taxonomy(taxonomy)

def validate_regime_foundation_context_safety(context: RegimeFoundationContext) -> List[str]:
    errors = []
    if context.activation_allowed or context.strategy_activation_allowed or context.deployment_allowed:
        errors.append("Context illegally allows activation or deployment")
    if context.active_paper_enabled or context.paper_state_mutation_enabled:
        errors.append("Context illegally enables paper trading or mutation")
    if context.broker_execution_enabled or context.order_creation_enabled:
        errors.append("Context illegally enables broker execution or order creation")
    if context.telegram_real_send_enabled:
        errors.append("Context illegally enables real Telegram messages")
    if context.scraping_enabled or context.html_parse_enabled:
        errors.append("Context illegally enables scraping or HTML parsing")
    if context.paid_api_enabled:
        errors.append("Context illegally enables paid APIs")
    if context.network_used or context.paid_api_used or context.scraping_used or context.html_parsing_used or context.broker_used or context.order_created or context.paper_state_mutated or context.telegram_real_sent or context.dashboard_started:
        errors.append("Context indicates illegal actions were performed")
    if context.produces_trade_signal or context.produces_order_decision or context.produces_portfolio_weights:
        errors.append("Context produces execution outputs")
    if context.investment_advice:
        errors.append("Context provides investment advice")
    if not context.boundary.boundary_passed and context.ready_for_phase127:
        errors.append("Context marked ready for Phase 127 without passing non-activation boundary")

    return errors

def collect_regime_foundation_risk_flags(context: RegimeFoundationContext | None = None) -> List[RegimeFoundationRiskFlag]:
    flags = set()
    if context:
        flags.update(context.risk_flags)
        if not context.ingestion.valid_for_phase126:
            flags.add(RegimeFoundationRiskFlag.FINAL_CLOSURE_REVIEW_INVALID)
        if not context.input_bundle.bundle_valid:
            flags.add(RegimeFoundationRiskFlag.FROZEN_ARTIFACTS_MISSING)
        if context.dataset_contract.errors:
            flags.add(RegimeFoundationRiskFlag.MARKET_STATE_DATASET_SCHEMA_INVALID)
        if context.taxonomy.errors:
            flags.add(RegimeFoundationRiskFlag.REGIME_TAXONOMY_INVALID)
        if not context.boundary.boundary_passed:
            flags.add(RegimeFoundationRiskFlag.NON_ACTIVATION_BOUNDARY_FAILED)

    return list(flags)

def regime_foundation_safety_summary(errors: List[str]) -> dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def regime_foundation_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Safety Validation: PASSED"
    lines = ["Safety Validation: FAILED", "Errors:"]
    for err in errors:
        lines.append(f"  - {err}")
    return "\n".join(lines)
