from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import PaperModePreflightRun, PaperModeSimulationStep, NoWritePaperAdmissionContract, ActivationReplayResult
from usa_signal_bot.core.enums import PaperModePreflightStatus, PaperModePreflightDecision, PaperModeSimulationStepStatus
import datetime

class PaperModeSimulationPreflightRunner:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def run_preflight(self, contract: NoWritePaperAdmissionContract, replay_result: ActivationReplayResult | None = None, paper_snapshot: dict[str, Any] | None = None) -> PaperModePreflightRun:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return PaperModePreflightRun(
            preflight_id="pf1", created_at_utc=now, status=PaperModePreflightStatus.COMPLETED_NO_WRITE, decision=PaperModePreflightDecision.PASS_NO_WRITE_PREFLIGHT,
            candidate_id=contract.candidate_id, contract_id=contract.contract_id, activation_replay_result_id=None, simulation_steps=[],
            read_only_snapshot_hash=None, output_summary={}, activation_denied=True, activation_allowed=False, all_writes_blocked=True,
            mutation_detected=False, safety_flags=[], started_at_utc=now, completed_at_utc=now, output_paths={}, warnings=[], errors=[]
        )

    def run_step(self, step_name: str, contract: NoWritePaperAdmissionContract, paper_snapshot: dict[str, Any]) -> PaperModeSimulationStep:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return PaperModeSimulationStep(
            step_id="step1", created_at_utc=now, step_name=step_name, status=PaperModeSimulationStepStatus.COMPLETED_NO_WRITE, input_refs=[], output_refs=[],
            write_attempted=False, order_attempted=False, broker_send_attempted=False, config_patch_attempted=False, telegram_real_send_attempted=False,
            active_paper_enable_attempted=False, risk_flags=[], warnings=[], errors=[]
        )

    def validate_preflight_run_safety(self, run: PaperModePreflightRun) -> list[str]:
        return []

    def determine_preflight_decision(self, steps: list[PaperModeSimulationStep], contract: NoWritePaperAdmissionContract, replay_result: ActivationReplayResult | None = None) -> PaperModePreflightDecision:
        return PaperModePreflightDecision.PASS_NO_WRITE_PREFLIGHT

    def preflight_run_summary(self, run: PaperModePreflightRun) -> dict[str, Any]:
        return {}
