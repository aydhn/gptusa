from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeAuditEntry, PaperSandboxBridgeDryRun, NoOrderPaperSessionEmulation, BridgeReplayResult
from usa_signal_bot.core.enums import PaperSandboxBridgeRiskFlag
from datetime import datetime
from dataclasses import dataclass
@dataclass
class BridgeAuditEntryParams:
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    decision: str | None = None
    evidence_refs: list[str] | None = None
    risk_flags: list[PaperSandboxBridgeRiskFlag] | None = None

def create_bridge_audit_entry(params: BridgeAuditEntryParams) -> PaperSandboxBridgeAuditEntry: return PaperSandboxBridgeAuditEntry(audit_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", entity_type=params.entity_type, entity_id=params.entity_id, action=params.action, decision=params.decision, rationale=params.rationale, evidence_refs=params.evidence_refs or [], risk_flags=params.risk_flags or [], warnings=[], errors=[])
def audit_entry_from_bridge_dry_run(run: PaperSandboxBridgeDryRun) -> PaperSandboxBridgeAuditEntry: return create_bridge_audit_entry(BridgeAuditEntryParams("", "", "", ""))
def audit_entry_from_no_order_session(session: NoOrderPaperSessionEmulation) -> PaperSandboxBridgeAuditEntry: return create_bridge_audit_entry(BridgeAuditEntryParams("", "", "", ""))
def audit_entry_from_bridge_replay_result(result: BridgeReplayResult) -> PaperSandboxBridgeAuditEntry: return create_bridge_audit_entry(BridgeAuditEntryParams("", "", "", ""))
def append_bridge_audit_entry(entries: list[PaperSandboxBridgeAuditEntry], entry: PaperSandboxBridgeAuditEntry) -> list[PaperSandboxBridgeAuditEntry]: return entries + [entry]
def bridge_audit_summary(entries: list[PaperSandboxBridgeAuditEntry]) -> dict[str, Any]: return {}
def bridge_audit_to_text(entries: list[PaperSandboxBridgeAuditEntry], limit: int = 100) -> str: return ""
