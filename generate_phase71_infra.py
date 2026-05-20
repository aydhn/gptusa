import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

write_file("usa_signal_bot/paper_shadow_governance/governance_store.py", """
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowSessionComparisonReport, ShadowAcceptanceScorecard, ShadowEvidencePack,
    ShadowDecisionBoardResult, ShadowGovernanceAuditEntry, ShadowGovernanceReview,
    shadow_session_comparison_report_to_dict, shadow_acceptance_scorecard_to_dict,
    shadow_evidence_pack_to_dict, shadow_decision_board_result_to_dict,
    shadow_governance_audit_entry_to_dict, shadow_governance_review_to_dict
)

def shadow_governance_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_shadow_governance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_comparison_reports_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "comparison_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_scorecards_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "scorecards"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_evidence_packs_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "evidence_packs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_decisions_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "decisions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_audit_logs_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "audit_logs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_governance_reviews_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_shadow_comparison_report_json(path: Path, item: ShadowSessionComparisonReport) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_session_comparison_report_to_dict(item), f, indent=2)
    return path

def write_shadow_acceptance_scorecard_json(path: Path, item: ShadowAcceptanceScorecard) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_acceptance_scorecard_to_dict(item), f, indent=2)
    return path

def write_shadow_evidence_pack_json(path: Path, item: ShadowEvidencePack) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_evidence_pack_to_dict(item), f, indent=2)
    return path

def write_shadow_decision_result_json(path: Path, item: ShadowDecisionBoardResult) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_decision_board_result_to_dict(item), f, indent=2)
    return path

def write_shadow_audit_entries_jsonl(path: Path, items: List[ShadowGovernanceAuditEntry]) -> Path:
    with open(path, 'a', encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(shadow_governance_audit_entry_to_dict(it)) + "\\n")
    return path

def write_shadow_governance_review_json(path: Path, item: ShadowGovernanceReview) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_governance_review_to_dict(item), f, indent=2)
    return path

def read_shadow_governance_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_shadow_governance_reviews(data_root: Path) -> List[Path]:
    d = shadow_governance_reviews_dir(data_root)
    return sorted(d.glob("*.json"), key=os.path.getmtime, reverse=True)

def get_latest_shadow_governance_review(data_root: Path) -> Optional[Path]:
    l = list_shadow_governance_reviews(data_root)
    return l[0] if l else None

def shadow_governance_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"total_reviews": len(list_shadow_governance_reviews(data_root))}
""")

