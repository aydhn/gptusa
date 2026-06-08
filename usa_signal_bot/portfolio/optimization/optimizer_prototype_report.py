from typing import Any, Dict
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerPrototypeContext, OptimizerPrototypeFullReview, OptimizerPrototypeReportType, OptimizerPrototypeStatus

def build_optimizer_prototype_context() -> OptimizerPrototypeContext:
    c = OptimizerPrototypeContext(status=OptimizerPrototypeStatus.DRAFT)
    c.ready_for_phase157 = False
    return c

def build_optimizer_prototype_full_review() -> OptimizerPrototypeFullReview:
    return OptimizerPrototypeFullReview(report_type=OptimizerPrototypeReportType.FULL_PHASE156_REVIEW)

def optimizer_prototype_full_review_summary(review: OptimizerPrototypeFullReview) -> Dict[str, Any]:
    return {"valid": len(review.errors) == 0}

def optimizer_prototype_limitations_text() -> str:
    return "Phase 156 limits: No actual portfolio optimization, no actual target weights, no capital deployment, no live/paper/broker trading. Outputs are sandbox weights for research only."

def optimizer_prototype_full_review_to_text(review: OptimizerPrototypeFullReview, limit: int = 300) -> str:
    return str(review.to_dict())[:limit]
