from typing import Any, Dict, List

from usa_signal_bot.core.enums import WalkForwardReportType, WalkForwardStatus, WalkForwardDecision
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardContext,
    WalkForwardFullReview,
    create_walk_forward_context_id,
    create_walk_forward_full_review_id,
    _now_utc
)

def build_walk_forward_context() -> WalkForwardContext:
    # This is a factory method to initialize an empty context
    from usa_signal_bot.backtesting.walk_forward.benchmark_comparison_ingestion import ingest_benchmark_comparison_review_payload
    from usa_signal_bot.backtesting.walk_forward.walk_forward_window_policy import build_default_walk_forward_window_policy
    from usa_signal_bot.backtesting.walk_forward.robustness_summary import build_robustness_summary
    from usa_signal_bot.backtesting.walk_forward.oos_robustness_metrics import OOSRobustnessMetrics, create_oos_robustness_metrics_id
    from usa_signal_bot.backtesting.walk_forward.walk_forward_validation_report import build_walk_forward_validation_report
    from usa_signal_bot.backtesting.walk_forward.temporal_stability_audit import build_temporal_stability_audit
    from usa_signal_bot.backtesting.walk_forward.walk_forward_safety_boundary import build_walk_forward_safety_boundary_result
    from usa_signal_bot.backtesting.walk_forward.phase151_readiness_gate import build_phase151_readiness_gate

    empty_ingest = ingest_benchmark_comparison_review_payload({})
    empty_policy = build_default_walk_forward_window_policy()

    empty_oos = OOSRobustnessMetrics(
        metrics_id=create_oos_robustness_metrics_id(),
        created_at_utc=_now_utc(),
        fold_count=0,
        passed_fold_count=0,
        failed_fold_count=0,
        oos_return_mean=0.0,
        oos_return_median=0.0,
        oos_return_min=0.0,
        oos_return_max=0.0,
        oos_return_std=0.0,
        oos_max_drawdown_mean=0.0,
        oos_excess_return_mean=0.0,
        oos_cost_drag_mean=0.0,
        fold_pass_rate=0.0,
        robustness_score=0.0,
        metrics_valid=False
    )
    empty_summary = build_robustness_summary(empty_oos, [], [])
    empty_report = build_walk_forward_validation_report([], [], [], [], empty_summary)
    empty_audit = build_temporal_stability_audit(empty_summary)
    empty_boundary = build_walk_forward_safety_boundary_result([])
    empty_gate = build_phase151_readiness_gate(empty_report, empty_audit, empty_boundary)

    return WalkForwardContext(
        context_id=create_walk_forward_context_id(),
        created_at_utc=_now_utc(),
        status=WalkForwardStatus.CREATED,
        decision=WalkForwardDecision.LOAD_BENCHMARK_COMPARISON_ARTIFACTS,
        source_benchmark_comparison_review_id=None,
        ingestion=empty_ingest,
        input_references=[],
        window_policy=empty_policy,
        folds=[],
        validation_report=empty_report,
        temporal_stability_audit=empty_audit,
        safety_boundary=empty_boundary,
        phase151_readiness_gate=empty_gate
    )

def build_walk_forward_full_review() -> WalkForwardFullReview:
    ctx = build_walk_forward_context()
    return WalkForwardFullReview(
        review_id=create_walk_forward_full_review_id(),
        created_at_utc=_now_utc(),
        report_type=WalkForwardReportType.FULL_PHASE150_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        validation_report=ctx.validation_report,
        temporal_stability_audit=ctx.temporal_stability_audit,
        safety_boundary=ctx.safety_boundary,
        phase151_readiness_gate=ctx.phase151_readiness_gate
    )

def walk_forward_full_review_summary(review: WalkForwardFullReview) -> Dict[str, Any]:
    return {
        "valid": review.phase151_readiness_gate.ready_for_phase151,
        "score": review.validation_report.robustness_summary.oos_metrics.robustness_score,
        "folds": len(review.context.folds)
    }

def walk_forward_limitations_text() -> str:
    return (
        "LIMITATIONS OF PHASE 150:\n"
        "- This phase performs walk-forward validation offline.\n"
        "- No live trading or real orders are generated.\n"
        "- No broker integration or paper state mutation occurs.\n"
        "- Outputs are NOT investment advice.\n"
        "- Phase 151 will handle stress testing and Monte Carlo robustness."
    )

def walk_forward_full_review_to_text(review: WalkForwardFullReview, limit: int = 300) -> str:
    summary = walk_forward_full_review_summary(review)
    lines = [
        f"Walk Forward Full Review:",
        f"  Valid: {summary['valid']}",
        f"  Score: {summary['score']}",
        f"  {walk_forward_limitations_text()}"
    ]
    return "\n".join(lines)[:limit]
