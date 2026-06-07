from typing import Any

def deduplicate_closure_warnings(warnings: list[str]) -> list[str]:
    return list(dict.fromkeys(warnings))

def collect_closure_warnings(payloads: dict[str, dict[str, Any]], audits: dict[str, Any]) -> list[str]:
    warnings = []

    # Collect warnings from audits
    for name, audit in audits.items():
        if hasattr(audit, 'warnings') and audit.warnings:
            warnings.extend(audit.warnings)

    return deduplicate_closure_warnings(warnings)

def closure_warnings_summary(warnings: list[str]) -> dict[str, Any]:
    return {"count": len(warnings)}

def closure_warnings_to_text(warnings: list[str], limit: int = 300) -> str:
    return f"Closure Warnings: {len(warnings)}"
