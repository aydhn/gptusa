from typing import Any
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    PrePaperHandoffFreezeFullReview
)
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_plan import build_sandbox_runtime_admission_replay_plan
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_engine import SandboxRuntimeAdmissionBlockerReplayEngine
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_evidence_freeze import build_simulator_evidence_freeze_bundle
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_rules import build_handoff_freeze_rules
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_assertions import build_handoff_freeze_assertions
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import build_final_pre_paper_handoff_freeze_gate
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_report import build_handoff_freeze_review_from_parts
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_dossier_ingestion import extract_sandbox_runtime_admission_blocker_events

def sandbox_runtime_admission_replay_result_from_simulator_dossier(payload: dict[str, Any]) -> SandboxRuntimeAdmissionReplayResult:
    plan = build_sandbox_runtime_admission_replay_plan(payload)
    events = extract_sandbox_runtime_admission_blocker_events(payload)
    engine = SandboxRuntimeAdmissionBlockerReplayEngine()
    return engine.replay(plan, events)

def simulator_evidence_freeze_from_simulator_dossier(payload: dict[str, Any]) -> SimulatorEvidenceFreezeBundle:
    return build_simulator_evidence_freeze_bundle(payload)

def handoff_freeze_gate_from_simulator_dossier(payload: dict[str, Any]) -> FinalPrePaperHandoffFreezeGate:
    gate = build_final_pre_paper_handoff_freeze_gate(payload)
    replay = sandbox_runtime_admission_replay_result_from_simulator_dossier(payload)
    freeze = simulator_evidence_freeze_from_simulator_dossier(payload)

    gate.sandbox_replay_result = replay
    gate.evidence_freeze = freeze
    gate.rules = build_handoff_freeze_rules(payload, replay, freeze)
    gate.assertions = build_handoff_freeze_assertions(payload, replay, freeze)

    return gate

def handoff_freeze_full_review_from_simulator_dossier(payload: dict[str, Any]) -> PrePaperHandoffFreezeFullReview:
    gate = handoff_freeze_gate_from_simulator_dossier(payload)
    return build_handoff_freeze_review_from_parts(gate, gate.sandbox_replay_result, gate.evidence_freeze)

def attach_handoff_freeze_metadata_to_simulator_dossier_payload(payload: dict[str, Any], review: PrePaperHandoffFreezeFullReview) -> dict[str, Any]:
    res = dict(payload)
    res["pre_paper_handoff_freeze"] = {
        "review_id": review.review_id,
        "gates": [g.gate_id for g in review.gates],
        "passed": all(g.pre_paper_handoff_complete for g in review.gates)
    }
    return res

def simulator_dossier_handoff_freeze_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("pre_paper_handoff_freeze", {})

def simulator_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = simulator_dossier_handoff_freeze_summary(payload)
    return f"Simulator Dossier Adapter - Handoff Freeze: {summary}"
