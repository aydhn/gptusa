import os

path1 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_store.py"
content1 = """import json
from pathlib import Path
from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionGateDossier,
    DryAdmissionDossierEvidenceItem,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerRule,
    PaperModeRehearsalBlockerEvent,
    DryAdmissionDossierAuditEntry,
    DryAdmissionDossierFullReview,
    dry_admission_gate_dossier_to_dict,
    dry_admission_dossier_evidence_item_to_dict,
    dry_admission_acceptance_seal_to_dict,
    rehearsal_blocker_rule_to_dict,
    rehearsal_blocker_event_to_dict,
    dry_admission_dossier_audit_entry_to_dict,
    dry_admission_dossier_full_review_to_dict
)

def dry_admission_dossier_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_mode_dry_admission_dossier"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossiers_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "dossiers"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossier_evidence_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "evidence"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_acceptance_seals_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "acceptance_seals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_blocker_rules_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "rehearsal_blocker_rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def rehearsal_blocker_events_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "rehearsal_blocker_events"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossier_audit_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_dossier_full_reviews_dir(data_root: Path) -> Path:
    d = dry_admission_dossier_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_dry_admission_dossier_json(path: Path, item: DryAdmissionGateDossier) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_gate_dossier_to_dict(item), f, indent=2)
    return path

def write_dry_admission_dossier_evidence_jsonl(path: Path, items: list[DryAdmissionDossierEvidenceItem]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_dossier_evidence_item_to_dict(item)) + "\\n")
    return path

def write_dry_admission_acceptance_seal_json(path: Path, item: DryAdmissionAcceptanceSeal) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_acceptance_seal_to_dict(item), f, indent=2)
    return path

def write_rehearsal_blocker_rules_jsonl(path: Path, items: list[PaperModeRehearsalBlockerRule]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(rehearsal_blocker_rule_to_dict(item)) + "\\n")
    return path

def write_rehearsal_blocker_events_jsonl(path: Path, items: list[PaperModeRehearsalBlockerEvent]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(rehearsal_blocker_event_to_dict(item)) + "\\n")
    return path

def write_dry_admission_dossier_audit_jsonl(path: Path, items: list[DryAdmissionDossierAuditEntry]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_dossier_audit_entry_to_dict(item)) + "\\n")
    return path

def write_dry_admission_dossier_full_review_json(path: Path, item: DryAdmissionDossierFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(dry_admission_dossier_full_review_to_dict(item), f, indent=2)
    return path

def read_dry_admission_dossier_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_dry_admission_dossier_full_reviews(data_root: Path) -> list[Path]:
    d = dry_admission_dossier_full_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_dry_admission_dossier_full_review(data_root: Path) -> Path | None:
    reviews = list_dry_admission_dossier_full_reviews(data_root)
    return reviews[0] if reviews else None

def dry_admission_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    try:
        reviews = list_dry_admission_dossier_full_reviews(data_root)
        dossiers = list(dry_admission_dossiers_dir(data_root).glob("*.json"))
        seals = list(dry_admission_acceptance_seals_dir(data_root).glob("*.json"))
        return {
            "reviews": len(reviews),
            "dossiers": len(dossiers),
            "seals": len(seals)
        }
    except Exception:
        return {"reviews": 0, "dossiers": 0, "seals": 0}
"""

