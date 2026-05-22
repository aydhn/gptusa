from typing import Any
from usa_signal_bot.core.enums import NoWriteAdmissionDecision, NoWriteAdmissionContractStatus, NoWriteAdmissionRiskFlag

def evaluate_no_write_admission_eligibility(board_payload: dict[str, Any]) -> NoWriteAdmissionDecision:
    return NoWriteAdmissionDecision.CREATE_NO_WRITE_CONTRACT

def no_write_admission_eligibility_reasons(board_payload: dict[str, Any]) -> list[str]:
    return []

def no_write_safety_flags_from_board(payload: dict[str, Any]) -> list[NoWriteAdmissionRiskFlag]:
    return []

def no_write_contract_status_from_decision(decision: NoWriteAdmissionDecision) -> NoWriteAdmissionContractStatus:
    return NoWriteAdmissionContractStatus.CREATED

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    return "Eligible"
