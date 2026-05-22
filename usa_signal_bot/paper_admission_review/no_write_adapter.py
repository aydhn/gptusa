from typing import Any, Dict, List, Tuple
import json

def admission_evidence_from_no_write(payload: Dict[str, Any]) -> List[str]:
    return [payload.get("evidence_ref")] if payload.get("evidence_ref") else []

def no_write_supports_admission_review(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    return True, []

def attach_admission_hint_to_no_write_payload(payload: Dict[str, Any], report: Any) -> Dict[str, Any]:
    payload["admission_hint"] = "Admission review completed"
    return payload

def no_write_admission_review_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"admission_hint": payload.get("admission_hint")}

def no_write_adapter_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(no_write_admission_review_summary(payload), indent=2)
