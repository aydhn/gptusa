from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    FoldReplayResult,
    FoldBenchmarkComparison,
    create_fold_benchmark_comparison_id,
    _now_utc
)

def build_fold_benchmark_comparisons(fold_results: List[FoldReplayResult]) -> List[FoldBenchmarkComparison]:
    comparisons = []

    for res in fold_results:
        # Mock calculation
        strat_ret = res.oos_metric_values.get("OOS_TOTAL_RETURN", 0.0)
        bench_ret = 0.02 # mock benchmark return

        comp = FoldBenchmarkComparison(
            comparison_id=create_fold_benchmark_comparison_id(),
            created_at_utc=_now_utc(),
            fold_id=res.fold_id,
            fold_index=res.fold_index,
            benchmark_label="Mock Benchmark",
            strategy_oos_return=strat_ret,
            benchmark_oos_return=bench_ret,
            excess_oos_return=strat_ret - bench_ret if strat_ret is not None else None,
            tracking_difference_mean=0.01,
            relative_drawdown=0.005,
            comparison_valid=True,
            not_strategy_activation=True,
            not_investment_advice=True,
            research_data_only=True
        )

        errors = validate_fold_benchmark_comparisons([comp])
        if errors:
            comp.comparison_valid = False
            comp.errors = errors
            comp.risk_flags.append(WalkForwardRiskFlag.FOLD_METRIC_INVALID)

        comparisons.append(comp)
    return comparisons

def validate_fold_benchmark_comparisons(items: List[FoldBenchmarkComparison]) -> List[str]:
    errors = []
    for c in items:
        if not c.not_investment_advice:
            errors.append(f"Comparison {c.comparison_id} must be not_investment_advice")
        if not c.not_strategy_activation:
            errors.append(f"Comparison {c.comparison_id} must be not_strategy_activation")
    return errors

def fold_benchmark_comparisons_summary(items: List[FoldBenchmarkComparison]) -> Dict[str, Any]:
    valid_count = sum(1 for c in items if c.comparison_valid)
    return {
        "total_comparisons": len(items),
        "valid_comparisons": valid_count,
        "all_valid": valid_count == len(items) and len(items) > 0
    }

def fold_benchmark_comparisons_to_text(items: List[FoldBenchmarkComparison], limit: int = 300) -> str:
    summary = fold_benchmark_comparisons_summary(items)
    return f"Fold Benchmark Comparisons: {summary['valid_comparisons']}/{summary['total_comparisons']} valid"
