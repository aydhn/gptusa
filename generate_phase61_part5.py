import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- portfolio_construction/conflict_resolver.py ---
conflict_code = """from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan, PortfolioAllocationStatus, PortfolioGuardDecision
from usa_signal_bot.core.enums import PortfolioConflictType

def detect_symbol_overlap_conflicts(plan: PortfolioConstructionPlan) -> list[dict[str, any]]:
    conflicts = []
    symbol_sides = {}
    for a in plan.allocations:
        if a.symbol not in symbol_sides:
            symbol_sides[a.symbol] = set()
        symbol_sides[a.symbol].add(a.side)

    for sym, sides in symbol_sides.items():
        if len(sides) > 1:
            conflicts.append({
                "type": PortfolioConflictType.SIDE_CONFLICT.value if hasattr(PortfolioConflictType.SIDE_CONFLICT, 'value') else str(PortfolioConflictType.SIDE_CONFLICT),
                "symbol": sym,
                "message": f"Symbol {sym} has conflicting allocations: {sides}"
            })
    return conflicts

def detect_portfolio_conflicts(plan: PortfolioConstructionPlan) -> list[dict[str, any]]:
    conflicts = []
    conflicts.extend(detect_symbol_overlap_conflicts(plan))
    # Sector/cluster conflicts can be inferred from concentration assessments
    for c in plan.concentration_assessments:
        if c.decision in [PortfolioGuardDecision.CAP, PortfolioGuardDecision.BLOCK]:
            conflicts.append({
                "type": f"{c.exposure_type.value if hasattr(c.exposure_type, 'value') else str(c.exposure_type)}_OVEREXPOSURE",
                "symbol": None,
                "message": f"{c.name} exceeded limits: {c.exposure_pct_equity}% vs {c.limit_pct_equity}%"
            })
    return conflicts

def resolve_portfolio_conflicts(plan: PortfolioConstructionPlan) -> PortfolioConstructionPlan:
    conflicts = detect_portfolio_conflicts(plan)
    plan.conflicts.extend(conflicts)

    # simple side conflict resolution: keep highest weight
    for c in conflicts:
        if c.get("type") == "SIDE_CONFLICT":
            sym = c.get("symbol")
            sym_allocs = [a for a in plan.allocations if a.symbol == sym]
            if not sym_allocs: continue
            best = max(sym_allocs, key=lambda x: x.weight_pct_equity or 0.0)
            for a in sym_allocs:
                if a != best and a.status != PortfolioAllocationStatus.SUPPRESSED:
                    a.status = PortfolioAllocationStatus.SUPPRESSED
                    a.guard_decisions.append(PortfolioGuardDecision.SUPPRESS)
                    a.adjustment_reasons.append("Suppressed due to side conflict resolution")
                    a.final_notional_usd = 0.0
                    a.weight_pct_equity = 0.0
                    plan.suppressed_count += 1
    return plan

def portfolio_conflicts_to_text(conflicts: list[dict[str, any]]) -> str:
    if not conflicts: return "No portfolio conflicts detected."
    lines = ["Portfolio Conflicts"]
    for c in conflicts:
        lines.append(f"  [{c.get('type')}] {c.get('message')}")
    return "\\n".join(lines)
"""
write_file("usa_signal_bot/portfolio_construction/conflict_resolver.py", conflict_code)

# --- portfolio_construction/construction_store.py ---
store_code = """import json
import os
from pathlib import Path
from typing import Any
from usa_signal_bot.portfolio_construction.portfolio_models import (
    SectorClusterRecord, ExposureSnapshot, ConcentrationAssessment,
    PortfolioConstructionPlan, PortfolioConstructionReview,
    sector_cluster_record_to_dict, exposure_snapshot_to_dict,
    concentration_assessment_to_dict, portfolio_construction_plan_to_dict,
    portfolio_construction_review_to_dict
)

def construction_store_dir(data_root: Path) -> Path:
    d = data_root / "portfolio_construction"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sector_cluster_records_dir(data_root: Path) -> Path:
    d = construction_store_dir(data_root) / "sector_cluster_records"
    d.mkdir(parents=True, exist_ok=True)
    return d

def exposure_snapshots_dir(data_root: Path) -> Path:
    d = construction_store_dir(data_root) / "exposure_snapshots"
    d.mkdir(parents=True, exist_ok=True)
    return d

def concentration_assessments_dir(data_root: Path) -> Path:
    d = construction_store_dir(data_root) / "concentration_assessments"
    d.mkdir(parents=True, exist_ok=True)
    return d

def portfolio_plans_dir(data_root: Path) -> Path:
    d = construction_store_dir(data_root) / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def construction_reviews_dir(data_root: Path) -> Path:
    d = construction_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_sector_cluster_records_jsonl(path: Path, items: list[SectorClusterRecord]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(sector_cluster_record_to_dict(item)) + "\\n")
    return path

def write_exposure_snapshot_json(path: Path, item: ExposureSnapshot) -> Path:
    with open(path, "w") as f:
        json.dump(exposure_snapshot_to_dict(item), f, indent=2)
    return path

def write_concentration_assessments_jsonl(path: Path, items: list[ConcentrationAssessment]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(concentration_assessment_to_dict(item)) + "\\n")
    return path

def write_portfolio_construction_plan_json(path: Path, item: PortfolioConstructionPlan) -> Path:
    with open(path, "w") as f:
        json.dump(portfolio_construction_plan_to_dict(item), f, indent=2)
    return path

def write_portfolio_construction_review_json(path: Path, item: PortfolioConstructionReview) -> Path:
    with open(path, "w") as f:
        json.dump(portfolio_construction_review_to_dict(item), f, indent=2)
    return path

def read_portfolio_construction_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_portfolio_construction_reviews(data_root: Path) -> list[Path]:
    d = construction_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_portfolio_construction_review(data_root: Path) -> Path | None:
    reviews = list_portfolio_construction_reviews(data_root)
    return reviews[-1] if reviews else None

def construction_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "sector_cluster_records": len(list(sector_cluster_records_dir(data_root).glob("*.*"))),
        "exposure_snapshots": len(list(exposure_snapshots_dir(data_root).glob("*.*"))),
        "concentration_assessments": len(list(concentration_assessments_dir(data_root).glob("*.*"))),
        "portfolio_plans": len(list(portfolio_plans_dir(data_root).glob("*.*"))),
        "construction_reviews": len(list_portfolio_construction_reviews(data_root)),
    }
"""
write_file("usa_signal_bot/portfolio_construction/construction_store.py", store_code)

print("Generated step 5")