path2 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_validation.py"
content2 = """from dataclasses import dataclass, field
from typing import Any
import json

from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionGateDossier,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerEvent,
    DryAdmissionDossierFullReview
)
from usa_signal_bot.core.exceptions import DryAdmissionDossierValidationError

@dataclass
class DryAdmissionDossierValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class DryAdmissionDossierValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[DryAdmissionDossierValidationIssue]
    warnings: list[str]
    errors: list[str]

def _create_report(issues: list[DryAdmissionDossierValidationIssue]) -> DryAdmissionDossierValidationReport:
    errors = [i.message for i in issues if i.severity in ["ERROR", "BLOCKED"]]
    warnings = [i.message for i in issues if i.severity == "WARNING"]
    return DryAdmissionDossierValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len([i for i in issues if i.severity == "ERROR"]),
        blocked_count=len([i for i in issues if i.severity == "BLOCKED"]),
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_dry_admission_dossier_report(item: DryAdmissionGateDossier) -> DryAdmissionDossierValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "activation_denied", "Dossier activation not denied"))
    if item.activation_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "activation_allowed", "Dossier allows activation"))
    if item.admission_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "admission_allowed", "Dossier allows admission"))
    if item.transition_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "transition_allowed", "Dossier allows transition"))
    if item.shadow_launch_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "shadow_launch_allowed", "Dossier allows shadow launch"))
    if item.paper_mode_launch_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "paper_mode_launch_allowed", "Dossier allows paper mode launch"))
    if item.rehearsal_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "rehearsal_allowed", "Dossier allows rehearsal"))
    if item.paper_mode_rehearsal_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "paper_mode_rehearsal_allowed", "Dossier allows paper mode rehearsal"))
    if not item.all_writes_blocked:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "all_writes_blocked", "Dossier writes not all blocked"))
    if item.order_created:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "order_created", "Dossier order created"))
    if item.mutation_detected:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "mutation_detected", "Dossier mutation detected"))
    if item.allows_active_paper:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_active_paper", "Dossier allows active paper"))
    if item.allows_broker_execution:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_broker_execution", "Dossier allows broker execution"))
    if item.allows_paper_state_mutation:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_paper_state_mutation", "Dossier allows paper state mutation"))
    if item.allows_config_patch:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_config_patch", "Dossier allows config patch"))
    if item.allows_telegram_real_send:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_telegram_real_send", "Dossier allows telegram real send"))

    return _create_report(issues)

def validate_dry_admission_acceptance_seal_report(item: DryAdmissionAcceptanceSeal) -> DryAdmissionDossierValidationReport:
    issues = []
    if item.allows_rehearsal:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_rehearsal", "Seal allows rehearsal"))
    if item.allows_paper_mode_rehearsal:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "allows_paper_mode_rehearsal", "Seal allows paper mode rehearsal"))
    return _create_report(issues)

def validate_rehearsal_blocker_event_report(item: PaperModeRehearsalBlockerEvent) -> DryAdmissionDossierValidationReport:
    issues = []
    if not item.blocked:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "blocked", "Rehearsal attempt not blocked"))
    if item.rehearsal_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "rehearsal_allowed", "Rehearsal allowed"))
    if item.paper_mode_rehearsal_allowed:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "paper_mode_rehearsal_allowed", "Paper mode rehearsal allowed"))
    if item.active_paper_enabled:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "active_paper_enabled", "Active paper enabled"))
    if item.order_created:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "order_created", "Order created"))
    if item.paper_state_mutated:
        issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "paper_state_mutated", "Paper state mutated"))
    return _create_report(issues)

def validate_dry_admission_dossier_full_review_report(item: DryAdmissionDossierFullReview) -> DryAdmissionDossierValidationReport:
    issues = []
    for dossier in item.dossiers:
        issues.extend(validate_dry_admission_dossier_report(dossier).issues)
    for seal in item.acceptance_seals:
        issues.extend(validate_dry_admission_acceptance_seal_report(seal).issues)
    for event in item.rehearsal_blocker_events:
        issues.extend(validate_rehearsal_blocker_event_report(event).issues)

    txt = json.dumps(dry_admission_dossier_full_review_to_dict(item))
    issues.extend(validate_no_live_execution_language_in_dry_admission_dossier(txt).issues)
    issues.extend(validate_no_active_paper_language_in_dry_admission_dossier(txt).issues)
    issues.extend(validate_no_rehearsal_language_in_dry_admission_dossier(txt).issues)

    payload = dry_admission_dossier_full_review_to_dict(item)
    issues.extend(validate_no_broker_execution_fields_in_dry_admission_dossier(payload).issues)
    issues.extend(validate_no_paper_state_mutation_fields_in_dry_admission_dossier(payload).issues)

    return _create_report(issues)

def validate_no_sensitive_data_in_dry_admission_dossier_payload(payload: dict[str, Any]) -> DryAdmissionDossierValidationReport:
    issues = []
    txt = json.dumps(payload).lower()
    for secret in ["api_key", "secret", "password", "token"]:
        if f'"{secret}"' in txt:
            issues.append(DryAdmissionDossierValidationIssue("ERROR", "secret", f"Potential secret {secret} found"))
    return _create_report(issues)

def validate_no_live_execution_language_in_dry_admission_dossier(text: str) -> DryAdmissionDossierValidationReport:
    issues = []
    txt = text.lower()
    for phrase in ["live approved", "sent to broker", "kesin al", "garanti", "gerçek emir", "kesin kâr", "candidate kesin iyi", "canlıya al"]:
        if phrase in txt:
            issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "language", f"Live execution language found: {phrase}"))
    return _create_report(issues)

def validate_no_active_paper_language_in_dry_admission_dossier(text: str) -> DryAdmissionDossierValidationReport:
    issues = []
    txt = text.lower()
    for phrase in ["paper'a uygula", "aktif et", "shadow launch başlat", "paper mode başlat"]:
        if phrase in txt:
            issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "language", f"Active paper language found: {phrase}"))
    return _create_report(issues)

def validate_no_rehearsal_language_in_dry_admission_dossier(text: str) -> DryAdmissionDossierValidationReport:
    issues = []
    txt = text.lower()
    for phrase in ["rehearsal başlat"]:
        if phrase in txt:
            issues.append(DryAdmissionDossierValidationIssue("BLOCKED", "language", f"Rehearsal language found: {phrase}"))
    return _create_report(issues)

def validate_no_paper_state_mutation_fields_in_dry_admission_dossier(payload: dict[str, Any]) -> DryAdmissionDossierValidationReport:
    issues = []
    txt = json.dumps(payload)
    for field in ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if f'"{field}": true' in txt.lower() or f'"{field}": True' in txt:
            issues.append(DryAdmissionDossierValidationIssue("BLOCKED", field, f"Paper state mutation field {field} is true"))
    return _create_report(issues)

def validate_no_broker_execution_fields_in_dry_admission_dossier(payload: dict[str, Any]) -> DryAdmissionDossierValidationReport:
    issues = []
    txt = json.dumps(payload)
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f'"{field}"' in txt:
            issues.append(DryAdmissionDossierValidationIssue("BLOCKED", field, f"Broker execution field {field} found"))
    return _create_report(issues)

def dry_admission_dossier_validation_report_to_text(report: DryAdmissionDossierValidationReport) -> str:
    text = f"Validation Report: {'VALID' if report.valid else 'INVALID'}\n"
    text += f"- Issues: {report.issue_count} (Errors: {report.error_count}, Blocked: {report.blocked_count}, Warnings: {report.warning_count})\n"
    if not report.valid:
        text += f"- Errors: {', '.join(report.errors[:5])}\n"
    return text

def assert_dry_admission_dossier_valid(report: DryAdmissionDossierValidationReport) -> None:
    if not report.valid:
        raise DryAdmissionDossierValidationError(f"Dossier is invalid. Blocked: {report.blocked_count}, Errors: {report.error_count}")
"""

