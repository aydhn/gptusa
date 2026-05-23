from typing import Any, Dict, List, Optional, Tuple
from usa_signal_bot.core.enums import PaperSafeGateReportType

def ingest_paper_safe_gate_full_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    if payload.get("report_type") != PaperSafeGateReportType.FINAL_PAPER_SAFE_GATE_REPORT.value:
        payload["warnings"] = payload.get("warnings", []) + ["Payload is not a valid PAPER_SAFE_GATE_REPORT."]
    return payload

def extract_final_paper_safe_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    gates = payload.get("gates", [])
    if gates:
        return gates[-1]
    return None

def extract_boundary_replay_result(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    results = payload.get("replay_results", [])
    if results:
        return results[-1]
    return None

def extract_frozen_evidence_integrity_audit(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    audits = payload.get("integrity_audits", [])
    if audits:
        return audits[-1]
    return None

def extract_paper_safe_rules(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("rules", [])

def extract_paper_safe_assertions(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("assertions", [])

def extract_paper_safe_candidate_id(payload: Dict[str, Any]) -> Optional[str]:
    gate = extract_final_paper_safe_gate(payload)
    if gate:
         return gate.get("candidate_id")
    return None

def extract_paper_safe_decision(payload: Dict[str, Any]) -> Optional[str]:
    gate = extract_final_paper_safe_gate(payload)
    if gate:
        return gate.get("decision")
    return None

def paper_safe_gate_supports_dossier(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    gate = extract_final_paper_safe_gate(payload)
    if not gate:
        reasons.append("Missing final paper-safe gate.")
        return False, reasons

    if gate.get("status") == "FAILED" or gate.get("status") == "BLOCKED":
        reasons.append("Final paper-safe gate is failed or blocked.")
        return False, reasons

    audit = extract_frozen_evidence_integrity_audit(payload)
    if audit and audit.get("tamper_count", 0) > 0:
        reasons.append("Frozen evidence tamper detected.")
        return False, reasons

    return True, reasons

def paper_safe_ingestion_to_text(payload: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"Ingested Review ID: {payload.get('review_id', 'Unknown')}")
    gate = extract_final_paper_safe_gate(payload)
    if gate:
        lines.append(f"Gate Status: {gate.get('status')}")
        lines.append(f"Decision: {gate.get('decision')}")
    else:
        lines.append("Gate: Missing")

    return "\n".join(lines)
