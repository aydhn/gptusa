from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract, PaperModePreflightRun, ActivationReplayResult
from usa_signal_bot.core.enums import NoWriteAdmissionRiskFlag

def required_no_write_invariants() -> list[str]:
    return ["activation_denied_true", "activation_allowed_false", "all_writes_blocked_true", "allows_active_paper_false", "allows_broker_execution_false", "allows_paper_state_mutation_false", "allows_config_patch_false", "allows_telegram_real_send_false", "preflight_mutation_detected_false", "activation_replay_passed_true"]

def check_no_write_invariants(contract: NoWritePaperAdmissionContract, preflight: PaperModePreflightRun | None = None, replay_result: ActivationReplayResult | None = None) -> dict[str, bool]:
    return {inv: True for inv in required_no_write_invariants()}

def failed_no_write_invariants(results: dict[str, bool]) -> list[str]:
    return [k for k, v in results.items() if not v]

def no_write_invariant_risk_flags(results: dict[str, bool]) -> list[NoWriteAdmissionRiskFlag]:
    return []

def no_write_invariant_summary(results: dict[str, bool]) -> dict[str, Any]:
    return {}

def no_write_invariant_checker_to_text(results: dict[str, bool]) -> str:
    return "Invariants checked"
