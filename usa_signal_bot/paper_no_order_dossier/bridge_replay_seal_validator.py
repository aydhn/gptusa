from typing import Any
import json
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import BridgeReplayAuditSeal
from usa_signal_bot.core.enums import BridgeReplayAuditSealStatus, BridgeReplayAuditSealDecision

def validate_bridge_replay_audit_seal_safety(seal: BridgeReplayAuditSeal) -> list[str]:
    reasons = []
    if not seal.sealed:
        reasons.append("seal is not sealed")
    if not seal.immutable:
        reasons.append("seal is not immutable")
    if not seal.replay_passed:
        reasons.append("replay_passed is false")
    if not seal.all_dangerous_routes_denied:
        reasons.append("all_dangerous_routes_denied is false")
    if seal.dangerous_allowed_count > 0:
        reasons.append(f"dangerous_allowed_count > 0 ({seal.dangerous_allowed_count})")
    if seal.missing_route_count > 0:
        reasons.append(f"missing_route_count > 0 ({seal.missing_route_count})")

    return reasons

def bridge_replay_seal_allows_admission(seal: BridgeReplayAuditSeal) -> bool:
    # Seal NEVER allows admission, it is metadata only
    return False

def bridge_replay_seal_requires_followup(seal: BridgeReplayAuditSeal) -> bool:
    return len(validate_bridge_replay_audit_seal_safety(seal)) > 0 or seal.status != BridgeReplayAuditSealStatus.SEALED

def bridge_replay_seal_blocks_next_stage(seal: BridgeReplayAuditSeal) -> bool:
    return len(validate_bridge_replay_audit_seal_safety(seal)) > 0

def bridge_replay_seal_validator_summary(seal: BridgeReplayAuditSeal) -> dict[str, Any]:
    return {
        "valid": not bridge_replay_seal_blocks_next_stage(seal),
        "reasons": validate_bridge_replay_audit_seal_safety(seal)
    }

def bridge_replay_seal_validator_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
