from typing import Any
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview
from usa_signal_bot.core.enums import RegimeAlignmentStatus

def attach_regime_map_to_backtest_result(result: dict[str, Any], review: RegimeMapReview | None = None) -> dict[str, Any]:
    if not review:
        return result

    out = dict(result)
    if "metadata" not in out:
         out["metadata"] = {}

    out["metadata"]["regime_map_review_id"] = review.review_id
    if review.cross_sectional_map:
         out["metadata"]["cross_sectional_regime"] = review.cross_sectional_map.cross_sectional_regime.value
         out["metadata"]["breadth_regime"] = review.cross_sectional_map.breadth_regime.value

    conflicted = sum(1 for a in review.alignments if a.status in [RegimeAlignmentStatus.CONFLICTED, RegimeAlignmentStatus.DIVERGENT])
    out["metadata"]["conflicted_trade_count"] = conflicted # Proxy for backtest

    out["metadata"]["regime_warning_count"] = len(review.warnings)

    return out

def backtest_regime_map_summary(result: dict[str, Any]) -> dict[str, Any]:
    meta = result.get("metadata", {})
    return {
        "cross_sectional_regime": meta.get("cross_sectional_regime", "UNKNOWN"),
        "breadth_regime": meta.get("breadth_regime", "UNKNOWN"),
        "conflicted_trade_count": meta.get("conflicted_trade_count", 0)
    }

def backtest_regime_transition_warnings(result: dict[str, Any]) -> list[str]:
    # Placeholder to extract warnings from metadata if injected
    meta = result.get("metadata", {})
    return meta.get("transition_warnings", [])

def backtest_regime_conditioned_metrics_placeholder(result: dict[str, Any]) -> dict[str, Any]:
    return {}
