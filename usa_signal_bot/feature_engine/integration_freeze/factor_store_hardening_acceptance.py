"""Factor Store Hardening Acceptance."""
from typing import Any

def extract_factor_store_hardening_result(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("factor_store_hardening")

def validate_factor_store_hardening_acceptance(payload: dict[str, Any]) -> list[str]:
    errors = []
    hardening = extract_factor_store_hardening_result(payload) or {}

    if not hardening.get("factor_store_hardened", False):
        errors.append("factor_store_hardened must be True")
    if not hardening.get("no_secret_leak", False):
         errors.append("no_secret_leak must be True")
    if not hardening.get("no_forbidden_columns", False):
         errors.append("no_forbidden_columns must be True")
    if not hardening.get("no_execution_language", False):
         errors.append("no_execution_language must be True")
    if not hardening.get("immutable_artifacts", False):
         errors.append("immutable_artifacts must be True")
    if not hardening.get("overwrite_safe", False):
         errors.append("overwrite_safe must be True")
    if not hardening.get("research_data_only", False):
         errors.append("research_data_only must be True")

    return errors

def factor_store_hardening_accepted(payload: dict[str, Any]) -> bool:
    return len(validate_factor_store_hardening_acceptance(payload)) == 0

def factor_store_hardening_acceptance_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"accepted": factor_store_hardening_accepted(payload)}

def factor_store_hardening_acceptance_to_text(payload: dict[str, Any]) -> str:
    return f"Factor Store Hardening Accepted: {factor_store_hardening_accepted(payload)}"
