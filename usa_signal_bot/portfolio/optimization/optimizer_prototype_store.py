import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerPrototypeContext, OptimizerPrototypeFullReview, OptimizerInputReference, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerObjectiveContract, OptimizerConstraintContract, OptimizerSandboxResult, OptimizerObjectiveScore, ObjectiveComparisonReport, OptimizerDiagnosticRecord, OptimizerValidationReport, OptimizerSafetyBoundaryResult, Phase157ReadinessGate

def optimizer_prototype_store_dir(data_root: Path) -> Path: return data_root / "portfolio" / "optimization"
def optimizer_prototype_contexts_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "contexts"
def optimizer_prototype_reviews_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "reviews"
def optimizer_inputs_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "inputs"
def optimizer_candidates_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "candidates"
def optimizer_policies_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "policies"
def objective_contracts_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "objective_contracts"
def constraint_contracts_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "constraint_contracts"
def optimizer_results_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "results"
def objective_scores_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "objective_scores"
def objective_comparison_reports_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "objective_comparison_reports"
def optimizer_diagnostics_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "diagnostics"
def optimizer_validation_reports_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "validation_reports"
def optimizer_safety_boundaries_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "safety_boundaries"
def phase157_gates_dir(data_root: Path) -> Path: return optimizer_prototype_store_dir(data_root) / "phase157_gates"

def write_optimizer_prototype_context_json(path: Path, item: OptimizerPrototypeContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def write_optimizer_prototype_full_review_json(path: Path, item: OptimizerPrototypeFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def write_optimizer_input_refs_jsonl(path: Path, items: List[OptimizerInputReference]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_optimizer_candidates_jsonl(path: Path, items: List[OptimizerSandboxCandidate]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_optimizer_policy_json(path: Path, item: OptimizerPolicy) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def write_objective_contracts_jsonl(path: Path, items: List[OptimizerObjectiveContract]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_constraint_contracts_jsonl(path: Path, items: List[OptimizerConstraintContract]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_optimizer_results_jsonl(path: Path, items: List[OptimizerSandboxResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_objective_scores_jsonl(path: Path, items: List[OptimizerObjectiveScore]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_objective_comparison_report_json(path: Path, item: ObjectiveComparisonReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def write_optimizer_diagnostics_jsonl(path: Path, items: List[OptimizerDiagnosticRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for i in items: f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_optimizer_validation_report_json(path: Path, item: OptimizerValidationReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def write_optimizer_safety_boundary_json(path: Path, item: OptimizerSafetyBoundaryResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def write_phase157_readiness_gate_json(path: Path, item: Phase157ReadinessGate) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f: json.dump(item.to_dict(), f)
    return path

def read_optimizer_prototype_full_review_json(path: Path) -> Dict[str, Any]:
    with path.open() as f: return json.load(f)

def list_optimizer_prototype_reviews(data_root: Path) -> List[Path]:
    d = optimizer_prototype_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_optimizer_prototype_review(data_root: Path) -> Optional[Path]:
    revs = list_optimizer_prototype_reviews(data_root)
    if not revs: return None
    return max(revs, key=lambda p: p.stat().st_mtime)

def optimizer_prototype_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews_count": len(list_optimizer_prototype_reviews(data_root))}
