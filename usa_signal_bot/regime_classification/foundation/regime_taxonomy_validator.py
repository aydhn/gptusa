from typing import Any, List
from usa_signal_bot.regime_classification.foundation.phase126_models import RegimeLabelTaxonomy, RegimeLabelDefinition
from usa_signal_bot.regime_classification.foundation.regime_label_taxonomy import validate_regime_label_definition, compute_regime_taxonomy_hash

def validate_regime_label_names(labels: List[RegimeLabelDefinition]) -> List[str]:
    errors = []
    seen = set()
    for lbl in labels:
        if lbl.label_name in seen:
            errors.append(f"Duplicate label found: {lbl.label_name}")
        seen.add(lbl.label_name)

    required = ["unknown_regime", "mixed_regime"]
    for req in required:
        if req not in seen:
            errors.append(f"Missing required label: {req}")

    return errors

def validate_regime_label_safety(labels: List[RegimeLabelDefinition]) -> List[str]:
    errors = []
    for lbl in labels:
        errors.extend(validate_regime_label_definition(lbl))
        # Simple heuristic check for unsafe names
        unsafe_words = ["buy", "sell", "order", "entry", "exit", "portfolio_weight"]
        for word in unsafe_words:
            if word in lbl.label_name.lower():
                errors.append(f"Unsafe language in label name: {lbl.label_name}")
    return errors

def validate_regime_taxonomy_hash(taxonomy: RegimeLabelTaxonomy) -> List[str]:
    errors = []
    expected_hash = compute_regime_taxonomy_hash(taxonomy)
    if taxonomy.taxonomy_hash != expected_hash:
        errors.append(f"Taxonomy hash mismatch. Expected {expected_hash}, got {taxonomy.taxonomy_hash}")
    return errors

def validate_regime_taxonomy(taxonomy: RegimeLabelTaxonomy) -> List[str]:
    errors = []
    errors.extend(validate_regime_label_names(taxonomy.labels))
    errors.extend(validate_regime_label_safety(taxonomy.labels))

    if taxonomy.activation_allowed or taxonomy.strategy_activation_allowed:
        errors.append("Taxonomy allows activation")
    if taxonomy.produces_trade_signal or taxonomy.produces_order_decision or taxonomy.produces_portfolio_weights:
        errors.append("Taxonomy produces execution outputs")
    if taxonomy.investment_advice:
        errors.append("Taxonomy provides investment advice")

    return errors

def regime_taxonomy_validator_summary(errors: List[str]) -> dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def regime_taxonomy_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Taxonomy Validation: PASSED"

    lines = ["Taxonomy Validation: FAILED", "Errors:"]
    for err in errors:
        lines.append(f"  - {err}")
    return "\n".join(lines)
