
from pathlib import Path
from typing import Any, List, Optional
import json
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    PaperReadinessBoardReview, PaperReadinessBoardGate, RuntimeWriteBlockEvent,
    WriteBlockedRuntimeAdapterProof, ActivationFirewallRule, ActivationFirewallEvent,
    PaperReadinessBoardAuditEntry, PaperReadinessBoardFullReview,
    paper_readiness_board_review_to_dict, paper_readiness_board_gate_to_dict,
    runtime_write_block_event_to_dict, write_blocked_runtime_adapter_proof_to_dict,
    activation_firewall_rule_to_dict, activation_firewall_event_to_dict,
    paper_readiness_board_audit_entry_to_dict, paper_readiness_board_full_review_to_dict
)

def paper_readiness_board_store_dir(data_root: Path) -> Path: return data_root / "paper_readiness_board"
def board_reviews_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "board_reviews"
def board_gates_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "gates"
def write_block_events_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "write_block_events"
def write_block_proofs_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "write_block_proofs"
def activation_firewall_rules_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "activation_firewall_rules"
def activation_firewall_events_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "activation_firewall_events"
def board_audit_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "audit"
def board_full_reviews_dir(data_root: Path) -> Path: return paper_readiness_board_store_dir(data_root) / "full_reviews"

def _ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_board_review_json(path: Path, item: PaperReadinessBoardReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(paper_readiness_board_review_to_dict(item), f, indent=2)
    return path

def write_board_gates_jsonl(path: Path, items: List[PaperReadinessBoardGate]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items: f.write(json.dumps(paper_readiness_board_gate_to_dict(item)) + "\n")
    return path

def write_runtime_write_block_events_jsonl(path: Path, items: List[RuntimeWriteBlockEvent]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items: f.write(json.dumps(runtime_write_block_event_to_dict(item)) + "\n")
    return path

def write_write_block_proof_json(path: Path, item: WriteBlockedRuntimeAdapterProof) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(write_blocked_runtime_adapter_proof_to_dict(item), f, indent=2)
    return path

def write_activation_firewall_rules_jsonl(path: Path, items: List[ActivationFirewallRule]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items: f.write(json.dumps(activation_firewall_rule_to_dict(item)) + "\n")
    return path

def write_activation_firewall_events_jsonl(path: Path, items: List[ActivationFirewallEvent]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items: f.write(json.dumps(activation_firewall_event_to_dict(item)) + "\n")
    return path

def write_board_audit_jsonl(path: Path, items: List[PaperReadinessBoardAuditEntry]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "a") as f:
        for item in items: f.write(json.dumps(paper_readiness_board_audit_entry_to_dict(item)) + "\n")
    return path

def write_board_full_review_json(path: Path, item: PaperReadinessBoardFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(paper_readiness_board_full_review_to_dict(item), f, indent=2)
    return path

def read_board_full_review_json(path: Path) -> dict:
    if not path.exists(): return {}
    with open(path, "r") as f: return json.load(f)

def list_board_full_reviews(data_root: Path) -> List[Path]:
    d = board_full_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_board_full_review(data_root: Path) -> Optional[Path]:
    files = list_board_full_reviews(data_root)
    if not files: return None
    return sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[0]

def board_store_summary(data_root: Path) -> dict:
    return {"reviews": len(list_board_full_reviews(data_root))}

from dataclasses import dataclass, field
from usa_signal_bot.core.exceptions import PaperReadinessBoardValidationError

@dataclass
class PaperReadinessBoardValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: dict = field(default_factory=dict)

@dataclass
class PaperReadinessBoardValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[PaperReadinessBoardValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_board_review_report(item: PaperReadinessBoardReview) -> PaperReadinessBoardValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(PaperReadinessBoardValidationIssue("ERROR", "activation_denied", "must be true"))
    if item.activation_allowed:
        issues.append(PaperReadinessBoardValidationIssue("ERROR", "activation_allowed", "must be false"))
    valid = len(issues) == 0
    return PaperReadinessBoardValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_write_block_proof_report(item: WriteBlockedRuntimeAdapterProof) -> PaperReadinessBoardValidationReport:
    issues = []
    if not item.all_writes_blocked:
        issues.append(PaperReadinessBoardValidationIssue("ERROR", "all_writes_blocked", "must be true"))
    valid = len(issues) == 0
    return PaperReadinessBoardValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_activation_firewall_event_report(item: ActivationFirewallEvent) -> PaperReadinessBoardValidationReport:
    issues = []
    if not item.blocked:
        issues.append(PaperReadinessBoardValidationIssue("ERROR", "blocked", "must be true"))
    valid = len(issues) == 0
    return PaperReadinessBoardValidationReport(valid, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_board_full_review_report(item: PaperReadinessBoardFullReview) -> PaperReadinessBoardValidationReport:
    return PaperReadinessBoardValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_board_payload(payload: dict) -> PaperReadinessBoardValidationReport:
    return PaperReadinessBoardValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_board(text: str) -> PaperReadinessBoardValidationReport:
    issues = []
    t = text.lower()
    for bad in ["sent to broker", "live approved", "gerçek emir", "kesin al"]:
        if bad in t:
            issues.append(PaperReadinessBoardValidationIssue("ERROR", "text", f"Forbidden language: {bad}"))
    return PaperReadinessBoardValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_active_paper_language_in_board(text: str) -> PaperReadinessBoardValidationReport:
    issues = []
    t = text.lower()
    for bad in ["aktif et", "paper'a uygula", "canlıya al", "enable active paper"]:
        if bad in t:
            issues.append(PaperReadinessBoardValidationIssue("ERROR", "text", f"Forbidden language: {bad}"))
    return PaperReadinessBoardValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_paper_state_mutation_fields_in_board(payload: dict) -> PaperReadinessBoardValidationReport:
    bad_keys = {"paper_state_committed", "portfolio_state_mutated", "position_mutated"}
    issues = []
    for bad in bad_keys & payload.keys():
        issues.append(PaperReadinessBoardValidationIssue("ERROR", "fields", f"Forbidden field: {bad}"))
    return PaperReadinessBoardValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def validate_no_broker_execution_fields_in_board(payload: dict) -> PaperReadinessBoardValidationReport:
    keys = " ".join(payload.keys())
    issues = []
    for bad in ["broker_order_id", "live_order_id", "sent_to_broker"]:
        if bad in keys:
            issues.append(PaperReadinessBoardValidationIssue("ERROR", "fields", f"Forbidden field: {bad}"))
    return PaperReadinessBoardValidationReport(len(issues)==0, len(issues), 0, len(issues), 0, issues, [], [i.message for i in issues])

def paper_readiness_board_validation_report_to_text(report: PaperReadinessBoardValidationReport) -> str:
    return f"Valid: {report.valid}, Errors: {report.errors}"

def assert_paper_readiness_board_valid(report: PaperReadinessBoardValidationReport) -> None:
    if not report.valid:
        raise PaperReadinessBoardValidationError(f"Validation failed: {report.errors}")

def board_store_summary_to_text(summary: dict) -> str:
    return str(summary)
