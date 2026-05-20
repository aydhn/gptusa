from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ShadowComparisonRole

def extract_shadow_session_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("session_id") or payload.get("id")

def extract_shadow_session_role(payload: Dict[str, Any]) -> ShadowComparisonRole:
    role_str = payload.get("metadata", {}).get("role", "UNKNOWN")
    try:
        return ShadowComparisonRole(role_str)
    except ValueError:
        return ShadowComparisonRole.UNKNOWN

def extract_shadow_session_safety_flags(payload: Dict[str, Any]) -> List[str]:
    return payload.get("safety_flags", [])

def shadow_session_ingestion_warnings(payload: Dict[str, Any]) -> List[str]:
    warnings = []
    if not extract_shadow_session_id(payload):
        warnings.append("Missing session_id in payload.")
    flags = extract_shadow_session_safety_flags(payload)
    if "REAL_ORDER_RISK" in flags or "PAPER_MUTATION_RISK" in flags:
        warnings.append("Critical safety risk flag detected in ingestion.")
    return warnings

def ingest_shadow_session_payload(payload: Dict[str, Any], role: ShadowComparisonRole = ShadowComparisonRole.UNKNOWN) -> Dict[str, Any]:
    cleaned = payload.copy()
    if "metadata" not in cleaned:
        cleaned["metadata"] = {}
    cleaned["metadata"]["ingested_role"] = role.value
    cleaned["ingestion_warnings"] = shadow_session_ingestion_warnings(cleaned)
    return cleaned

def ingest_shadow_sessions(baseline_payload: Optional[Dict[str, Any]], candidate_payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    res = {}
    if baseline_payload:
        res["baseline"] = ingest_shadow_session_payload(baseline_payload, ShadowComparisonRole.BASELINE)
    else:
        res["baseline"] = None
    if candidate_payload:
        res["candidate"] = ingest_shadow_session_payload(candidate_payload, ShadowComparisonRole.CANDIDATE)
    else:
        res["candidate"] = None
    return res

def shadow_session_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return f"Shadow Ingestion [Role: {payload.get('metadata', {}).get('ingested_role')}] - ID: {extract_shadow_session_id(payload)}"