path3 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_reporting.py"
content3 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionGateDossier,
    DryAdmissionDossierEvidenceItem,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerRule,
    PaperModeRehearsalBlockerEvent,
    DryAdmissionDossierAuditEntry,
    DryAdmissionDossierFullReview
)
from usa_signal_bot.paper_mode_dry_admission_dossier.dossier_evidence import dry_admission_dossier_evidence_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_acceptance_seal import dry_admission_acceptance_seal_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import rehearsal_blocker_rules_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import dry_admission_dossier_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_audit import dry_admission_dossier_audit_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_report import dry_admission_dossier_full_review_to_text, dry_admission_dossier_limitations_text

def dry_admission_dossier_evidence_item_to_text(item: DryAdmissionDossierEvidenceItem) -> str:
    return f"Evidence [{item.evidence_type}]: {item.status.value}"

def rehearsal_blocker_rule_to_text(item: PaperModeRehearsalBlockerRule) -> str:
    return f"Rule [{item.attempt_type.value}]: Blocking={item.blocking}"

def rehearsal_blocker_event_to_text(item: PaperModeRehearsalBlockerEvent) -> str:
    return f"Event [{item.attempt_type.value}]: Blocked={item.blocked}"

def dry_admission_gate_dossier_to_text(item: DryAdmissionGateDossier, limit: int = 100) -> str:
    return dry_admission_dossier_to_text(item, limit)

def dry_admission_dossier_audit_entry_to_text(item: DryAdmissionDossierAuditEntry) -> str:
    return f"Audit [{item.entity_type} - {item.action}]: {item.decision}"

def dry_admission_dossier_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Dossier Store: {summary['reviews']} reviews, {summary['dossiers']} dossiers, {summary['seals']} seals"
"""

with open(path1, "w") as f:
    f.write(content1)
with open(path2, "w") as f:
    f.write(content2)
with open(path3, "w") as f:
    f.write(content3)

print("Store, validation and reporting created")
