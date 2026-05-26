from typing import Any
from usa_signal_bot.core.enums import FeatureOutputKind, FeatureBlockedOutputKind
from usa_signal_bot.feature_engine.phase116_models import FeatureComputationResult, FeatureOutputSchema

def allowed_feature_output_kinds() -> list[FeatureOutputKind]:
    return [
        FeatureOutputKind.FEATURE_METADATA,
        FeatureOutputKind.FEATURE_SCHEMA,
        FeatureOutputKind.FEATURE_PLAN,
        FeatureOutputKind.FEATURE_VALUE_PLACEHOLDER,
        FeatureOutputKind.FACTOR_METADATA,
        FeatureOutputKind.LINEAGE_METADATA,
        FeatureOutputKind.VALIDATION_REPORT
    ]

def blocked_feature_output_kinds() -> list[FeatureBlockedOutputKind]:
    return [
        FeatureBlockedOutputKind.TRADE_SIGNAL,
        FeatureBlockedOutputKind.ORDER_DECISION,
        FeatureBlockedOutputKind.BROKER_INSTRUCTION,
        FeatureBlockedOutputKind.PAPER_STATE_MUTATION,
        FeatureBlockedOutputKind.LIVE_ORDER,
        FeatureBlockedOutputKind.DEMO_ORDER,
        FeatureBlockedOutputKind.TELEGRAM_REAL_SEND,
        FeatureBlockedOutputKind.DASHBOARD_PAYLOAD,
        FeatureBlockedOutputKind.SCRAPED_HTML,
        FeatureBlockedOutputKind.PAID_API_PAYLOAD
    ]

def validate_feature_output_contract(result: FeatureComputationResult | FeatureOutputSchema) -> list[str]:
    errors = []
    if isinstance(result, FeatureComputationResult):
        if result.produced_trade_signal:
            errors.append("Output must not produce trade signal")
        if result.produced_order_decision:
            errors.append("Output must not produce order decision")
    elif isinstance(result, FeatureOutputSchema):
        if not result.trade_signal_blocked:
            errors.append("Schema must block trade signals")
        if not result.order_decision_blocked:
            errors.append("Schema must block order decisions")
    return errors

def feature_output_contract_blocks_trade_signal() -> bool:
    return True

def feature_output_contract_blocks_order_decision() -> bool:
    return True

def feature_output_contract_summary() -> dict[str, Any]:
    return {"allowed": len(allowed_feature_output_kinds()), "blocked": len(blocked_feature_output_kinds())}

def feature_output_contract_to_text() -> str:
    return "Feature Output Contract Enforced: True"
