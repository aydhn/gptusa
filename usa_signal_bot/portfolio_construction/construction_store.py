import json
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
            f.write(json.dumps(sector_cluster_record_to_dict(item)) + "\n")
    return path

def write_exposure_snapshot_json(path: Path, item: ExposureSnapshot) -> Path:
    with open(path, "w") as f:
        json.dump(exposure_snapshot_to_dict(item), f, indent=2)
    return path

def write_concentration_assessments_jsonl(path: Path, items: list[ConcentrationAssessment]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(concentration_assessment_to_dict(item)) + "\n")
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
