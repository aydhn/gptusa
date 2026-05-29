from typing import Any
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelingSpec,
    RegimeLabelingRule,
    create_regime_labeling_spec_id,
    create_regime_labeling_rule_id,
    _now_utc
)
from usa_signal_bot.core.enums import RegimeLabelingMethod

def build_default_regime_labeling_specs(taxonomy_labels: list[str] | None = None) -> list[RegimeLabelingSpec]:
    labels = taxonomy_labels or ["bull_regime", "bear_regime", "ranging_regime", "high_volatility", "low_volatility"]

    spec1 = RegimeLabelingSpec(
        spec_id=create_regime_labeling_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="top_candidate_labeling",
        method=RegimeLabelingMethod.DETERMINISTIC_TOP_CANDIDATE,
        taxonomy_labels=labels,
        candidate_score_columns=[], # will be resolved dynamically
        minimum_score_threshold=40.0,
        minimum_score_gap=5.0,
        fallback_label="unknown_regime",
        mixed_label="mixed_regime",
        unknown_label="unknown_regime",
        conflict_policy="fallback_to_mixed_or_unknown",
        deterministic=True,
        research_metadata_only=True,
        model_training_used=False,
        model_prediction_used=False,
        activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

    spec2 = RegimeLabelingSpec(
        spec_id=create_regime_labeling_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="threshold_priority_labeling",
        method=RegimeLabelingMethod.DETERMINISTIC_THRESHOLD_RULES,
        taxonomy_labels=labels,
        candidate_score_columns=[],
        minimum_score_threshold=50.0,
        minimum_score_gap=10.0,
        fallback_label="unknown_regime",
        mixed_label="mixed_regime",
        unknown_label="unknown_regime",
        conflict_policy="strict_priority",
        deterministic=True,
        research_metadata_only=True,
        model_training_used=False,
        model_prediction_used=False,
        activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

    return [spec1, spec2]

def build_default_regime_labeling_rules(taxonomy_labels: list[str] | None = None) -> list[RegimeLabelingRule]:
    # Placeholder for deterministic rules
    return []

def regime_labeling_spec_by_name(name: str, specs: list[RegimeLabelingSpec] | None = None) -> RegimeLabelingSpec | None:
    if not specs:
        specs = build_default_regime_labeling_specs()
    for s in specs:
        if s.spec_name == name:
            return s
    return None

def validate_regime_labeling_specs(specs: list[RegimeLabelingSpec]) -> list[str]:
    errors = []
    for s in specs:
        if s.model_training_used:
            errors.append(f"Spec {s.spec_name} uses model training")
        if s.model_prediction_used:
            errors.append(f"Spec {s.spec_name} uses model prediction")
        if s.produces_trade_signal or s.produces_order_decision or s.produces_portfolio_weights:
            errors.append(f"Spec {s.spec_name} produces execution outputs")
    return errors

def validate_regime_labeling_rules(rules: list[RegimeLabelingRule]) -> list[str]:
    errors = []
    for r in rules:
        if r.produces_trade_signal or r.produces_order_decision or r.produces_portfolio_weights:
            errors.append(f"Rule {r.rule_name} produces execution outputs")
    return errors

def regime_labeling_specs_summary(specs: list[RegimeLabelingSpec]) -> dict[str, Any]:
    return {
        "spec_count": len(specs),
        "spec_names": [s.spec_name for s in specs]
    }

def regime_labeling_specs_to_text(specs: list[RegimeLabelingSpec], limit: int = 200) -> str:
    return f"Specs: {', '.join(s.spec_name for s in specs)}"
