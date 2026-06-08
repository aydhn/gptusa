import json
import dataclasses
from pathlib import Path
from typing import Any
import pandas as pd
from usa_signal_bot.portfolio.sizing.phase154_models import (
    SizingPrototypeContext, SizingPrototypeFullReview, SizingInputReference,
    SizingCandidate, SizingPolicy, SizingMethodContract, SizingPrototypeResult,
    SizingCapFloorRule, SizingComparisonMatrix, SizingDiagnosticRecord,
    SizingSensitivityReport, RiskBudgetAdherenceReport, SizingSafetyBoundaryResult,
    Phase155ReadinessGate
)
from usa_signal_bot.portfolio.sizing.sizing_comparison_matrix import sizing_comparison_matrix_to_dataframe

def sizing_prototype_store_dir(data_root: Path) -> Path:
    d = data_root / "portfolio" / "sizing"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_prototype_contexts_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_prototype_reviews_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_inputs_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "inputs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_candidates_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "candidates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_policies_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "policies"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_method_contracts_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "method_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_results_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_cap_floor_rules_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "cap_floor_rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_comparison_matrices_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "comparison_matrices"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_diagnostics_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "diagnostics"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_sensitivity_reports_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "sensitivity_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def risk_budget_adherence_reports_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "risk_budget_adherence"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sizing_safety_boundaries_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "safety_boundaries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def phase155_gates_dir(data_root: Path) -> Path:
    d = sizing_prototype_store_dir(data_root) / "phase155_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _to_dict(obj):
    if dataclasses.is_dataclass(obj):
        d = dataclasses.asdict(obj)
        for k, v in d.items():
            if hasattr(v, "value"):
                d[k] = v.value
        return d
    return obj

def write_sizing_prototype_context_json(path: Path, item: SizingPrototypeContext) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_sizing_prototype_full_review_json(path: Path, item: SizingPrototypeFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_sizing_input_refs_jsonl(path: Path, items: list[SizingInputReference]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict(i), default=str) + "\n")
    return path

def write_sizing_candidates_jsonl(path: Path, items: list[SizingCandidate]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict(i), default=str) + "\n")
    return path

def write_sizing_policy_json(path: Path, item: SizingPolicy) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_sizing_method_contracts_jsonl(path: Path, items: list[SizingMethodContract]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict(i), default=str) + "\n")
    return path

def write_sizing_results_jsonl(path: Path, items: list[SizingPrototypeResult]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict(i), default=str) + "\n")
    return path

def write_sizing_cap_floor_rules_jsonl(path: Path, items: list[SizingCapFloorRule]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict(i), default=str) + "\n")
    return path

def write_sizing_comparison_matrix_json(path: Path, item: SizingComparisonMatrix) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_sizing_comparison_matrix_csv(path: Path, item: SizingComparisonMatrix) -> Path:
    df = sizing_comparison_matrix_to_dataframe(item)
    df.to_csv(path, index=False)
    return path

def write_sizing_diagnostics_jsonl(path: Path, items: list[SizingDiagnosticRecord]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict(i), default=str) + "\n")
    return path

def write_sizing_sensitivity_report_json(path: Path, item: SizingSensitivityReport) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_risk_budget_adherence_report_json(path: Path, item: RiskBudgetAdherenceReport) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_sizing_safety_boundary_json(path: Path, item: SizingSafetyBoundaryResult) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def write_phase155_readiness_gate_json(path: Path, item: Phase155ReadinessGate) -> Path:
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2, default=str)
    return path

def read_sizing_prototype_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_sizing_prototype_reviews(data_root: Path) -> list[Path]:
    d = sizing_prototype_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_sizing_prototype_review(data_root: Path) -> Path | None:
    files = list_sizing_prototype_reviews(data_root)
    if not files:
        return None
    return sorted(files, key=lambda p: p.stat().st_mtime)[-1]

def sizing_prototype_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews_count": len(list_sizing_prototype_reviews(data_root))}
