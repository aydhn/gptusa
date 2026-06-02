from typing import Any
import pandas as pd

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    FactorContributionSummary,
    FeatureAttributionProxy,
    ExplainabilityMethodKind,
    create_factor_contribution_summary_id,
    current_time
)

def infer_factor_group(factor_name: str) -> str | None:
    name_lower = factor_name.lower()
    if any(x in name_lower for x in ["mom", "momentum", "roc"]):
        return "momentum"
    if any(x in name_lower for x in ["vol", "atr", "std"]):
        return "volatility"
    if any(x in name_lower for x in ["trend", "sma", "ema", "macd"]):
        return "trend"
    if any(x in name_lower for x in ["val", "pe", "pb"]):
        return "value"
    return "other"

def calculate_factor_contribution_proxy(series: pd.Series) -> float | None:
    if series.empty:
        return None
    try:
        return float(series.abs().mean())
    except:
        return None

def build_factor_contribution_summaries(
    factor_df: pd.DataFrame,
    feature_attributions: list[FeatureAttributionProxy] | None = None,
    max_factors: int = 30
) -> list[FactorContributionSummary]:

    summaries = []

    skip_cols = ['date', 'time', 'timestamp', 'index', 'id']
    factor_cols = [c for c in factor_df.columns if c.lower() not in skip_cols]

    for col in factor_cols:
        series = factor_df[col]
        if not pd.api.types.is_numeric_dtype(series):
            continue

        score = calculate_factor_contribution_proxy(series)

        summaries.append(FactorContributionSummary(
            summary_id=create_factor_contribution_summary_id(),
            created_at_utc=current_time(),
            method_kind=ExplainabilityMethodKind.FACTOR_SUMMARY_PROXY,
            factor_name=col,
            contribution_score=score,
            contribution_rank=None, # Sorted below
            contributing_features=[], # Would map from feature_attributions in real logic
            factor_group=infer_factor_group(col),
            stability_notes=["Computed without live inference"],
            drift_notes=["Metadata diagnostic only"],
            summary_valid=True,
            not_trade_signal=True,
            not_portfolio_weight=True,
            not_allocation=True,
            research_data_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    valid_items = [i for i in summaries if i.contribution_score is not None]
    invalid_items = [i for i in summaries if i.contribution_score is None]

    valid_items.sort(key=lambda x: x.contribution_score, reverse=True)

    for rank, item in enumerate(valid_items, 1):
        item.contribution_rank = rank

    ranked = valid_items + invalid_items
    return ranked[:max_factors]

def validate_factor_contribution_summaries(items: list[FactorContributionSummary]) -> list[str]:
    errors = []
    for item in items:
        if not item.not_trade_signal:
            errors.append(f"Factor {item.factor_name} is marked as trade signal")
        if not item.not_portfolio_weight or not item.not_allocation:
            errors.append(f"Factor {item.factor_name} is marked as portfolio weight/allocation")
        if item.produces_trade_signal or item.produces_order_decision or item.produces_portfolio_weights:
            errors.append(f"Factor {item.factor_name} produces execution artifacts")
    return errors

def factor_contribution_summary_summary(items: list[FactorContributionSummary]) -> dict[str, Any]:
    return {
        "count": len(items),
        "top_factors": [i.factor_name for i in items[:3] if i.contribution_rank is not None]
    }

def factor_contribution_summary_to_text(items: list[FactorContributionSummary], limit: int = 300) -> str:
    summary = factor_contribution_summary_summary(items)
    return f"Built {summary['count']} factor contributions. Top factors: {', '.join(summary['top_factors'])}"
