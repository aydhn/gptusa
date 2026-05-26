import datetime
from typing import Any
from usa_signal_bot.core.enums import FactorCategory, FeatureComputationMode, FeatureFoundationRiskFlag
from usa_signal_bot.feature_engine.phase116_models import FactorDefinition, create_factor_definition_id, FeatureDefinition, validate_factor_definition

def build_default_factor_definitions(features: list[FeatureDefinition] | None = None) -> list[FactorDefinition]:
    default_factors = [
        ("momentum_factor_metadata", FactorCategory.MOMENTUM),
        ("trend_factor_metadata", FactorCategory.TREND),
        ("volatility_factor_metadata", FactorCategory.LOW_VOLATILITY),
        ("liquidity_factor_metadata", FactorCategory.LIQUIDITY),
        ("quality_context_factor_metadata", FactorCategory.DATA_QUALITY_CONTEXT),
        ("event_risk_context_factor_metadata", FactorCategory.EVENT_RISK_CONTEXT),
        ("mean_reversion_context_factor_metadata", FactorCategory.REVERSAL),
        ("data_confidence_factor_metadata", FactorCategory.DATA_QUALITY_CONTEXT)
    ]
    out = []
    for name, cat in default_factors:
        item = FactorDefinition(
            factor_id=create_factor_definition_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            name=name,
            category=cat,
            description=f"Placeholder factor for {name}",
            input_features=[],
            output_column=name,
            factor_direction="NEUTRAL",
            computation_mode=FeatureComputationMode.PLANNED,
            research_metadata_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            enabled_for_phase116=True,
            implementation_phase=117,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        out.append(item)
    return out

def factor_definition_by_name(name: str, factors: list[FactorDefinition] | None = None) -> FactorDefinition | None:
    if factors is None:
        factors = build_default_factor_definitions()
    for factor in factors:
        if factor.name == name:
            return factor
    return None

def validate_factor_registry(factors: list[FactorDefinition]) -> list[str]:
    errors = []
    for factor in factors:
        validate_factor_definition(factor)
        if factor.errors:
            errors.extend([f"Factor {factor.name} error: {e}" for e in factor.errors])
    return errors

def factor_registry_summary(factors: list[FactorDefinition]) -> dict[str, Any]:
    return {"total": len(factors)}

def factor_registry_to_text(factors: list[FactorDefinition], limit: int = 200) -> str:
    lines = [f"Total Factors: {len(factors)}"]
    for i, factor in enumerate(factors):
        if i >= limit:
            lines.append("... [truncated]")
            break
        lines.append(f" - {factor.name} [{factor.category.value}]")
    return "\n".join(lines)