write_file("usa_signal_bot/paper_shadow_governance/governance_validation.py", """
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowSessionComparisonReport, ShadowAcceptanceScorecard, ShadowDecisionBoardResult, ShadowGovernanceReview
)
from usa_signal_bot.core.exceptions import ShadowGovernanceValidationError

@dataclass
class ShadowGovernanceValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowGovernanceValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[ShadowGovernanceValidationIssue]
    warnings: List[str]
    errors: List[str]

def check_boolean_false(obj, attr_name) -> Optional[ShadowGovernanceValidationIssue]:
    val = getattr(obj, attr_name, False)
    if val:
        return ShadowGovernanceValidationIssue("error", attr_name, f"{attr_name} must be False.")
    return None

def validate_shadow_comparison_report_report(item: ShadowSessionComparisonReport) -> ShadowGovernanceValidationReport:
    return ShadowGovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_shadow_scorecard_report(item: ShadowAcceptanceScorecard) -> ShadowGovernanceValidationReport:
    iss = []
    for attr in ["allowed_for_real_orders", "allowed_for_paper_state_mutation", "allowed_for_telegram_real_send", "allowed_for_production_config_write"]:
        err = check_boolean_false(item, attr)
        if err: iss.append(err)
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_shadow_decision_report(item: ShadowDecisionBoardResult) -> ShadowGovernanceValidationReport:
    iss = []
    for attr in ["allowed_for_real_orders", "allowed_for_paper_state_mutation", "allowed_for_telegram_real_send", "allowed_for_production_config_write"]:
        err = check_boolean_false(item, attr)
        if err: iss.append(err)
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_shadow_governance_review_report(item: ShadowGovernanceReview) -> ShadowGovernanceValidationReport:
    return ShadowGovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_shadow_governance_payload(payload: Dict[str, Any]) -> ShadowGovernanceValidationReport:
    s = str(payload).lower()
    if "api_key" in s or "secret" in s or "token" in s:
        iss = [ShadowGovernanceValidationIssue("error", None, "Secret leak detected in governance payload.")]
        return ShadowGovernanceValidationReport(False, 1, 0, 1, 0, iss, [], ["Secret leak detected in governance payload."])
    return ShadowGovernanceValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_shadow_governance(text: str) -> ShadowGovernanceValidationReport:
    t = text.lower()
    bad = ["live approved", "sent to broker", "kesin al", "garanti"]
    iss = [ShadowGovernanceValidationIssue("error", None, f"Live language: {b}") for b in bad if b in t]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_no_real_order_language_in_shadow_governance(text: str) -> ShadowGovernanceValidationReport:
    t = text.lower()
    bad = ["paper'a uygula", "canlıya al", "gerçek emir", "kesin kâr", "candidate kesin iyi"]
    iss = [ShadowGovernanceValidationIssue("error", None, f"Real order language: {b}") for b in bad if b in t]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_no_paper_state_mutation_fields_in_shadow_governance(payload: Dict[str, Any]) -> ShadowGovernanceValidationReport:
    bad = ["paper_state_committed", "paper_order_executed", "portfolio_state_mutated"]
    iss = [ShadowGovernanceValidationIssue("error", b, f"{b} found in payload") for b in bad if b in payload]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def validate_no_broker_execution_fields_in_shadow_governance(payload: Dict[str, Any]) -> ShadowGovernanceValidationReport:
    bad = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    iss = [ShadowGovernanceValidationIssue("error", b, f"{b} found in payload") for b in bad if b in payload]
    return ShadowGovernanceValidationReport(len(iss)==0, len(iss), 0, len(iss), 0, iss, [], [i.message for i in iss])

def shadow_governance_validation_report_to_text(report: ShadowGovernanceValidationReport) -> str:
    return f"Valid: {report.valid}. Errors: {report.error_count}"

def assert_shadow_governance_valid(report: ShadowGovernanceValidationReport) -> None:
    if not report.valid:
        raise ShadowGovernanceValidationError(" | ".join(report.errors))
""")

write_file("usa_signal_bot/paper_shadow_governance/governance_reporting.py", """
from typing import Any, Dict
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowMetricComparison, ShadowAcceptanceGate, ShadowAcceptanceScorecard,
    ShadowSessionComparisonReport, ShadowEvidencePack, ShadowDecisionBoardResult,
    ShadowGovernanceAuditEntry, ShadowGovernanceReview
)

def shadow_metric_comparison_to_text(item: ShadowMetricComparison) -> str:
    return f"{item.metric_name}: {item.baseline_value} -> {item.candidate_value} ({item.direction.value})"

def shadow_acceptance_gate_to_text(item: ShadowAcceptanceGate) -> str:
    return f"Gate {item.gate_type.value}: {item.status.value}"

def shadow_acceptance_scorecard_to_text(item: ShadowAcceptanceScorecard) -> str:
    return f"Scorecard: {item.overall_status.value} (Score: {item.acceptance_score})"

def shadow_session_comparison_report_to_text(item: ShadowSessionComparisonReport, limit: int = 100) -> str:
    return f"Comparison Report: Outcome={item.outcome.value}"

def shadow_evidence_pack_to_text(item: ShadowEvidencePack) -> str:
    return f"Evidence Pack: Complete={item.evidence_complete}"

def shadow_decision_board_result_to_text(item: ShadowDecisionBoardResult) -> str:
    return f"Decision: {item.decision.value}"

def shadow_governance_audit_entry_to_text(item: ShadowGovernanceAuditEntry) -> str:
    return f"Audit: {item.action} on {item.entity_type}"

def shadow_governance_review_to_text(item: ShadowGovernanceReview, limit: int = 100) -> str:
    return f"Governance Review {item.review_id}: {len(item.decisions)} decisions."

def shadow_governance_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return str(summary)

def shadow_governance_limitations_text() -> str:
    return (
        "LIMITATIONS:\\n"
        "- Shadow governance is a local simulation governance only.\\n"
        "- Shadow PnL is not real portfolio performance.\\n"
        "- Acceptance scores are NOT investment advice.\\n"
        "- Decisions do NOT constitute paper/live/demo trading approval.\\n"
        "- No broker API calls, real orders, or paper mutations are executed."
    )
""")

print("Infra files generated successfully.")
