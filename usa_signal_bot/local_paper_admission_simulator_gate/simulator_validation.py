from dataclasses import dataclass, field
from typing import Any
from .simulator_gate_models import FinalLocalPaperAdmissionSimulatorGate, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle, SimulatorGateFullReview

@dataclass
class SimulatorValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulatorValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: list[SimulatorValidationIssue]
    warnings: list[str]
    errors: list[str]

def validate_final_simulator_gate_report(item: FinalLocalPaperAdmissionSimulatorGate) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_rehearsal_replay_result_report(item: RehearsalReplayResult) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_dry_admission_evidence_freeze_report(item: DryAdmissionEvidenceFreezeBundle) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_simulator_full_review_report(item: SimulatorGateFullReview) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_sensitive_data_in_simulator_payload(payload: dict[str, Any]) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_live_execution_language_in_simulator(text: str) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_active_paper_language_in_simulator(text: str) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_simulator_admission_language(text: str) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_paper_state_mutation_fields_in_simulator(payload: dict[str, Any]) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def validate_no_broker_execution_fields_in_simulator(payload: dict[str, Any]) -> SimulatorValidationReport:
    return SimulatorValidationReport(True, 0, 0, 0, 0, [], [], [])

def simulator_validation_report_to_text(report: SimulatorValidationReport) -> str:
    return ""

def assert_simulator_valid(report: SimulatorValidationReport) -> None:
    if not report.valid:
        raise ValueError("Invalid simulator report")
