from typing import Any

def reason_for_low_compatibility(result: dict[str, Any]) -> list[str]:
    reasons = []
    if result.get("score", 100) < 40:
        reasons.append("compatibility_score_below_40")
    if result.get("data_quality_limited"):
        reasons.append("data_quality_limited")
    if not reasons:
        reasons.append("unexplained_low_score")
    return reasons

def reason_for_uncertain_compatibility(result: dict[str, Any]) -> list[str]:
    return ["uncertain_classification"]

def reason_for_conflicted_context(result: dict[str, Any]) -> list[str]:
    return ["conflicted_classification"]

def reason_for_data_quality_limited_context(result: dict[str, Any]) -> list[str]:
    return ["data_quality_flag_set"]

def map_low_compatibility_reasons(compatibility_results: list[dict[str, Any]], diagnostics_profiles: list[dict[str, Any]]) -> dict[str, list[str]]:
    mapper = {}
    for c in compatibility_results:
        cid = c.get("compatibility_id", "unknown")
        score = c.get("score", 100)
        cls = c.get("classification", "").lower()
        if score < 40 or "low" in cls:
            mapper[cid] = reason_for_low_compatibility(c)
    return mapper

def validate_low_compatibility_reasons(reason_map: dict[str, list[str]]) -> list[str]:
    errors = []
    for cid, reasons in reason_map.items():
        if "unexplained_low_score" in reasons:
            errors.append(f"Unexplained low score for {cid}")
    return errors

def low_compatibility_reason_mapper_summary(reason_map: dict[str, list[str]]) -> dict[str, Any]:
    return {"mapped_contexts": len(reason_map)}

def low_compatibility_reason_mapper_to_text(reason_map: dict[str, list[str]], limit: int = 300) -> str:
    return f"Mapped reasons for {len(reason_map)} low compatibility contexts."
