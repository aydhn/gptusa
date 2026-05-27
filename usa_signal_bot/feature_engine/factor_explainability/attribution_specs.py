import datetime
from typing import Any

from usa_signal_bot.core.enums import FeatureAttributionMethod
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FeatureAttributionSpec,
    create_feature_attribution_spec_id
)

def infer_input_features_for_factor(factor_name: str, available_columns: list[str]) -> list[str]:
    # Dummy deterministic logic to infer input columns
    inputs = []
    prefix = factor_name.split("_")[0]
    for col in available_columns:
        if col.startswith(prefix) and col != factor_name:
            inputs.append(col)
    if not inputs:
        # Fallback
        inputs = [c for c in available_columns if c != factor_name and c not in ("date", "symbol")]
    return inputs

def build_attribution_spec_for_factor(factor_name: str, factor_column: str, available_columns: list[str]) -> FeatureAttributionSpec:
    inputs = infer_input_features_for_factor(factor_name, available_columns)
    warnings = []
    if not inputs:
        warnings.append(f"No input features found for factor {factor_name}")

    return FeatureAttributionSpec(
        spec_id=create_feature_attribution_spec_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        factor_name=factor_name,
        factor_column=factor_column,
        input_feature_columns=inputs,
        attribution_method=FeatureAttributionMethod.DETERMINISTIC_HEURISTIC,
        normalize_attributions=True,
        quality_weighted=False,
        confidence_weighted=False,
        lineage_weighted=False,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=warnings,
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_default_feature_attribution_specs(factor_columns: list[str], available_columns: list[str]) -> list[FeatureAttributionSpec]:
    specs = []
    for f_col in factor_columns:
        # Assuming factor_name is derived from factor_column
        specs.append(build_attribution_spec_for_factor(f_col, f_col, available_columns))
    return specs

def validate_feature_attribution_specs(specs: list[FeatureAttributionSpec]) -> list[str]:
    errors = []
    for spec in specs:
        if spec.produces_trade_signal:
            errors.append(f"Spec {spec.spec_id} produces trade signal")
        if spec.produces_order_decision:
            errors.append(f"Spec {spec.spec_id} produces order decision")
        if spec.produces_portfolio_weights:
            errors.append(f"Spec {spec.spec_id} produces portfolio weights")
    return errors

def attribution_specs_summary(specs: list[FeatureAttributionSpec]) -> dict[str, Any]:
    return {"spec_count": len(specs)}

def attribution_specs_to_text(specs: list[FeatureAttributionSpec], limit: int = 200) -> str:
    return f"Generated {len(specs)} feature attribution specs."
