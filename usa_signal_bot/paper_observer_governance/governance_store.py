from typing import Any
from pathlib import Path
from .observer_governance_models import ObserverPaperComparisonReport, PromotionEvidenceRefresh, ObserverGovernanceGate, ObserverGovernanceDecisionResult, ObserverGovernanceAuditEntry, ObserverGovernanceReview

def observer_governance_store_dir(data_root: Path) -> Path: return data_root / "paper_observer_governance"
def observer_comparison_reports_dir(data_root: Path) -> Path: return observer_governance_store_dir(data_root) / "comparisons"
def evidence_refreshes_dir(data_root: Path) -> Path: return observer_governance_store_dir(data_root) / "evidence_refreshes"
def observer_governance_gates_dir(data_root: Path) -> Path: return observer_governance_store_dir(data_root) / "gates"
def observer_governance_decisions_dir(data_root: Path) -> Path: return observer_governance_store_dir(data_root) / "decisions"
def observer_governance_audit_dir(data_root: Path) -> Path: return observer_governance_store_dir(data_root) / "audit"
def observer_governance_reviews_dir(data_root: Path) -> Path: return observer_governance_store_dir(data_root) / "reviews"

def write_observer_paper_comparison_report_json(path: Path, item: ObserverPaperComparisonReport) -> Path: return path
def write_promotion_evidence_refresh_json(path: Path, item: PromotionEvidenceRefresh) -> Path: return path
def write_observer_governance_gates_jsonl(path: Path, items: list[ObserverGovernanceGate]) -> Path: return path
def write_observer_governance_decision_json(path: Path, item: ObserverGovernanceDecisionResult) -> Path: return path
def write_observer_governance_audit_jsonl(path: Path, items: list[ObserverGovernanceAuditEntry]) -> Path: return path
def write_observer_governance_review_json(path: Path, item: ObserverGovernanceReview) -> Path: return path
def read_observer_governance_review_json(path: Path) -> dict[str, Any]: return {}
def list_observer_governance_reviews(data_root: Path) -> list[Path]: return []
def get_latest_observer_governance_review(data_root: Path) -> Path | None: return None
def observer_governance_store_summary(data_root: Path) -> dict[str, Any]: return {}
