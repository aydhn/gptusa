"""Research Report Acceptance."""
from typing import Any

def extract_report_text_from_payload(payload: dict[str, Any]) -> str:
    return payload.get("text", "")

def validate_research_report_artifact(payload: dict[str, Any]) -> list[str]:
    errors = []
    if not research_report_has_required_sections(payload):
        errors.append("Missing required sections")
    if not research_report_has_safety_boundary(payload):
        errors.append("Missing safety boundary section")
    if not research_report_has_limitations(payload):
        errors.append("Missing limitations section")
    return errors

def research_report_has_required_sections(payload: dict[str, Any]) -> bool:
    text = extract_report_text_from_payload(payload).lower()
    sections = [
        "executive summary", "data scope", "factor validation summary",
        "factor drift summary", "factor diagnostics summary", "feature attribution summary",
        "factor interpretation summary", "lineage and quality summary",
        "limitations", "safety boundary"
    ]
    return all(s in text for s in sections)

def research_report_has_safety_boundary(payload: dict[str, Any]) -> bool:
    return "safety boundary" in extract_report_text_from_payload(payload).lower()

def research_report_has_limitations(payload: dict[str, Any]) -> bool:
    return "limitations" in extract_report_text_from_payload(payload).lower()

def research_report_acceptance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"valid": len(validate_research_report_artifact(payload)) == 0}

def research_report_acceptance_to_text(payload: dict[str, Any]) -> str:
    valid = len(validate_research_report_artifact(payload)) == 0
    return f"Research Report Valid: {valid}"
