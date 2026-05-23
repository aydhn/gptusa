from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import PaperSandboxBoundaryCertificate, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle
from usa_signal_bot.core.enums import PaperSandboxBoundaryRiskFlag

def collect_boundary_safety_flags(certificate: PaperSandboxBoundaryCertificate | None = None, replay_result: AdmissionBlockerReplayResult | None = None, freeze_bundle: NoOrderEvidenceFreezeBundle | None = None) -> list[PaperSandboxBoundaryRiskFlag]:
    flags = []
    if certificate:
        if certificate.allows_active_paper: flags.append(PaperSandboxBoundaryRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if certificate.allows_broker_execution: flags.append(PaperSandboxBoundaryRiskFlag.BROKER_ORDER_RISK)
        if certificate.allows_paper_state_mutation: flags.append(PaperSandboxBoundaryRiskFlag.PAPER_STATE_MUTATION_RISK)
        if certificate.allows_config_patch: flags.append(PaperSandboxBoundaryRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if certificate.allows_telegram_real_send: flags.append(PaperSandboxBoundaryRiskFlag.TELEGRAM_REAL_SEND_RISK)
        if certificate.admission_allowed: flags.append(PaperSandboxBoundaryRiskFlag.ADMISSION_ALLOWED_RISK)
    return flags

def boundary_has_blocking_flags(flags: list[PaperSandboxBoundaryRiskFlag]) -> bool:
    return len(flags) > 0

def validate_boundary_safety(certificate: PaperSandboxBoundaryCertificate | None = None, replay_result: AdmissionBlockerReplayResult | None = None, freeze_bundle: NoOrderEvidenceFreezeBundle | None = None) -> list[str]:
    flags = collect_boundary_safety_flags(certificate, replay_result, freeze_bundle)
    return [f.value for f in flags]

def boundary_safety_summary(flags: list[PaperSandboxBoundaryRiskFlag]) -> dict[str, Any]:
    return {"safe": not boundary_has_blocking_flags(flags), "flags": [f.value for f in flags]}

def boundary_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
