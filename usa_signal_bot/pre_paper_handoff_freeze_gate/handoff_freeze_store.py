from pathlib import Path
from typing import Any, List, Optional
from usa_signal_bot.core.serialization import serialize_value
from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json
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
    return ensure_dir(data_root / "pre_paper_handoff_freeze_gate")

def final_handoff_freeze_gates_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "gates")

def sandbox_replay_plans_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "sandbox_replay_plans")

def sandbox_replay_results_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "sandbox_replay_results")

def sandbox_replay_items_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "sandbox_replay_items")

def simulator_evidence_freezes_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "simulator_evidence_freezes")

def handoff_freeze_rules_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "rules")

def handoff_freeze_assertions_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "assertions")

def handoff_freeze_audit_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "audit")

def handoff_freeze_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(handoff_freeze_store_dir(data_root) / "full_reviews")

def write_final_handoff_freeze_gate_json(path: Path, item: FinalPrePaperHandoffFreezeGate) -> Path:
    return write_json(path, serialize_value(item), ensure_parent=False)

def write_sandbox_replay_plan_json(path: Path, item: SandboxRuntimeAdmissionReplayPlan) -> Path:
    return write_json(path, serialize_value(item), ensure_parent=False)

def write_sandbox_replay_result_json(path: Path, item: SandboxRuntimeAdmissionReplayResult) -> Path:
    return write_json(path, serialize_value(item), ensure_parent=False)

def write_sandbox_replay_items_jsonl(path: Path, items: List[SandboxRuntimeAdmissionReplayItem]) -> Path:
    return write_jsonl(path, (serialize_value(i) for i in items), ensure_parent=False)

def write_simulator_evidence_freeze_json(path: Path, item: SimulatorEvidenceFreezeBundle) -> Path:
    return write_json(path, serialize_value(item), ensure_parent=False)

def write_handoff_freeze_rules_jsonl(path: Path, items: List[HandoffFreezeRule]) -> Path:
    return write_jsonl(path, (serialize_value(i) for i in items), ensure_parent=False)

def write_handoff_freeze_assertions_jsonl(path: Path, items: List[HandoffFreezeAssertion]) -> Path:
    return write_jsonl(path, (serialize_value(i) for i in items), ensure_parent=False)

def write_handoff_freeze_audit_jsonl(path: Path, items: List[PrePaperHandoffFreezeAuditEntry]) -> Path:
    return write_jsonl(path, (serialize_value(i) for i in items), ensure_parent=False)

def write_handoff_freeze_full_review_json(path: Path, item: PrePaperHandoffFreezeFullReview) -> Path:
    return write_json(path, serialize_value(item), ensure_parent=False)

def read_handoff_freeze_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

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
