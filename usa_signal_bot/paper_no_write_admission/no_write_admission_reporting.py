from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import (
    NoWriteContractClause, NoWritePaperAdmissionContract, ActivationReplayPlan,
    ActivationReplayResult, PaperModeSimulationStep, PaperModePreflightRun,
    NoWriteAdmissionAuditEntry, NoWriteAdmissionFullReview
)

def no_write_contract_clause_to_text(item: NoWriteContractClause) -> str:
    return "Clause"

def no_write_paper_admission_contract_to_text(item: NoWritePaperAdmissionContract, limit: int = 100) -> str:
    return "Contract"

def activation_replay_plan_to_text(item: ActivationReplayPlan) -> str:
    return "Replay Plan"

def activation_replay_result_to_text(item: ActivationReplayResult) -> str:
    return "Replay Result"

def paper_mode_simulation_step_to_text(item: PaperModeSimulationStep) -> str:
    return "Step"

def paper_mode_preflight_run_to_text(item: PaperModePreflightRun, limit: int = 100) -> str:
    return "Preflight Run"

def no_write_admission_audit_entry_to_text(item: NoWriteAdmissionAuditEntry) -> str:
    return "Audit Entry"

def no_write_admission_full_review_to_text(item: NoWriteAdmissionFullReview, limit: int = 100) -> str:
    return "Full Review"

def no_write_admission_store_summary_to_text(summary: dict[str, Any]) -> str:
    return "Store Summary"

def no_write_admission_limitations_text() -> str:
    return "Limitations: No write admission contract is not active paper admission."
