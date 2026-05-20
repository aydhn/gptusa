from typing import Any, Dict, List
from usa_signal_bot.core.exceptions import ShadowValidationError

def ingest_sandbox_review_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    warnings = sandbox_ingestion_warnings(payload)
    return {
        "status": "ingested",
        "warnings": warnings,
        "context": extract_sandbox_context_payload(payload),
        "bundle_refs": extract_sandbox_bundle_refs(payload),
        "preview_outputs": extract_sandbox_preview_outputs(payload)
    }

def extract_sandbox_context_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("context", {})

def extract_sandbox_bundle_refs(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("bundle_refs", {})

def extract_sandbox_preview_outputs(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("preview_outputs", [])

def sandbox_ingestion_warnings(payload: Dict[str, Any]) -> List[str]:
    warnings = []
    if "context" not in payload:
        warnings.append("Missing sandbox context in payload.")
    if "unsafe_flags" in payload and payload["unsafe_flags"]:
        warnings.append("Sandbox payload contains unsafe flags.")
    return warnings

def sandbox_ingestion_to_text(payload: Dict[str, Any]) -> str:
    warnings = sandbox_ingestion_warnings(payload)
    return f"Sandbox Ingestion Payload (Warnings: {len(warnings)})"
