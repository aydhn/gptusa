from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    MetricNormalizationRule,
    MetricNormalizationResult,
    create_metric_normalization_rule_id,
    create_metric_normalization_result_id
)

def build_default_metric_normalization_rules() -> list[MetricNormalizationRule]:
    default_rules = [
        ("classification_accuracy", "HIGHER_IS_BETTER_DIRECT", True),
        ("classification_balanced_accuracy", "HIGHER_IS_BETTER_DIRECT", True),
        ("classification_f1_macro", "HIGHER_IS_BETTER_DIRECT", True),
        ("regression_mae", "LOWER_IS_BETTER_INVERTED", False),
        ("regression_rmse", "LOWER_IS_BETTER_INVERTED", False),
        ("regression_r2", "HIGHER_IS_BETTER_DIRECT", True),
        ("rank_correlation", "HIGHER_IS_BETTER_DIRECT", True),
        ("calibration_brier_score", "LOWER_IS_BETTER_INVERTED", False),
        ("stability_metric", "HIGHER_IS_BETTER_DIRECT", True),
        ("coverage_metric", "HIGHER_IS_BETTER_DIRECT", True),
    ]

    rules = []
    for name, norm_kind, hib in default_rules:
        rules.append(
            MetricNormalizationRule(
                rule_id=create_metric_normalization_rule_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                metric_name=name,
                metric_kind="standard",
                normalization_kind=norm_kind,
                higher_is_better=hib,
                min_value=None,
                max_value=None,
                weight=1.0,
                required=False,
                non_trading_metric=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
        )
    return rules

def normalize_metric_value(raw_value: Any, rule: MetricNormalizationRule, peer_values: list[Any] | None = None) -> float | None:
    if not isinstance(raw_value, (int, float)):
        return None

    if rule.normalization_kind == "HIGHER_IS_BETTER_DIRECT":
        return float(raw_value)
    elif rule.normalization_kind == "LOWER_IS_BETTER_INVERTED":
        return -float(raw_value)
    return float(raw_value)

def build_metric_normalization_results(rows: list[dict[str, Any]], rules: list[MetricNormalizationRule] | None = None) -> list[MetricNormalizationResult]:
    if rules is None:
        rules = build_default_metric_normalization_rules()

    rules_dict = {r.metric_name: r for r in rules}
    results = []
    for row in rows:
        name = row.get("metric_name", "")
        raw = row.get("metric_value")
        rule = rules_dict.get(name)
        if rule:
            norm_val = normalize_metric_value(raw, rule)
            results.append(
                MetricNormalizationResult(
                    result_id=create_metric_normalization_result_id(),
                    created_at_utc=datetime.now(timezone.utc).isoformat(),
                    metric_name=name,
                    metric_kind=rule.metric_kind,
                    experiment_id=row.get("experiment_id"),
                    model_artifact_id=row.get("model_artifact_id"),
                    raw_value=raw,
                    normalized_value=norm_val,
                    normalization_kind=rule.normalization_kind,
                    weight=rule.weight,
                    included_in_ranking=True,
                    non_trading_metric=True,
                    warnings=[],
                    errors=[],
                    risk_flags=[],
                    metadata={}
                )
            )
    return results

def validate_metric_normalization_results(items: list[MetricNormalizationResult]) -> list[str]:
    return []

def metric_normalization_summary(items: list[MetricNormalizationResult]) -> dict[str, Any]:
    return {"count": len(items)}

def metric_normalization_to_text(items: list[MetricNormalizationResult], limit: int = 300) -> str:
    return str([res.metric_name for res in items])[:limit]
