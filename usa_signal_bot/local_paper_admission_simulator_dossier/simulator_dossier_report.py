from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import SimulatorDossierReportType
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    SimulatorDossierFullReview,
    create_simulator_dossier_full_review_id,
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorAcceptanceSeal,
    PaperSandboxRuntimeAdmissionBlockerEvent,
    PaperSandboxRuntimeAdmissionBlockerRule
)
from usa_signal_bot.local_paper_admission_simulator_dossier.sandbox_runtime_admission_blocker_rules import default_sandbox_runtime_admission_blocker_rules
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_audit import audit_entry_from_simulator_dossier, audit_entry_from_simulator_acceptance_seal, audit_entry_from_sandbox_runtime_admission_blocker_events
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier import build_local_paper_admission_simulator_gate_dossier
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_acceptance_seal import build_simulator_acceptance_seal
from usa_signal_bot.local_paper_admission_simulator_dossier.sandbox_runtime_admission_attempt_simulator import simulate_sandbox_runtime_admission_attempts
from usa_signal_bot.local_paper_admission_simulator_dossier.dossier_evidence import collect_simulator_dossier_evidence

def simulator_dossier_limitations_text() -> str:
    return (
        "Simulator Dossier Limitations:\n"
        "- No broker/live/demo order.\n"
        "- No active paper enable.\n"
        "- No paper admission.\n"
        "- No simulator admission.\n"
        "- No local paper simulator start.\n"
        "- No paper sandbox runtime admission.\n"
        "- No paper sandbox runtime start.\n"
        "- No real paper mutation.\n"
        "- No paper order.\n"
        "- No Telegram real send.\n"
        "- No production config patch.\n"
        "- Simulator dossier is not activation.\n"
        "- Simulator acceptance seal is metadata-only.\n"
        "- Sandbox runtime admission blocker denies admission.\n"
        "- Not investment advice.\n"
    )

def build_simulator_dossier_review_from_parts(
    dossier: LocalPaperAdmissionSimulatorGateDossier,
    seal: SimulatorAcceptanceSeal | None = None,
    blocker_events: list[PaperSandboxRuntimeAdmissionBlockerEvent] | None = None
) -> SimulatorDossierFullReview:

    audit_entries = [audit_entry_from_simulator_dossier(dossier)]
    if seal:
        audit_entries.append(audit_entry_from_simulator_acceptance_seal(seal))
    if blocker_events:
        audit_entries.append(audit_entry_from_sandbox_runtime_admission_blocker_events(blocker_events))

    return SimulatorDossierFullReview(
        review_id=create_simulator_dossier_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=SimulatorDossierReportType.FULL_SIMULATOR_DOSSIER_REVIEW,
        dossiers=[dossier],
        evidence_items=dossier.evidence_items,
        acceptance_seals=[seal] if seal else [],
        sandbox_runtime_admission_blocker_rules=default_sandbox_runtime_admission_blocker_rules(),
        sandbox_runtime_admission_blocker_events=blocker_events or [],
        audit_entries=audit_entries,
        output_paths={},
        warnings=[],
        errors=[]
    )

def build_simulator_dossier_full_review(payload: dict[str, Any]) -> SimulatorDossierFullReview:
    dossier = build_local_paper_admission_simulator_gate_dossier(payload)
    dossier.evidence_items = collect_simulator_dossier_evidence(payload)
    seal = build_simulator_acceptance_seal(payload, dossier.evidence_items)
    blocker_events = simulate_sandbox_runtime_admission_attempts()
    return build_simulator_dossier_review_from_parts(dossier, seal, blocker_events)

def simulator_dossier_full_review_summary(review: SimulatorDossierFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "dossier_count": len(review.dossiers),
        "seal_count": len(review.acceptance_seals),
        "blocker_events_count": len(review.sandbox_runtime_admission_blocker_events)
    }

def simulator_dossier_full_review_to_text(review: SimulatorDossierFullReview, limit: int = 100) -> str:
    summary = simulator_dossier_full_review_summary(review)
    lines = [
        "--- Simulator Dossier Full Review ---",
        f"Review ID: {summary['review_id']}",
        f"Dossiers: {summary['dossier_count']}",
        f"Seals: {summary['seal_count']}",
        f"Blocker Events: {summary['blocker_events_count']}",
        "",
        simulator_dossier_limitations_text()
    ]
    return "\n".join(lines)
