from typing import Any
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    SimulatorDossierEvidenceItem,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerRule,
    PaperSandboxRuntimeAdmissionBlockerEvent,
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorDossierAuditEntry,
    SimulatorDossierFullReview
)
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_report import simulator_dossier_limitations_text

def simulator_dossier_evidence_item_to_text(item: SimulatorDossierEvidenceItem) -> str:
    return f"[{item.evidence_type}] Status: {item.status.value}, Available: {item.available}"

def simulator_acceptance_seal_to_text(item: SimulatorAcceptanceSeal) -> str:
    return f"Seal: {item.status.value}, Decision: {item.decision.value}, Sealed: {item.sealed}"

def sandbox_runtime_admission_blocker_rule_to_text(item: PaperSandboxRuntimeAdmissionBlockerRule) -> str:
    return f"Rule [{item.attempt_type.value}]: Enabled: {item.enabled}, Blocking: {item.blocking}"

def sandbox_runtime_admission_blocker_event_to_text(item: PaperSandboxRuntimeAdmissionBlockerEvent) -> str:
    return f"Event [{item.attempt_type.value}]: Blocked: {item.blocked}, Status: {item.status.value}"

def local_paper_admission_simulator_gate_dossier_to_text(item: LocalPaperAdmissionSimulatorGateDossier, limit: int = 100) -> str:
    lines = [
        f"--- Dossier: {item.dossier_id} ---",
        f"Status: {item.status.value}, Decision: {item.decision.value}",
        f"Sealed: {item.sealed}, Immutable: {item.immutable}",
        f"Evidence Items: {len(item.evidence_items)}"
    ]
    for ev in item.evidence_items[:limit]:
        lines.append(f"  - {simulator_dossier_evidence_item_to_text(ev)}")
    return "\n".join(lines)

def simulator_dossier_audit_entry_to_text(item: SimulatorDossierAuditEntry) -> str:
    return f"[{item.created_at_utc}] {item.action} on {item.entity_type}: {item.decision} - {item.rationale}"

def simulator_dossier_full_review_to_text(item: SimulatorDossierFullReview, limit: int = 100) -> str:
    lines = [
        f"=== Simulator Dossier Full Review: {item.review_id} ===",
        f"Dossiers: {len(item.dossiers)}",
        f"Seals: {len(item.acceptance_seals)}",
        f"Blocker Events: {len(item.sandbox_runtime_admission_blocker_events)}"
    ]

    for d in item.dossiers[:limit]:
        lines.append(local_paper_admission_simulator_gate_dossier_to_text(d, limit))

    for s in item.acceptance_seals[:limit]:
        lines.append(simulator_acceptance_seal_to_text(s))

    for e in item.sandbox_runtime_admission_blocker_events[:limit]:
        lines.append(sandbox_runtime_admission_blocker_event_to_text(e))

    lines.append("")
    lines.append(simulator_dossier_limitations_text())
    return "\n".join(lines)

def simulator_dossier_store_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "--- Simulator Dossier Store Summary ---"
    ]
    for k, v in summary.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)
