from typing import Any
from .observer_governance_models import ObserverMetricComparison, ObserverPaperComparisonReport, PromotionEvidenceItem, PromotionEvidenceRefresh, ObserverGovernanceGate, ObserverGovernanceDecisionResult, ObserverGovernanceAuditEntry, ObserverGovernanceReview

def observer_metric_comparison_to_text(item: ObserverMetricComparison) -> str: return ""
def observer_paper_comparison_report_to_text(item: ObserverPaperComparisonReport, limit: int = 100) -> str: return ""
def promotion_evidence_item_to_text(item: PromotionEvidenceItem) -> str: return ""
def promotion_evidence_refresh_to_text(item: PromotionEvidenceRefresh, limit: int = 100) -> str: return ""
def observer_governance_gate_to_text(item: ObserverGovernanceGate) -> str: return ""
def observer_governance_decision_result_to_text(item: ObserverGovernanceDecisionResult) -> str: return ""
def observer_governance_audit_entry_to_text(item: ObserverGovernanceAuditEntry) -> str: return ""
def observer_governance_review_to_text(item: ObserverGovernanceReview, limit: int = 100) -> str: return ""
def observer_governance_store_summary_to_text(summary: dict[str, Any]) -> str: return ""
def observer_governance_limitations_text() -> str: return ""
