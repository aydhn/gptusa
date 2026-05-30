from typing import Any, Dict, List, Optional
from pathlib import Path
import json

from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeResearchFreezeContext,
    RegimeResearchFreezeFullReview,
    MonitoringValidationResult,
    DriftReportDocument,
    DriftReportQaRuleResult,
    ResearchFreezePackage,
    ResearchFreezeReadinessGate
)

def research_freeze_store_dir(data_root: Path) -> Path:
    d = data_root / "regime_classification" / "freeze_preparation"
    d.mkdir(parents=True, exist_ok=True)
    return d

def research_freeze_contexts_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "contexts"
    d.mkdir(exist_ok=True)
    return d

def research_freeze_reviews_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "reviews"
    d.mkdir(exist_ok=True)
    return d

def monitoring_validation_results_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "monitoring_validation"
    d.mkdir(exist_ok=True)
    return d

def drift_reports_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "drift_reports"
    d.mkdir(exist_ok=True)
    return d

def drift_report_qa_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "drift_report_qa"
    d.mkdir(exist_ok=True)
    return d

def freeze_packages_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "freeze_packages"
    d.mkdir(exist_ok=True)
    return d

def freeze_readiness_gates_dir(data_root: Path) -> Path:
    d = research_freeze_store_dir(data_root) / "gates"
    d.mkdir(exist_ok=True)
    return d

# Dummies for saving JSON:
def write_regime_research_freeze_context_json(path: Path, item: RegimeResearchFreezeContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path

def write_regime_research_freeze_full_review_json(path: Path, item: RegimeResearchFreezeFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path

def write_monitoring_validation_result_json(path: Path, item: MonitoringValidationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path

def write_drift_report_document_json(path: Path, item: DriftReportDocument) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path

def write_drift_report_markdown(path: Path, item: DriftReportDocument, overwrite: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(item.rendered_markdown or "", encoding="utf-8")
    return path

def write_drift_report_text(path: Path, item: DriftReportDocument, overwrite: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(item.rendered_text or "", encoding="utf-8")
    return path

def write_drift_report_qa_results_jsonl(path: Path, items: List[DriftReportQaRuleResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    return path

def write_research_freeze_package_json(path: Path, item: ResearchFreezePackage) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path

def write_research_freeze_readiness_gate_json(path: Path, item: ResearchFreezeReadinessGate) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
    return path

def read_regime_research_freeze_full_review_json(path: Path) -> Dict[str, Any]:
    return {}

def list_regime_research_freeze_reviews(data_root: Path) -> List[Path]:
    return []

def get_latest_regime_research_freeze_review(data_root: Path) -> Optional[Path]:
    return None

def research_freeze_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": 0}
