import json
from pathlib import Path
from typing import Any, List, Optional
from usa_signal_bot.core.serialization import serialize_value
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    FinalPrePaperHandoffFreezeGate,
    SandboxRuntimeAdmissionReplayPlan,
    SandboxRuntimeAdmissionReplayResult,
    SandboxRuntimeAdmissionReplayItem,
    SimulatorEvidenceFreezeBundle,
    HandoffFreezeRule,
    HandoffFreezeAssertion,
    PrePaperHandoffFreezeAuditEntry,
    PrePaperHandoffFreezeFullReview
)

def handoff_freeze_store_dir(data_root: Path) -> Path:
    d = data_root / "pre_paper_handoff_freeze_gate"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_handoff_freeze_gates_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_replay_plans_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "sandbox_replay_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_replay_results_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "sandbox_replay_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def sandbox_replay_items_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "sandbox_replay_items"
    d.mkdir(parents=True, exist_ok=True)
    return d

def simulator_evidence_freezes_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "simulator_evidence_freezes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def handoff_freeze_rules_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def handoff_freeze_assertions_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "assertions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def handoff_freeze_audit_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def handoff_freeze_full_reviews_dir(data_root: Path) -> Path:
    d = handoff_freeze_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_final_handoff_freeze_gate_json(path: Path, item: FinalPrePaperHandoffFreezeGate) -> Path:
    with open(path, "w") as f:
        json.dump(serialize_value(item), f, indent=2)
    return path

def write_sandbox_replay_plan_json(path: Path, item: SandboxRuntimeAdmissionReplayPlan) -> Path:
    with open(path, "w") as f:
        json.dump(serialize_value(item), f, indent=2)
    return path

def write_sandbox_replay_result_json(path: Path, item: SandboxRuntimeAdmissionReplayResult) -> Path:
    with open(path, "w") as f:
        json.dump(serialize_value(item), f, indent=2)
    return path

def write_sandbox_replay_items_jsonl(path: Path, items: List[SandboxRuntimeAdmissionReplayItem]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(serialize_value(i)) + "\n")
    return path

def write_simulator_evidence_freeze_json(path: Path, item: SimulatorEvidenceFreezeBundle) -> Path:
    with open(path, "w") as f:
        json.dump(serialize_value(item), f, indent=2)
    return path

def write_handoff_freeze_rules_jsonl(path: Path, items: List[HandoffFreezeRule]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(serialize_value(i)) + "\n")
    return path

def write_handoff_freeze_assertions_jsonl(path: Path, items: List[HandoffFreezeAssertion]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(serialize_value(i)) + "\n")
    return path

def write_handoff_freeze_audit_jsonl(path: Path, items: List[PrePaperHandoffFreezeAuditEntry]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(serialize_value(i)) + "\n")
    return path

def write_handoff_freeze_full_review_json(path: Path, item: PrePaperHandoffFreezeFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(serialize_value(item), f, indent=2)
    return path

def read_handoff_freeze_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_handoff_freeze_full_reviews(data_root: Path) -> List[Path]:
    d = handoff_freeze_full_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_handoff_freeze_full_review(data_root: Path) -> Optional[Path]:
    files = list_handoff_freeze_full_reviews(data_root)
    return files[-1] if files else None

def handoff_freeze_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "gates": len(list(final_handoff_freeze_gates_dir(data_root).glob("*.json"))),
        "replay_plans": len(list(sandbox_replay_plans_dir(data_root).glob("*.json"))),
        "replay_results": len(list(sandbox_replay_results_dir(data_root).glob("*.json"))),
        "evidence_freezes": len(list(simulator_evidence_freezes_dir(data_root).glob("*.json"))),
        "full_reviews": len(list_handoff_freeze_full_reviews(data_root))
    }
