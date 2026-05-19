from typing import Any, Dict, List

def extract_candidate_overlay_from_bundle(bundle_payload: Dict[str, Any]) -> Dict[str, Any]:
    return bundle_payload.get("overlay", {})

def build_in_memory_candidate_config(bundle_payload: Dict[str, Any]) -> Dict[str, Any]:
    return extract_candidate_overlay_from_bundle(bundle_payload)

def validate_overlay_does_not_patch_files(overlay: Dict[str, Any]) -> List[str]:
    warnings = []
    # If the overlay includes a file patch or direct override instruction:
    if overlay.get("patch_files") or overlay.get("override_production_config"):
        warnings.append("Overlay attempts to patch files. Blocked in sandbox.")
    return warnings

def validate_overlay_has_no_broker_live_fields(overlay: Dict[str, Any]) -> List[str]:
    warnings = []
    bad_fields = ["live_enabled", "demo_enabled", "order_routing_enabled", "auto_apply"]
    for field in bad_fields:
        if overlay.get(field) is True:
            warnings.append(f"Overlay contains risky broker field '{field}' set to True.")
    return warnings

def overlay_resolver_summary(overlay: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "keys_count": len(overlay.keys()),
        "has_live_enabled": overlay.get("live_enabled", False)
    }

def overlay_resolver_to_text(payload: Dict[str, Any]) -> str:
    summary = overlay_resolver_summary(payload)
    return f"Overlay Resolved: {summary['keys_count']} keys configured."
