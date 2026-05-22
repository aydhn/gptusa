
from typing import Any, List
from usa_signal_bot.core.enums import PaperReadinessBoardDecision, PaperReadinessBoardStatus, PaperReadinessBoardRiskFlag
from usa_signal_bot.paper_readiness_board.confirmation_ingestion import extract_human_review_bundle, extract_activation_still_denied_registry_entry, extract_activation_denied_state

def evaluate_paper_readiness_board_eligibility(confirmation_payload: dict) -> PaperReadinessBoardDecision:
    bundle = extract_human_review_bundle(confirmation_payload)
    registry = extract_activation_still_denied_registry_entry(confirmation_payload)
    denied, allowed = extract_activation_denied_state(confirmation_payload)

    if allowed:
        return PaperReadinessBoardDecision.BLOCK
    if not bundle:
        return PaperReadinessBoardDecision.REQUEST_MANUAL_REVIEW
    if not registry:
        return PaperReadinessBoardDecision.BLOCK
    if denied and bundle and registry:
        return PaperReadinessBoardDecision.PASS_WITH_ACTIVATION_DENIED
    return PaperReadinessBoardDecision.INCONCLUSIVE

def paper_readiness_board_eligibility_reasons(confirmation_payload: dict) -> List[str]:
    return ["Evaluated based on bundle, registry, and denied state."]

def board_safety_flags_from_confirmation(payload: dict) -> List[PaperReadinessBoardRiskFlag]:
    flags = []
    denied, allowed = extract_activation_denied_state(payload)
    if allowed: flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
    if not extract_human_review_bundle(payload): flags.append(PaperReadinessBoardRiskFlag.HUMAN_REVIEW_BUNDLE_MISSING)
    if not extract_activation_still_denied_registry_entry(payload): flags.append(PaperReadinessBoardRiskFlag.ACTIVATION_DENIAL_MISSING)
    return flags

def board_status_from_decision(decision: PaperReadinessBoardDecision) -> PaperReadinessBoardStatus:
    mapping = {
        PaperReadinessBoardDecision.PASS_WITH_ACTIVATION_DENIED: PaperReadinessBoardStatus.PASSED_WITH_ACTIVATION_DENIED,
        PaperReadinessBoardDecision.REQUEST_CONFIRMATION_REFRESH: PaperReadinessBoardStatus.REQUEST_CHANGES,
        PaperReadinessBoardDecision.REQUEST_FIREWALL_AUDIT_REFRESH: PaperReadinessBoardStatus.REQUEST_CHANGES,
        PaperReadinessBoardDecision.REQUEST_ZERO_MUTATION_RETEST: PaperReadinessBoardStatus.REQUEST_CHANGES,
        PaperReadinessBoardDecision.REQUEST_MANUAL_REVIEW: PaperReadinessBoardStatus.REVIEWING,
        PaperReadinessBoardDecision.REJECT: PaperReadinessBoardStatus.REJECTED,
        PaperReadinessBoardDecision.BLOCK: PaperReadinessBoardStatus.BLOCKED,
        PaperReadinessBoardDecision.INCONCLUSIVE: PaperReadinessBoardStatus.UNKNOWN,
        PaperReadinessBoardDecision.UNKNOWN: PaperReadinessBoardStatus.UNKNOWN
    }
    return mapping.get(decision, PaperReadinessBoardStatus.UNKNOWN)

def eligibility_checker_to_text(payload: dict) -> str:
    return str(payload)
