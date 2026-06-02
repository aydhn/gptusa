from typing import Any
import pandas as pd

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    FeatureAttributionProxy,
    ExplainabilityMethodKind,
    ExplanationScope,
    create_feature_attribution_proxy_id,
    current_time
)

def calculate_feature_proxy_score(series: pd.Series) -> float | None:
    if series.empty:
        return None
    try:
        # Simple proxy: mean absolute value as a dummy importance
        return float(series.abs().mean())
    except:
        return None

def calculate_feature_stability_proxy(series: pd.Series) -> float | None:
    if series.empty:
        return None
    try:
        # Simple proxy: 1 / (1 + std/mean)
        mean = series.abs().mean()
        if mean == 0:
            return 1.0
        cv = series.std() / mean
        return float(1.0 / (1.0 + cv))
    except:
        return None

def rank_feature_attributions(items: list[FeatureAttributionProxy]) -> list[FeatureAttributionProxy]:
    valid_items = [i for i in items if i.proxy_score is not None]
    invalid_items = [i for i in items if i.proxy_score is None]

    valid_items.sort(key=lambda x: x.proxy_score, reverse=True)

    for rank, item in enumerate(valid_items, 1):
        item.rank = rank

    for item in invalid_items:
        item.rank = None

    return valid_items + invalid_items

def build_feature_attribution_proxies(
    feature_df: pd.DataFrame,
    drift_metrics: list[dict[str, Any]] | None = None,
    max_features: int = 50
) -> list[FeatureAttributionProxy]:

    proxies = []

    # Exclude non-feature columns
    skip_cols = ['date', 'time', 'timestamp', 'index', 'id']
    feature_cols = [c for c in feature_df.columns if c.lower() not in skip_cols]

    for col in feature_cols:
        series = feature_df[col]
        if not pd.api.types.is_numeric_dtype(series):
            continue

        proxy_score = calculate_feature_proxy_score(series)
        stability = calculate_feature_stability_proxy(series)

        proxies.append(FeatureAttributionProxy(
            attribution_id=create_feature_attribution_proxy_id(),
            created_at_utc=current_time(),
            method_kind=ExplainabilityMethodKind.FEATURE_SUMMARY_PROXY,
            scope=ExplanationScope.FEATURE_LEVEL,
            feature_name=col,
            proxy_score=proxy_score,
            rank=None, # Assigned later
            direction_label="positive" if proxy_score and proxy_score > 0 else "neutral",
            stability_score=stability,
            drift_sensitivity_score=0.5, # Dummy
            attribution_notes=["Computed via simple statistical proxy without SHAP/LIME"],
            not_trade_signal=True,
            not_portfolio_weight=True,
            not_order_decision=True,
            research_data_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    ranked = rank_feature_attributions(proxies)
    return ranked[:max_features]

def validate_feature_attribution_proxies(items: list[FeatureAttributionProxy]) -> list[str]:
    errors = []
    for item in items:
        if not item.not_trade_signal:
            errors.append(f"Attribution {item.feature_name} is marked as trade signal")
        if not item.not_portfolio_weight:
            errors.append(f"Attribution {item.feature_name} is marked as portfolio weight")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Attribution {item.feature_name} produces execution artifacts")
    return errors

def feature_attribution_proxy_summary(items: list[FeatureAttributionProxy]) -> dict[str, Any]:
    return {
        "count": len(items),
        "top_features": [i.feature_name for i in items[:5] if i.rank is not None]
    }

def feature_attribution_proxy_to_text(items: list[FeatureAttributionProxy], limit: int = 300) -> str:
    summary = feature_attribution_proxy_summary(items)
    return f"Built {summary['count']} feature attributions. Top features: {', '.join(summary['top_features'])}"
