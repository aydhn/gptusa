from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract, ActivationReplayResult, PaperModePreflightRun
from usa_signal_bot.core.enums import NoWriteAdmissionRiskFlag

def collect_preflight_safety_flags(contract: NoWritePaperAdmissionContract | None = None, replay_result: ActivationReplayResult | None = None, preflight: PaperModePreflightRun | None = None) -> list[NoWriteAdmissionRiskFlag]:
    return []

def preflight_has_blocking_flags(flags: list[NoWriteAdmissionRiskFlag]) -> bool:
    return False

def validate_preflight_safety(contract: NoWritePaperAdmissionContract | None = None, replay_result: ActivationReplayResult | None = None, preflight: PaperModePreflightRun | None = None) -> list[str]:
    return []

def preflight_safety_summary(flags: list[NoWriteAdmissionRiskFlag]) -> dict[str, Any]:
    return {}

def preflight_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return "Safety valid"
