from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract, NoWriteContractClause
from usa_signal_bot.core.enums import NoWriteAdmissionContractStatus, NoWriteAdmissionDecision, NoWriteAdmissionRiskFlag
import datetime

def build_no_write_paper_admission_contract(board_payload: dict[str, Any]) -> NoWritePaperAdmissionContract:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return NoWritePaperAdmissionContract(
        contract_id="c1", created_at_utc=now, status=NoWriteAdmissionContractStatus.CREATED, decision=NoWriteAdmissionDecision.CREATE_NO_WRITE_CONTRACT,
        candidate_id="c1", source_board_review_id=None, source_write_block_proof_id=None, source_activation_firewall_event_refs=[],
        clauses=[], evidence_refs=[], manual_review_required=True, activation_denied=True, activation_allowed=False, all_writes_blocked=True,
        allows_active_paper=False, allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, safety_flags=[], warnings=[], errors=[]
    )

def build_default_no_write_contract(candidate_id: str | None = None) -> NoWritePaperAdmissionContract:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return NoWritePaperAdmissionContract(
        contract_id="c1", created_at_utc=now, status=NoWriteAdmissionContractStatus.CREATED, decision=NoWriteAdmissionDecision.CREATE_NO_WRITE_CONTRACT,
        candidate_id=candidate_id, source_board_review_id=None, source_write_block_proof_id=None, source_activation_firewall_event_refs=[],
        clauses=[], evidence_refs=[], manual_review_required=True, activation_denied=True, activation_allowed=False, all_writes_blocked=True,
        allows_active_paper=False, allows_broker_execution=False, allows_paper_state_mutation=False, allows_config_patch=False,
        allows_telegram_real_send=False, safety_flags=[], warnings=[], errors=[]
    )

def collect_contract_evidence_refs(board_payload: dict[str, Any]) -> list[str]:
    return []

def contract_safety_flags(board_payload: dict[str, Any], clauses: list[NoWriteContractClause]) -> list[NoWriteAdmissionRiskFlag]:
    return []

def no_write_contract_summary(contract: NoWritePaperAdmissionContract) -> dict[str, Any]:
    return {}

def no_write_contract_to_text(contract: NoWritePaperAdmissionContract) -> str:
    return "Contract"
