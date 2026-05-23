from typing import Any, Dict, List, Optional, Tuple
import json
from usa_signal_bot.core.exceptions import NonExecutionBoardDossierIngestionError

def ingest_paper_safe_dossier_full_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload:
        raise NonExecutionBoardDossierIngestionError("Payload cannot be empty")

    if "boards" in payload and "report_type" in payload:
        # Avoid double-ingestion
        return payload

    return payload

def extract_paper_safe_gate_dossier(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("paper_safe_gate_dossiers", [None])[0] if "paper_safe_gate_dossiers" in payload else None

def extract_non_execution_acceptance_seal(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("non_execution_acceptance_seals", [None])[0] if "non_execution_acceptance_seals" in payload else None

def extract_pre_paper_runtime_map(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("pre_paper_local_runtime_maps", [None])[0] if "pre_paper_local_runtime_maps" in payload else None

def extract_runtime_component_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("runtime_component_items", [])

def extract_runtime_route_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("runtime_route_items", [])

def extract_dossier_candidate_id(payload: Dict[str, Any]) -> Optional[str]:
    dossiers = payload.get("paper_safe_dossiers", [])
    if dossiers:
        return dossiers[0].get("candidate_id")
    return None

def extract_dossier_decision(payload: Dict[str, Any]) -> Optional[str]:
    dossiers = payload.get("paper_safe_dossiers", [])
    if dossiers:
        return dossiers[0].get("decision")
    return None

def paper_safe_dossier_supports_non_execution_board(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    decision = extract_dossier_decision(payload)
    if decision not in ["CREATE_PAPER_SAFE_DOSSIER", "VALIDATED_PAPER_SAFE"]:
        warnings.append(f"Dossier decision '{decision}' is not optimal for non-execution board")

    seal = extract_non_execution_acceptance_seal(payload)
    if not seal:
        warnings.append("Missing non-execution acceptance seal")
    elif seal.get("status") == "FAILED" or not seal.get("passed", False):
        warnings.append("Non-execution acceptance seal is invalid or failed")

    rmap = extract_pre_paper_runtime_map(payload)
    if not rmap:
        warnings.append("Missing pre-paper runtime map")
    elif rmap.get("outcome") != "MAP_VERIFIED_SAFE":
        warnings.append("Runtime map outcome is not MAP_VERIFIED_SAFE")

    return len(warnings) == 0, warnings

def dossier_ingestion_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- DOSSIER INGESTION ---"]
    lines.append(f"Candidate: {extract_dossier_candidate_id(payload)}")
    lines.append(f"Decision: {extract_dossier_decision(payload)}")
    valid, warnings = paper_safe_dossier_supports_non_execution_board(payload)
    lines.append(f"Supports Board: {valid}")
    if warnings:
        lines.append("Warnings:")
        for w in warnings:
            lines.append(f"  - {w}")
    return "\n".join(lines)
