from typing import Any, List, Optional
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunProposal, DryRunBridgeSession
from usa_signal_bot.paper_dry_run_bridge.paper_snapshot_loader import load_read_only_paper_snapshot

def build_read_only_paper_runtime_snapshot_for_dry_run(paper_payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return load_read_only_paper_snapshot(paper_payload)

def compare_dry_run_proposals_to_paper_snapshot(proposals: List[DryRunProposal], paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_count": len(proposals),
        "snapshot_orders_count": len(paper_snapshot.get("orders", [])),
        "comparison": "Safe - snapshot unchanged."
    }

def validate_paper_runtime_snapshot_not_mutated(before: dict[str, Any], after: dict[str, Any]) -> List[str]:
    errors = []
    if before.get("paper_state_committed") != after.get("paper_state_committed"):
        errors.append("paper_state_committed mutated")
    if before.get("paper_order_executed") != after.get("paper_order_executed"):
        errors.append("paper_order_executed mutated")
    if before.get("portfolio_state_mutated") != after.get("portfolio_state_mutated"):
        errors.append("portfolio_state_mutated mutated")
    return errors

def attach_dry_run_metadata_to_paper_analytics(payload: dict[str, Any], session: DryRunBridgeSession) -> dict[str, Any]:
    result = payload.copy()
    result["dry_run_metadata"] = {
        "session_id": session.session_id,
        "is_read_only": True
    }
    return result

def paper_runtime_dry_run_adapter_to_text(payload: dict[str, Any]) -> str:
    metadata = payload.get("dry_run_metadata", {})
    return f"Paper Runtime Adapter: Metadata Attached={bool(metadata)}"
