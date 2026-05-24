from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import AcceptanceBoardSeal

def validate_acceptance_board_seal_safety(seal: AcceptanceBoardSeal) -> list[str]:
    issues = []

    if not seal.sealed:
        issues.append("Seal is not sealed")
    if not seal.immutable:
        issues.append("Seal is not immutable")
    if not seal.seal_is_metadata_only:
        issues.append("Seal must be metadata_only")

    if not seal.board_gates_passed:
        issues.append("Board gates not passed")
    if not seal.board_assertions_passed:
        issues.append("Board assertions not passed")
    if not seal.runtime_replay_passed:
        issues.append("Runtime replay not passed")
    if not seal.all_dangerous_runtime_routes_denied:
        issues.append("Not all dangerous runtime routes denied")
    if not seal.non_execution_seal_integrity_valid:
        issues.append("Non-execution seal integrity invalid")

    if seal.allows_shadow_launch:
        issues.append("Seal allows shadow launch")
    if seal.allows_paper_mode_launch:
        issues.append("Seal allows paper mode launch")
    if seal.allows_active_paper:
        issues.append("Seal allows active paper")
    if seal.allows_broker_execution:
        issues.append("Seal allows broker execution")
    if seal.allows_paper_state_mutation:
        issues.append("Seal allows paper state mutation")
    if seal.allows_config_patch:
        issues.append("Seal allows config patch")
    if seal.allows_telegram_real_send:
        issues.append("Seal allows telegram real send")

    return issues

def acceptance_board_seal_allows_shadow_launch(seal: AcceptanceBoardSeal) -> bool:
    return seal.allows_shadow_launch or seal.allows_paper_mode_launch

def acceptance_board_seal_allows_execution(seal: AcceptanceBoardSeal) -> bool:
    return (
        seal.allows_active_paper or
        seal.allows_broker_execution or
        seal.allows_paper_state_mutation or
        seal.allows_config_patch or
        seal.allows_telegram_real_send
    )

def acceptance_board_seal_requires_followup(seal: AcceptanceBoardSeal) -> bool:
    return len(seal.required_followups) > 0 or len(seal.warnings) > 0 or len(seal.errors) > 0

def acceptance_board_seal_blocks_next_stage(seal: AcceptanceBoardSeal) -> bool:
    return seal.decision.name == "BLOCK" or len(validate_acceptance_board_seal_safety(seal)) > 0

def acceptance_board_seal_validator_summary(seal: AcceptanceBoardSeal) -> dict[str, Any]:
    issues = validate_acceptance_board_seal_safety(seal)
    return {
        "valid": len(issues) == 0,
        "issue_count": len(issues),
        "allows_shadow_launch": acceptance_board_seal_allows_shadow_launch(seal),
        "allows_execution": acceptance_board_seal_allows_execution(seal),
        "blocks_next_stage": acceptance_board_seal_blocks_next_stage(seal)
    }

def acceptance_board_seal_validator_to_text(payload: dict[str, Any]) -> str:
    lines = [f"Seal Validator (Valid: {payload.get('valid')})"]
    if payload.get("issue_count", 0) > 0:
        lines.append(f"  Found {payload.get('issue_count')} issues blocking safety")
    lines.append(f"  Blocks Next Stage: {payload.get('blocks_next_stage')}")
    return "\n".join(lines)
