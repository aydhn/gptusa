from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract

def validate_contract_no_write_clauses(contract: NoWritePaperAdmissionContract) -> list[str]:
    return []

def validate_contract_activation_denied(contract: NoWritePaperAdmissionContract) -> list[str]:
    return []

def validate_contract_no_execution_permissions(contract: NoWritePaperAdmissionContract) -> list[str]:
    return []

def contract_allows_activation(contract: NoWritePaperAdmissionContract) -> bool:
    return contract.activation_allowed

def contract_requires_followup(contract: NoWritePaperAdmissionContract) -> bool:
    return False

def contract_validator_summary(contract: NoWritePaperAdmissionContract) -> dict[str, Any]:
    return {}

def contract_validator_to_text(payload: dict[str, Any]) -> str:
    return "Validator"
