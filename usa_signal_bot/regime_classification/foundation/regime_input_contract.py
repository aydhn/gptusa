from typing import Any, Dict, List
from usa_signal_bot.regime_classification.foundation.phase126_models import RegimeResearchInputBundle

def build_regime_input_contract(bundle: RegimeResearchInputBundle) -> dict[str, Any]:
    return {
        "bundle_id": bundle.bundle_id,
        "factor_table_refs": bundle.factor_table_refs,
        "factor_diagnostics_refs": bundle.factor_diagnostics_refs,
        "schema_contract_refs": bundle.schema_contract_refs,
        "lineage_contract_refs": bundle.lineage_contract_refs,
        "safety_contract_refs": bundle.safety_contract_refs,
        "research_report_refs": bundle.research_report_refs,
        "allowed_use": "regime_research_only",
        "disallowed_use": [
            "trade_signal",
            "order_decision",
            "strategy_activation",
            "portfolio_weight",
            "broker_execution",
            "paper_mutation",
            "investment_advice"
        ]
    }

def validate_regime_input_contract(contract: dict[str, Any]) -> List[str]:
    errors = []

    if contract.get("allowed_use") != "regime_research_only":
        errors.append("allowed_use must be 'regime_research_only'")

    disallowed = contract.get("disallowed_use", [])
    required_disallowed = [
        "trade_signal",
        "order_decision",
        "strategy_activation",
        "portfolio_weight",
        "broker_execution",
        "paper_mutation",
        "investment_advice"
    ]
    for d in required_disallowed:
        if d not in disallowed:
            errors.append(f"Missing required disallowed_use: {d}")

    return errors

def regime_input_contract_summary(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "bundle_id": contract.get("bundle_id"),
        "factor_tables": len(contract.get("factor_table_refs", [])),
        "allowed_use": contract.get("allowed_use")
    }

def regime_input_contract_to_text(contract: dict[str, Any]) -> str:
    lines = [
        f"Regime Input Contract for Bundle: {contract.get('bundle_id')}",
        f"Allowed Use: {contract.get('allowed_use')}",
        "Disallowed Use:"
    ]
    for d in contract.get("disallowed_use", []):
        lines.append(f"  - {d}")

    return "\n".join(lines)
