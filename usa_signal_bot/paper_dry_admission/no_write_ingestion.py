from typing import Any, Tuple, List
from usa_signal_bot.core.enums import PaperModePreflightDecision

def ingest_no_write_admission_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.copy()

def extract_no_write_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    contracts = payload.get("contracts", [])
    if contracts:
        return contracts[-1]
    return None

def extract_activation_replay_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    replays = payload.get("replays", [])
    if replays:
        return replays[-1]
    return None

def extract_paper_mode_preflight(payload: dict[str, Any]) -> dict[str, Any] | None:
    preflights = payload.get("preflights", [])
    if preflights:
        return preflights[-1]
    return None

def extract_no_write_candidate_id(payload: dict[str, Any]) -> str | None:
    preflight = extract_paper_mode_preflight(payload)
    if preflight:
        return preflight.get("candidate_id")
    contract = extract_no_write_contract(payload)
    if contract:
        return contract.get("candidate_id")
    return None

def extract_no_write_decision(payload: dict[str, Any]) -> str | None:
    preflight = extract_paper_mode_preflight(payload)
    if preflight:
        return preflight.get("decision")
    return None

def no_write_supports_dry_admission(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    supported = True

    contract = extract_no_write_contract(payload)
    if not contract:
        reasons.append("Missing no-write contract")
        supported = False
    elif contract.get("activation_allowed", True):
        reasons.append("No-write contract allows activation")
        supported = False
    elif not contract.get("activation_denied", False):
        reasons.append("No-write contract does not explicitly deny activation")
        supported = False

    replay = extract_activation_replay_result(payload)
    if not replay:
        reasons.append("Missing activation replay")
        supported = False

    preflight = extract_paper_mode_preflight(payload)
    if not preflight:
        reasons.append("Missing paper mode preflight")
        supported = False
    elif preflight.get("decision") != PaperModePreflightDecision.PASS_NO_WRITE_PREFLIGHT.value:
        reasons.append(f"Preflight decision is not PASS_NO_WRITE_PREFLIGHT: {preflight.get('decision')}")
        supported = False
    elif preflight.get("mutation_detected", True):
        reasons.append("Preflight detected mutation")
        supported = False
    elif not preflight.get("all_writes_blocked", False):
        reasons.append("Preflight did not block all writes")
        supported = False
    elif preflight.get("activation_allowed", True):
        reasons.append("Preflight allowed activation")
        supported = False

    return supported, reasons

def no_write_ingestion_to_text(payload: dict[str, Any]) -> str:
    lines = []
    contract = extract_no_write_contract(payload)
    replay = extract_activation_replay_result(payload)
    preflight = extract_paper_mode_preflight(payload)

    lines.append(f"No-Write Contract: {'Present' if contract else 'Missing'}")
    lines.append(f"Activation Replay: {'Present' if replay else 'Missing'}")
    lines.append(f"Paper Mode Preflight: {'Present' if preflight else 'Missing'}")

    supported, reasons = no_write_supports_dry_admission(payload)
    lines.append(f"Supports Dry Admission: {supported}")
    if reasons:
        lines.append("Block Reasons:")
        for r in reasons:
            lines.append(f"  - {r}")

    return "\n".join(lines)
