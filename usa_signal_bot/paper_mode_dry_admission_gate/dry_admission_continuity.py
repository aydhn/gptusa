from typing import Any, List
from usa_signal_bot.core.enums import DryAdmissionGateRiskFlag
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle
)
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_validator import validate_final_dry_admission_gate_safety

def validate_dry_admission_continuity(
    gate: FinalPaperModeDryAdmissionGate | None = None,
    replay_result: ShadowLaunchReplayResult | None = None,
    freeze_bundle: BoardEvidenceFreezeBundle | None = None
) -> List[str]:
    errors = []

    if gate:
        errors.extend(validate_final_dry_admission_gate_safety(gate))

    if replay_result and not replay_result.passed:
        errors.append("Shadow replay did not pass")

    if freeze_bundle and freeze_bundle.missing_evidence_count > 0:
        errors.append("Evidence freeze is missing items")

    return errors

def dry_admission_continuity_flags(payload: dict[str, Any]) -> List[DryAdmissionGateRiskFlag]:
    # Placeholder for deriving flags based on continuity errors
    flags = []
    if not payload.get("is_preserved", False):
        flags.append(DryAdmissionGateRiskFlag.DRY_ADMISSION_GATE_INVALID)
    return flags

def dry_admission_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    return len(payload.get("errors", [])) == 0

def dry_admission_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "is_preserved": dry_admission_continuity_is_preserved(payload),
        "errors": payload.get("errors", [])
    }

def dry_admission_continuity_to_text(payload: dict[str, Any]) -> str:
    preserved = dry_admission_continuity_is_preserved(payload)
    return f"Dry Admission Continuity Preserved: {preserved}"
