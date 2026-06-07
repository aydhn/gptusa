from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestClosureContext, BacktestClosureFullReview, BacktestClosureReportType
)

def build_backtest_closure_context() -> BacktestClosureContext:
    # A simplified mock builder
    from usa_signal_bot.backtesting.closure.backtest_closure_orchestrator import build_safe_phase152_gate

    ctx = BacktestClosureContext()
    ctx.phase153_readiness_gate = build_safe_phase152_gate()
    ctx.phase153_readiness_gate_passed = ctx.phase153_readiness_gate.ready_for_phase153
    ctx.ready_for_phase153 = ctx.phase153_readiness_gate_passed
    return ctx

def build_backtest_closure_full_review() -> BacktestClosureFullReview:
    rev = BacktestClosureFullReview()
    rev.report_type = BacktestClosureReportType.FULL_PHASE152_REVIEW
    rev.context = build_backtest_closure_context()
    rev.phase153_readiness_gate = rev.context.phase153_readiness_gate
    return rev

def backtest_closure_full_review_summary(review: BacktestClosureFullReview) -> dict[str, Any]:
    return {"id": review.review_id, "ready_for_phase153": review.context.ready_for_phase153}

def backtest_closure_limitations_text() -> str:
    return "Phase 152 is a read-only final audit and closure phase. It does not perform active trading, deployment, portfolio construction, or optimization. The generated handoff package is for research purposes only."

def backtest_closure_full_review_to_text(review: BacktestClosureFullReview, limit: int = 300) -> str:
    return f"BacktestClosureFullReview: Ready for Phase 153 = {review.context.ready_for_phase153}"
