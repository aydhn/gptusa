import hashlib
from typing import Any, Dict, List

from usa_signal_bot.core.enums import RegimeTaxonomyStatus, RegimeLabelKind, RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    RegimeLabelDefinition,
    RegimeLabelTaxonomy,
    create_regime_label_definition_id,
    create_regime_label_taxonomy_id,
    _now
)

def build_default_regime_label_definitions() -> List[RegimeLabelDefinition]:
    labels = [
        ("risk_on", RegimeLabelKind.RISK_ON),
        ("risk_off", RegimeLabelKind.RISK_OFF),
        ("high_volatility", RegimeLabelKind.HIGH_VOLATILITY),
        ("low_volatility", RegimeLabelKind.LOW_VOLATILITY),
        ("trending_up", RegimeLabelKind.TRENDING_UP),
        ("trending_down", RegimeLabelKind.TRENDING_DOWN),
        ("range_bound", RegimeLabelKind.RANGE_BOUND),
        ("liquidity_stress", RegimeLabelKind.LIQUIDITY_STRESS),
        ("normal_liquidity", RegimeLabelKind.NORMAL_LIQUIDITY),
        ("event_distorted", RegimeLabelKind.EVENT_DISTORTED),
        ("data_quality_degraded", RegimeLabelKind.DATA_QUALITY_DEGRADED),
        ("mixed_regime", RegimeLabelKind.MIXED_REGIME),
        ("unknown_regime", RegimeLabelKind.UNKNOWN_REGIME)
    ]

    return [
        RegimeLabelDefinition(
            label_id=create_regime_label_definition_id(),
            created_at_utc=_now(),
            label_name=name,
            label_kind=kind,
            description=f"Label for {name}",
            intended_use="research_metadata",
            allowed_inputs=["market_state_dataset"],
            disallowed_outputs=["trade_signal", "order_decision", "portfolio_weight"],
            mutually_exclusive_group=None,
            hierarchy_level=1,
            research_metadata_only=True,
            activation_allowed=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            investment_advice=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        for name, kind in labels
    ]

def compute_regime_taxonomy_hash(taxonomy: RegimeLabelTaxonomy) -> str:
    hash_str = f"{taxonomy.taxonomy_name}_{taxonomy.version}_" + "_".join(sorted([l.label_name for l in taxonomy.labels]))
    return hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

def regime_label_by_name(name: str, taxonomy: RegimeLabelTaxonomy) -> RegimeLabelDefinition | None:
    for label in taxonomy.labels:
        if label.label_name == name:
            return label
    return None

def validate_regime_label_definition(label: RegimeLabelDefinition) -> List[str]:
    errors = []
    if label.activation_allowed:
        errors.append(f"Label {label.label_name} allows activation")
    if label.produces_trade_signal or label.produces_order_decision or label.produces_portfolio_weights:
        errors.append(f"Label {label.label_name} produces execution outputs")
    if label.investment_advice:
        errors.append(f"Label {label.label_name} is marked as investment advice")
    return errors

def build_regime_label_taxonomy(version: str = "phase126.v1") -> RegimeLabelTaxonomy:
    labels = build_default_regime_label_definitions()

    from usa_signal_bot.regime_classification.foundation.regime_taxonomy_validator import validate_regime_taxonomy

    tax = RegimeLabelTaxonomy(
        taxonomy_id=create_regime_label_taxonomy_id(),
        created_at_utc=_now(),
        status=RegimeTaxonomyStatus.CREATED,
        taxonomy_name="regime_label_taxonomy",
        version=version,
        labels=labels,
        default_label="unknown_regime",
        unknown_label="unknown_regime",
        label_count=len(labels),
        taxonomy_hash=None,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    tax.taxonomy_hash = compute_regime_taxonomy_hash(tax)

    errors = validate_regime_taxonomy(tax)
    if errors:
        tax.status = RegimeTaxonomyStatus.BLOCKED
        tax.errors = errors
        tax.risk_flags.append(RegimeFoundationRiskFlag.REGIME_TAXONOMY_INVALID)

    return tax

def regime_label_taxonomy_summary(taxonomy: RegimeLabelTaxonomy) -> dict[str, Any]:
    return {
        "taxonomy_id": taxonomy.taxonomy_id,
        "taxonomy_name": taxonomy.taxonomy_name,
        "version": taxonomy.version,
        "label_count": taxonomy.label_count,
        "status": taxonomy.status.value
    }

def regime_label_taxonomy_to_text(taxonomy: RegimeLabelTaxonomy, limit: int = 300) -> str:
    lines = [
        f"Taxonomy ID: {taxonomy.taxonomy_id}",
        f"Name: {taxonomy.taxonomy_name} (v{taxonomy.version})",
        f"Status: {taxonomy.status.value}",
        f"Labels ({taxonomy.label_count}):"
    ]
    for lbl in taxonomy.labels[:limit]:
        lines.append(f"  - {lbl.label_name}")

    if taxonomy.errors:
        lines.append("Errors:")
        for err in taxonomy.errors:
            lines.append(f"  - {err}")

    return "\n".join(lines)
