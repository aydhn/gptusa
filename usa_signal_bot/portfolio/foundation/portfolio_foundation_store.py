import json
from pathlib import Path
from typing import Any

from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioFoundationContext, PortfolioFoundationFullReview,
    PortfolioInputReference, CandidateUniverseContract, PortfolioEligibilityRule,
    PortfolioConstraintCatalog, RiskBudgetContract, PositionSizingBoundaryContract,
    PortfolioConstructionBoundary, CandidateUniverseDiagnostics, ConstraintValidationReport,
    RiskBudgetValidationReport, SizingBoundaryValidationReport, PortfolioFoundationSafetyBoundaryResult,
    Phase154ReadinessGate
)

def portfolio_foundation_store_dir(data_root: Path) -> Path: return data_root / "portfolio" / "foundation"
def portfolio_foundation_contexts_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "contexts"
def portfolio_foundation_reviews_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "reviews"
def portfolio_inputs_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "inputs"
def candidate_universe_contracts_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "candidate_universe_contracts"
def eligibility_rules_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "eligibility_rules"
def constraint_catalogs_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "constraint_catalogs"
def risk_budget_contracts_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "risk_budget_contracts"
def sizing_boundaries_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "sizing_boundaries"
def construction_boundaries_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "construction_boundaries"
def diagnostics_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "diagnostics"
def validation_reports_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "validation_reports"
def safety_boundaries_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "safety_boundaries"
def phase154_gates_dir(data_root: Path) -> Path: return portfolio_foundation_store_dir(data_root) / "phase154_gates"

def _ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_portfolio_foundation_context_json(path: Path, item: PortfolioFoundationContext) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_portfolio_foundation_full_review_json(path: Path, item: PortfolioFoundationFullReview) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_portfolio_input_refs_jsonl(path: Path, items: list[PortfolioInputReference]) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(_to_dict(item)) + "\n")
    return path

def write_candidate_universe_contract_json(path: Path, item: CandidateUniverseContract) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_eligibility_rules_jsonl(path: Path, items: list[PortfolioEligibilityRule]) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(_to_dict(item)) + "\n")
    return path

def write_constraint_catalog_json(path: Path, item: PortfolioConstraintCatalog) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_risk_budget_contract_json(path: Path, item: RiskBudgetContract) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_position_sizing_boundary_json(path: Path, item: PositionSizingBoundaryContract) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_portfolio_construction_boundary_json(path: Path, item: PortfolioConstructionBoundary) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_candidate_universe_diagnostics_json(path: Path, item: CandidateUniverseDiagnostics) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_constraint_validation_report_json(path: Path, item: ConstraintValidationReport) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_risk_budget_validation_report_json(path: Path, item: RiskBudgetValidationReport) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_sizing_boundary_validation_report_json(path: Path, item: SizingBoundaryValidationReport) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_portfolio_foundation_safety_boundary_json(path: Path, item: PortfolioFoundationSafetyBoundaryResult) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def write_phase154_readiness_gate_json(path: Path, item: Phase154ReadinessGate) -> Path:
    _ensure_dir(path.parent)
    from usa_signal_bot.portfolio.foundation.phase153_models import _to_dict
    with open(path, "w") as f:
        json.dump(_to_dict(item), f, indent=2)
    return path

def read_portfolio_foundation_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_portfolio_foundation_reviews(data_root: Path) -> list[Path]:
    d = portfolio_foundation_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted([f for f in d.iterdir() if f.suffix == ".json"], key=lambda x: x.stat().st_mtime, reverse=True)

def get_latest_portfolio_foundation_review(data_root: Path) -> Path | None:
    lst = list_portfolio_foundation_reviews(data_root)
    return lst[0] if lst else None

def portfolio_foundation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_portfolio_foundation_reviews(data_root))
    }
