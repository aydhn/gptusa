from typing import Any, List
from usa_signal_bot.core.enums import DryAdmissionGateRiskFlag
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle
)

def collect_dry_admission_safety_flags(
    gate: FinalPaperModeDryAdmissionGate | None = None,
    replay_result: ShadowLaunchReplayResult | None = None,
    freeze_bundle: BoardEvidenceFreezeBundle | None = None
) -> List[DryAdmissionGateRiskFlag]:
    flags = []
    if gate:
        flags.extend(gate.safety_flags)
    if replay_result:
        flags.extend(replay_result.risk_flags)
    if freeze_bundle:
        flags.extend(freeze_bundle.risk_flags)
    return list(set(flags))

def dry_admission_has_blocking_flags(flags: List[DryAdmissionGateRiskFlag]) -> bool:
    blocking_flags = [
        DryAdmissionGateRiskFlag.REAL_ORDER_RISK,
        DryAdmissionGateRiskFlag.PAPER_ORDER_RISK,
        DryAdmissionGateRiskFlag.BROKER_ORDER_RISK,
        DryAdmissionGateRiskFlag.PAPER_STATE_MUTATION_RISK,
        DryAdmissionGateRiskFlag.TELEGRAM_REAL_SEND_RISK,
        DryAdmissionGateRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        DryAdmissionGateRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        DryAdmissionGateRiskFlag.SHADOW_LAUNCH_RISK,
        DryAdmissionGateRiskFlag.PAPER_MODE_LAUNCH_RISK,
        DryAdmissionGateRiskFlag.ADMISSION_ALLOWED_RISK,
        DryAdmissionGateRiskFlag.ACTIVATION_ALLOWED_RISK,
        DryAdmissionGateRiskFlag.TRANSITION_ALLOWED_RISK,
        DryAdmissionGateRiskFlag.ORDER_CREATED_RISK,
        DryAdmissionGateRiskFlag.MUTATION_DETECTED_RISK,
        DryAdmissionGateRiskFlag.SHADOW_REPLAY_FAILED,
        DryAdmissionGateRiskFlag.BOARD_EVIDENCE_FREEZE_FAILED,
        DryAdmissionGateRiskFlag.DRY_ADMISSION_ASSERTION_FAILED,
        DryAdmissionGateRiskFlag.SECRET_RISK
    ]
    return any(f in blocking_flags for f in flags)

def validate_dry_admission_safety(
    gate: FinalPaperModeDryAdmissionGate | None = None,
    replay_result: ShadowLaunchReplayResult | None = None,
    freeze_bundle: BoardEvidenceFreezeBundle | None = None
) -> List[str]:
    flags = collect_dry_admission_safety_flags(gate, replay_result, freeze_bundle)
    if dry_admission_has_blocking_flags(flags):
        return ["Blocking safety flags present"]
    return []

def dry_admission_safety_summary(flags: List[DryAdmissionGateRiskFlag]) -> dict[str, Any]:
    return {
        "flags_count": len(flags),
        "has_blocking": dry_admission_has_blocking_flags(flags)
    }

def dry_admission_safety_validator_to_text(payload: dict[str, Any]) -> str:
    safe = not payload.get("has_blocking", True)
    return f"Dry Admission Safety - Safe: {safe}"
