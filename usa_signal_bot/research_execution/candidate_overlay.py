from typing import Any
import copy

from usa_signal_bot.core.exceptions import CandidateOverlayError

def build_candidate_overlay_from_parameter_proposals(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    overlay = {}
    for prop in proposals:
        target = prop.get("target_parameter", "")
        if not target:
            continue

        parts = target.split(".")
        current = overlay
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = prop.get("proposed_value")
    return overlay

def apply_candidate_overlay_to_config(config_payload: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    warnings = validate_candidate_overlay_safe(overlay)
    if warnings:
        raise CandidateOverlayError(f"Overlay safety validation failed: {warnings}")

    result = copy.deepcopy(config_payload)
    def merge(a: dict, b: dict) -> dict:
        for key, val in b.items():
            if key in a and isinstance(a[key], dict) and isinstance(val, dict):
                merge(a[key], val)
            else:
                a[key] = val
        return a

    return merge(result, overlay)

def validate_candidate_overlay_safe(overlay: dict[str, Any]) -> list[str]:
    warnings = []

    def count_keys(d: dict) -> int:
        c = 0
        for k, v in d.items():
            c += 1
            if isinstance(v, dict):
                c += count_keys(v)
        return c

    if count_keys(overlay) > 50:
        warnings.append("Overlay exceeds max allowed keys (50).")

    def check_recursive(d: dict):
        for k, v in d.items():
            kl = k.lower()
            if any(bf in kl for bf in ["broker", "order", "live", "demo_account"]):
                warnings.append(f"BLOCKED: Broker/order field detected in overlay: {k}")
            if any(af in kl for af in ["auto_apply", "auto_execution"]):
                warnings.append(f"BLOCKED: Auto-apply field detected in overlay: {k}")

            if isinstance(v, dict):
                check_recursive(v)

    check_recursive(overlay)
    warnings.extend(reject_overlay_if_auto_apply_requested(overlay))

    return warnings

def reject_overlay_if_auto_apply_requested(overlay: dict[str, Any]) -> list[str]:
    warnings = []
    if overlay.get("auto_apply", False) or overlay.get("auto_execution", False):
        warnings.append("BLOCKED: auto_apply or auto_execution requested in candidate overlay. This is strictly a local analytics framework.")
    return warnings

def candidate_overlay_to_text(overlay: dict[str, Any]) -> str:
    lines = ["--- CANDIDATE OVERLAY ---"]
    import json
    lines.append(json.dumps(overlay, indent=2))
    lines.append("NOTE: This overlay is an in-memory test patch. It does NOT mutate production configuration.")
    return "\n".join(lines)
