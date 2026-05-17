from typing import Any, List
from .workflow_models import RepairQueueItem, ResearchHypothesis, ExperimentPlan
from .priority_scoring import score_repair_item_priority, score_hypothesis_priority, score_experiment_priority

def rank_repair_items(items: List[RepairQueueItem]) -> List[RepairQueueItem]:
    return sorted(items, key=lambda x: score_repair_item_priority(x), reverse=True)

def rank_hypotheses(hypotheses: List[ResearchHypothesis]) -> List[ResearchHypothesis]:
    return sorted(hypotheses, key=lambda x: score_hypothesis_priority(x), reverse=True)

def rank_experiment_plans(plans: List[ExperimentPlan]) -> List[ExperimentPlan]:
    return sorted(plans, key=lambda x: score_experiment_priority(x), reverse=True)

def top_repair_items(items: List[RepairQueueItem], top_n: int = 10) -> List[RepairQueueItem]:
    return rank_repair_items(items)[:top_n]

def queue_ranking_summary(items: List[RepairQueueItem]) -> dict[str, Any]:
    ranked = rank_repair_items(items)
    return {
        "top_item_id": ranked[0].item_id if ranked else None,
        "top_score": score_repair_item_priority(ranked[0]) if ranked else 0.0
    }

def queue_ranking_to_text(payload: dict[str, Any]) -> str:
    return f"Top Item: {payload['top_item_id']} with score {payload['top_score']:.2f}"
