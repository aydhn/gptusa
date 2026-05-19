from typing import Any
from usa_signal_bot.core.exceptions import ShadowValidationError

def ingest_sandbox_review_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if "context" not in payload and "sandbox_context" not in payload:
        payload["warnings"] = payload.get("warnings", []) + ["Missing sandbox context in payload"]
    return payload

def extract_sandbox_context_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("context", payload.get("sandbox_context", {}))

def extract_sandbox_bundle_refs(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_sandbox_id": payload.get("review_id", payload.get("sandbox_id")),
        "source_bundle_id": payload.get("bundle_id"),
        "source_bundle_version": payload.get("bundle_version")
    }

def extract_sandbox_preview_outputs(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("preview_outputs", payload.get("outputs", []))

def sandbox_ingestion_warnings(payload: dict[str, Any]) -> list[str]:
    warnings = []
    if "context" not in payload and "sandbox_context" not in payload:
        warnings.append("Missing sandbox context in payload")
    for flag in payload.get("safety_flags", []):
        if "UNSAFE" in str(flag) or "RISK" in str(flag):
            warnings.append(f"Unsafe flag detected in payload: {flag}")
    return warnings

def sandbox_ingestion_to_text(payload: dict[str, Any]) -> str:
    warnings = sandbox_ingestion_warnings(payload)
    refs = extract_sandbox_bundle_refs(payload)
    text = "Sandbox Ingestion Summary\n"
    text += f"Sandbox ID: {refs['source_sandbox_id']}\n"
    text += f"Bundle ID: {refs['source_bundle_id']}\n"
    if warnings:
        text += "Warnings:\n" + "\n".join(f"- {w}" for w in warnings) + "\n"
    text += "Note: Ingestion does not modify paper state."
    return text
