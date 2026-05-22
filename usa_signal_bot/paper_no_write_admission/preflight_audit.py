from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWriteAdmissionAuditEntry, NoWritePaperAdmissionContract, ActivationReplayResult, PaperModePreflightRun
from usa_signal_bot.core.enums import NoWriteAdmissionRiskFlag
import datetime

def create_no_write_admission_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, decision: str | None = None, evidence_refs: list[str] | None = None, risk_flags: list[NoWriteAdmissionRiskFlag] | None = None) -> NoWriteAdmissionAuditEntry:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return NoWriteAdmissionAuditEntry(
        audit_id="a1", created_at_utc=now, entity_type=entity_type, entity_id=entity_id, action=action, decision=decision, rationale=rationale,
        evidence_refs=evidence_refs or [], risk_flags=risk_flags or [], warnings=[], errors=[]
    )

def audit_entry_from_contract(contract: NoWritePaperAdmissionContract) -> NoWriteAdmissionAuditEntry:
    return create_no_write_admission_audit_entry("contract", contract.contract_id, "create", "")

def audit_entry_from_activation_replay_result(result: ActivationReplayResult) -> NoWriteAdmissionAuditEntry:
    return create_no_write_admission_audit_entry("replay", result.replay_result_id, "replay", "")

def audit_entry_from_preflight_run(run: PaperModePreflightRun) -> NoWriteAdmissionAuditEntry:
    return create_no_write_admission_audit_entry("preflight", run.preflight_id, "preflight", "")

def append_no_write_admission_audit_entry(entries: list[NoWriteAdmissionAuditEntry], entry: NoWriteAdmissionAuditEntry) -> list[NoWriteAdmissionAuditEntry]:
    entries.append(entry)
    return entries

def no_write_admission_audit_summary(entries: list[NoWriteAdmissionAuditEntry]) -> dict[str, Any]:
    return {}

def no_write_admission_audit_to_text(entries: list[NoWriteAdmissionAuditEntry], limit: int = 100) -> str:
    return "Audit"
