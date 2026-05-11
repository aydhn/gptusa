from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from usa_signal_bot.taskqueue.task_models import TaskQueuePlan, TaskQueueRunResult, WorkloadBudgetEvaluation, TaskConflict, task_queue_plan_to_dict, task_queue_run_result_to_dict, workload_budget_evaluation_to_dict, task_conflict_to_dict

def taskqueue_store_dir(data_root: Path) -> Path:
    d = data_root / "taskqueue"
    d.mkdir(parents=True, exist_ok=True)
    return d

def queue_plans_dir(data_root: Path) -> Path:
    d = taskqueue_store_dir(data_root) / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def queue_runs_dir(data_root: Path) -> Path:
    d = taskqueue_store_dir(data_root) / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def workload_reports_dir(data_root: Path) -> Path:
    d = taskqueue_store_dir(data_root) / "workload"
    d.mkdir(parents=True, exist_ok=True)
    return d

def workload_audit_dir(data_root: Path) -> Path:
    d = taskqueue_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_task_queue_plan_json(path: Path, plan: TaskQueuePlan) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(task_queue_plan_to_dict(plan), f, indent=2)
    return path

def write_task_queue_run_result_json(path: Path, result: TaskQueueRunResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(task_queue_run_result_to_dict(result), f, indent=2)
    return path

def write_workload_budget_evaluation_json(path: Path, evaluation: WorkloadBudgetEvaluation) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(workload_budget_evaluation_to_dict(evaluation), f, indent=2)
    return path

def write_task_batch_json(path: Path, batch: Any) -> Path:
    from usa_signal_bot.taskqueue.batch_builder import task_batch_to_dict
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(task_batch_to_dict(batch), f, indent=2)
    return path

def write_task_conflicts_jsonl(path: Path, conflicts: List[TaskConflict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for c in conflicts: f.write(json.dumps(task_conflict_to_dict(c)) + "\n")
    return path

def read_task_queue_plan_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def read_task_queue_run_result_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def list_task_queue_plans(data_root: Path) -> List[Path]:
    return sorted(queue_plans_dir(data_root).glob("*.json"), reverse=True)

def list_task_queue_runs(data_root: Path) -> List[Path]:
    return sorted(queue_runs_dir(data_root).glob("*.json"), reverse=True)

def get_latest_task_queue_plan(data_root: Path) -> Optional[Path]:
    plans = list_task_queue_plans(data_root)
    return plans[0] if plans else None

def get_latest_task_queue_run(data_root: Path) -> Optional[Path]:
    runs = list_task_queue_runs(data_root)
    return runs[0] if runs else None

def taskqueue_store_summary(data_root: Path) -> Dict[str, Any]:
    plans, runs = list_task_queue_plans(data_root), list_task_queue_runs(data_root)
    return {"plans_count": len(plans), "runs_count": len(runs), "latest_plan": str(plans[0].name) if plans else None, "latest_run": str(runs[0].name) if runs else None}
