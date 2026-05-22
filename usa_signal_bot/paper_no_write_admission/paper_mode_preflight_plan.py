from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract, ActivationReplayResult

def build_paper_mode_preflight_plan(contract: NoWritePaperAdmissionContract, replay_result: ActivationReplayResult | None = None) -> dict[str, Any]:
    return {"steps": default_paper_mode_simulation_steps()}

def default_paper_mode_simulation_steps() -> list[str]:
    return ["read_only_snapshot_load", "candidate_metadata_load", "signal_pipeline_dry_preview", "risk_pipeline_dry_preview", "notification_dry_preview", "write_lock_assertion", "activation_firewall_replay_reference", "no_write_summary"]

def required_preflight_inputs() -> list[str]:
    return []

def required_preflight_outputs() -> list[str]:
    return []

def validate_preflight_plan_no_write(payload: dict[str, Any]) -> list[str]:
    return []

def paper_mode_preflight_plan_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def paper_mode_preflight_plan_to_text(payload: dict[str, Any]) -> str:
    return "Preflight Plan"
