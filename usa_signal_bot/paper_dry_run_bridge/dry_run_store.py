from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json, list_files, count_files
from pathlib import Path
from typing import Any, List, Optional
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunBridgeSession,
    DryRunProposal,
    BridgeTelemetryEvent,
    HumanReviewCheckpoint,
    DryRunBridgeReview,
    dry_run_bridge_context_to_dict,
    dry_run_bridge_session_to_dict,
    dry_run_proposal_to_dict,
    bridge_telemetry_event_to_dict,
    human_review_checkpoint_to_dict,
    dry_run_bridge_review_to_dict
)

def dry_run_bridge_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_dry_run_bridge"
    ensure_dir(d)
    return d

def dry_run_contexts_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "contexts"
    ensure_dir(d)
    return d

def dry_run_sessions_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "sessions"
    ensure_dir(d)
    return d

def dry_run_proposals_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "proposals"
    ensure_dir(d)
    return d

def bridge_telemetry_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "telemetry"
    ensure_dir(d)
    return d

def human_checkpoints_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "checkpoints"
    ensure_dir(d)
    return d

def dry_run_reviews_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "reviews"
    ensure_dir(d)
    return d

def write_dry_run_context_json(path: Path, item: DryRunBridgeContext) -> Path:
    return write_json(path, dry_run_bridge_context_to_dict(item), ensure_parent=False)

def write_dry_run_session_json(path: Path, item: DryRunBridgeSession) -> Path:
    return write_json(path, dry_run_bridge_session_to_dict(item), ensure_parent=False)

def write_dry_run_proposals_jsonl(path: Path, items: List[DryRunProposal]) -> Path:
    return write_jsonl(path, (dry_run_proposal_to_dict(item) for item in items), ensure_parent=False)

def write_bridge_telemetry_jsonl(path: Path, items: List[BridgeTelemetryEvent]) -> Path:
    return write_jsonl(path, (bridge_telemetry_event_to_dict(item) for item in items), ensure_parent=False)

def write_human_checkpoints_jsonl(path: Path, items: List[HumanReviewCheckpoint]) -> Path:
    return write_jsonl(path, (human_review_checkpoint_to_dict(item) for item in items), ensure_parent=False)

def write_dry_run_bridge_review_json(path: Path, item: DryRunBridgeReview) -> Path:
    return write_json(path, dry_run_bridge_review_to_dict(item), ensure_parent=False)

def read_dry_run_bridge_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_dry_run_bridge_reviews(data_root: Path) -> List[Path]:
    d = dry_run_reviews_dir(data_root)
    return list_files(d, "*.json", reverse=True)

def get_latest_dry_run_bridge_review(data_root: Path) -> Optional[Path]:
    reviews = list_dry_run_bridge_reviews(data_root)
    return reviews[0] if reviews else None

def dry_run_bridge_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "contexts": count_files(dry_run_contexts_dir(data_root), "*.json"),
        "sessions": count_files(dry_run_sessions_dir(data_root), "*.json"),
        "proposals": count_files(dry_run_proposals_dir(data_root), "*.jsonl"),
        "telemetry": count_files(bridge_telemetry_dir(data_root), "*.jsonl"),
        "checkpoints": count_files(human_checkpoints_dir(data_root), "*.jsonl"),
        "reviews": count_files(dry_run_reviews_dir(data_root), "*.json")
    }
