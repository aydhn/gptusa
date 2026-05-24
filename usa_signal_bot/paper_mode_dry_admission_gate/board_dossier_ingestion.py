from typing import Any, Tuple, List

def ingest_board_dossier_full_review(payload: dict[str, Any]) -> dict[str, Any]:
    return payload

def extract_board_dossier(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("board_dossier")

def extract_acceptance_board_seal(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("acceptance_board_seal")

def extract_shadow_launch_blocker_events(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("shadow_launch_blocker_events", [])

def extract_board_dossier_candidate_id(payload: dict[str, Any]) -> str | None:
    dossier = extract_board_dossier(payload)
    if dossier:
        return dossier.get("candidate_id")
    return None

def extract_board_dossier_decision(payload: dict[str, Any]) -> str | None:
    dossier = extract_board_dossier(payload)
    if dossier:
        return dossier.get("decision")
    return None

def board_dossier_supports_dry_admission_gate(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    supported = True
    dossier = extract_board_dossier(payload)
    seal = extract_acceptance_board_seal(payload)
    events = extract_shadow_launch_blocker_events(payload)

    if not dossier:
        supported = False
        reasons.append("Missing board dossier")
    elif dossier.get("decision") not in ["CREATE_BOARD_DOSSIER", "VALIDATED_NON_EXECUTION"]:
        supported = False
        reasons.append(f"Board dossier decision is {dossier.get('decision')}, expected CREATE_BOARD_DOSSIER or VALIDATED_NON_EXECUTION")

    if not seal:
        supported = False
        reasons.append("Missing acceptance board seal")
    elif seal.get("status") not in ["VALIDATED", "SEALED"]:
        supported = False
        reasons.append(f"Acceptance board seal status is {seal.get('status')}, expected VALIDATED or SEALED")

    if not events:
        supported = False
        reasons.append("Missing shadow-launch blocker events")

    if payload.get("shadow_launch_allowed"):
        supported = False
        reasons.append("shadow_launch_allowed is True")

    if payload.get("paper_mode_launch_allowed"):
        supported = False
        reasons.append("paper_mode_launch_allowed is True")

    if payload.get("activation_allowed"):
        supported = False
        reasons.append("activation_allowed is True")

    if payload.get("admission_allowed"):
        supported = False
        reasons.append("admission_allowed is True")

    if payload.get("transition_allowed"):
        supported = False
        reasons.append("transition_allowed is True")

    if payload.get("order_created"):
        supported = False
        reasons.append("order_created is True")

    if payload.get("mutation_detected"):
        supported = False
        reasons.append("mutation_detected is True")

    for event in events:
        if not event.get("blocked", True):
            supported = False
            reasons.append(f"ShadowLaunchBlockerEvent {event.get('event_id')} has blocked=False")

    return supported, reasons

def board_dossier_ingestion_to_text(payload: dict[str, Any]) -> str:
    supported, reasons = board_dossier_supports_dry_admission_gate(payload)
    text = f"Supports Dry Admission Gate: {supported}\n"
    if reasons:
        text += "Reasons:\n" + "\n".join(f"- {r}" for r in reasons)
    return text
