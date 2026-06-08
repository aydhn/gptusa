import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionContext,
    PortfolioConstructionFullReview,
    PortfolioConstructionInputReference,
    PortfolioSandboxCandidate,
    PortfolioConstructionPolicy,
    SandboxAllocationMethodContract,
    ConstraintAwareScore,
    SandboxAllocationResult,
    PrototypeExposureTable,
    PortfolioSandboxDiagnosticRecord,
    AllocationSandboxComparisonReport,
    PortfolioConstructionValidationReport,
    AllocationSandboxSafetyBoundaryResult,
    Phase156ReadinessGate
)
import pandas as pd

def portfolio_construction_store_dir(data_root: Path) -> Path:
    d = data_root / "portfolio" / "construction"
    d.mkdir(parents=True, exist_ok=True)
    return d

def portfolio_construction_contexts_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def portfolio_construction_reviews_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def construction_inputs_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "inputs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_candidates_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "sandbox_candidates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def construction_policies_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "policies"
    d.mkdir(parents=True, exist_ok=True)
    return d

def method_contracts_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "method_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def constraint_scores_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "constraint_scores"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_allocations_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "sandbox_allocations"
    d.mkdir(parents=True, exist_ok=True)
    return d

def exposure_tables_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "exposure_tables"
    d.mkdir(parents=True, exist_ok=True)
    return d

def diagnostics_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "diagnostics"
    d.mkdir(parents=True, exist_ok=True)
    return d

def comparison_reports_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "comparison_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def validation_reports_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "validation_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def safety_boundaries_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "safety_boundaries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def phase156_gates_dir(data_root: Path) -> Path:
    d = portfolio_construction_store_dir(data_root) / "phase156_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, data: Any) -> Path:
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return path

def _write_jsonl(path: Path, items: List[Any]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, default=str) + "\n")
    return path

# Type hinting requires full implementations, using simple dict dumps for MVP

def write_portfolio_construction_context_json(path: Path, item: PortfolioConstructionContext) -> Path:
    return _write_json(path, item.__dict__)

def write_portfolio_construction_full_review_json(path: Path, item: PortfolioConstructionFullReview) -> Path:
    return _write_json(path, item.__dict__)

def write_construction_input_refs_jsonl(path: Path, items: List[PortfolioConstructionInputReference]) -> Path:
    return _write_jsonl(path, [i.__dict__ for i in items])

def write_sandbox_candidates_jsonl(path: Path, items: List[PortfolioSandboxCandidate]) -> Path:
    return _write_jsonl(path, [i.__dict__ for i in items])

def write_portfolio_construction_policy_json(path: Path, item: PortfolioConstructionPolicy) -> Path:
    return _write_json(path, item.__dict__)

def write_sandbox_allocation_method_contracts_jsonl(path: Path, items: List[SandboxAllocationMethodContract]) -> Path:
    return _write_jsonl(path, [i.__dict__ for i in items])

def write_constraint_aware_scores_jsonl(path: Path, items: List[ConstraintAwareScore]) -> Path:
    return _write_jsonl(path, [i.__dict__ for i in items])

def write_sandbox_allocation_results_jsonl(path: Path, items: List[SandboxAllocationResult]) -> Path:
    return _write_jsonl(path, [i.__dict__ for i in items])

def write_prototype_exposure_table_json(path: Path, item: PrototypeExposureTable) -> Path:
    return _write_json(path, item.__dict__)

def write_prototype_exposure_table_csv(path: Path, item: PrototypeExposureTable) -> Path:
    from usa_signal_bot.portfolio.construction.prototype_exposure_table import prototype_exposure_table_to_dataframe
    df = prototype_exposure_table_to_dataframe(item)
    df.to_csv(path, index=False)
    return path

def write_portfolio_sandbox_diagnostics_jsonl(path: Path, items: List[PortfolioSandboxDiagnosticRecord]) -> Path:
    return _write_jsonl(path, [i.__dict__ for i in items])

def write_allocation_sandbox_comparison_report_json(path: Path, item: AllocationSandboxComparisonReport) -> Path:
    return _write_json(path, item.__dict__)

def write_portfolio_construction_validation_report_json(path: Path, item: PortfolioConstructionValidationReport) -> Path:
    return _write_json(path, item.__dict__)

def write_allocation_sandbox_safety_boundary_json(path: Path, item: AllocationSandboxSafetyBoundaryResult) -> Path:
    return _write_json(path, item.__dict__)

def write_phase156_readiness_gate_json(path: Path, item: Phase156ReadinessGate) -> Path:
    return _write_json(path, item.__dict__)

def read_portfolio_construction_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_portfolio_construction_reviews(data_root: Path) -> List[Path]:
    d = portfolio_construction_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_portfolio_construction_review(data_root: Path) -> Optional[Path]:
    files = list_portfolio_construction_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

def portfolio_construction_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_portfolio_construction_reviews(data_root))
    }
