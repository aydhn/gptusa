import json
from pathlib import Path
from typing import Any, List, Optional
from .workflow_models import (
    RepairQueueItem, ResearchHypothesis, ExperimentPlan,
    ParameterChangeProposal, AcceptanceGate, ResearchDecisionLogEntry,
    ResearchWorkflowReview, repair_queue_item_to_dict, research_hypothesis_to_dict,
    experiment_plan_to_dict, parameter_change_proposal_to_dict,
    acceptance_gate_to_dict, research_decision_log_entry_to_dict,
    research_workflow_review_to_dict
)
from ..core.exceptions import ResearchWorkflowStorageError

def workflow_store_dir(data_root: Path) -> Path:
    d = data_root / "research_workflow"
    d.mkdir(parents=True, exist_ok=True)
    return d

def repair_items_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "repair_items"
    d.mkdir(exist_ok=True)
    return d

def hypotheses_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "hypotheses"
    d.mkdir(exist_ok=True)
    return d

def experiment_plans_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "experiment_plans"
    d.mkdir(exist_ok=True)
    return d

def parameter_proposals_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "parameter_proposals"
    d.mkdir(exist_ok=True)
    return d

def acceptance_gates_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "acceptance_gates"
    d.mkdir(exist_ok=True)
    return d

def decision_logs_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "decision_logs"
    d.mkdir(exist_ok=True)
    return d

def workflow_reviews_dir(data_root: Path) -> Path:
    d = workflow_store_dir(data_root) / "reviews"
    d.mkdir(exist_ok=True)
    return d

def _write_jsonl(path: Path, items: List[Any], to_dict_func) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(to_dict_func(item)) + "\n")
        return path
    except Exception as e:
        raise ResearchWorkflowStorageError(f"Failed to write to {path}: {e}")

def write_repair_items_jsonl(path: Path, items: List[RepairQueueItem]) -> Path:
    return _write_jsonl(path, items, repair_queue_item_to_dict)

def write_hypotheses_jsonl(path: Path, items: List[ResearchHypothesis]) -> Path:
    return _write_jsonl(path, items, research_hypothesis_to_dict)

def write_experiment_plans_jsonl(path: Path, items: List[ExperimentPlan]) -> Path:
    return _write_jsonl(path, items, experiment_plan_to_dict)

def write_parameter_proposals_jsonl(path: Path, items: List[ParameterChangeProposal]) -> Path:
    return _write_jsonl(path, items, parameter_change_proposal_to_dict)

def write_acceptance_gates_jsonl(path: Path, items: List[AcceptanceGate]) -> Path:
    return _write_jsonl(path, items, acceptance_gate_to_dict)

def write_decision_log_jsonl(path: Path, items: List[ResearchDecisionLogEntry]) -> Path:
    return _write_jsonl(path, items, research_decision_log_entry_to_dict)

def write_research_workflow_review_json(path: Path, item: ResearchWorkflowReview) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(research_workflow_review_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise ResearchWorkflowStorageError(f"Failed to write review to {path}: {e}")

def read_research_workflow_review_json(path: Path) -> dict[str, Any]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise ResearchWorkflowStorageError(f"Failed to read review from {path}: {e}")

def list_research_workflow_reviews(data_root: Path) -> List[Path]:
    d = workflow_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_research_workflow_review(data_root: Path) -> Optional[Path]:
    reviews = list_research_workflow_reviews(data_root)
    return reviews[-1] if reviews else None

def workflow_store_summary(data_root: Path) -> dict[str, Any]:
    reviews = list_research_workflow_reviews(data_root)
    return {
        "review_count": len(reviews),
        "latest_review": str(reviews[-1].name) if reviews else None
    }
