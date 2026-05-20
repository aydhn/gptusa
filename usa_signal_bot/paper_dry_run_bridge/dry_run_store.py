import json
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
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_run_contexts_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_run_sessions_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_run_proposals_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "proposals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def bridge_telemetry_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "telemetry"
    d.mkdir(parents=True, exist_ok=True)
    return d

def human_checkpoints_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "checkpoints"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_run_reviews_dir(data_root: Path) -> Path:
    d = dry_run_bridge_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_dry_run_context_json(path: Path, item: DryRunBridgeContext) -> Path:
    with open(path, "w") as f:
        json.dump(dry_run_bridge_context_to_dict(item), f, indent=2)
    return path

def write_dry_run_session_json(path: Path, item: DryRunBridgeSession) -> Path:
    with open(path, "w") as f:
        json.dump(dry_run_bridge_session_to_dict(item), f, indent=2)
    return path

def write_dry_run_proposals_jsonl(path: Path, items: List[DryRunProposal]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_run_proposal_to_dict(item)) + "\n")
    return path

def write_bridge_telemetry_jsonl(path: Path, items: List[BridgeTelemetryEvent]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(bridge_telemetry_event_to_dict(item)) + "\n")
    return path

def write_human_checkpoints_jsonl(path: Path, items: List[HumanReviewCheckpoint]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(human_review_checkpoint_to_dict(item)) + "\n")
    return path

def write_dry_run_bridge_review_json(path: Path, item: DryRunBridgeReview) -> Path:
    with open(path, "w") as f:
        json.dump(dry_run_bridge_review_to_dict(item), f, indent=2)
    return path

def read_dry_run_bridge_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_dry_run_bridge_reviews(data_root: Path) -> List[Path]:
    d = dry_run_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), reverse=True)

def get_latest_dry_run_bridge_review(data_root: Path) -> Optional[Path]:
    reviews = list_dry_run_bridge_reviews(data_root)
    return reviews[0] if reviews else None

def dry_run_bridge_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "contexts": len(list(dry_run_contexts_dir(data_root).glob("*.json"))),
        "sessions": len(list(dry_run_sessions_dir(data_root).glob("*.json"))),
        "proposals": len(list(dry_run_proposals_dir(data_root).glob("*.jsonl"))),
        "telemetry": len(list(bridge_telemetry_dir(data_root).glob("*.jsonl"))),
        "checkpoints": len(list(human_checkpoints_dir(data_root).glob("*.jsonl"))),
        "reviews": len(list(dry_run_reviews_dir(data_root).glob("*.json")))
    }
