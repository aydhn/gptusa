from typing import Any, Dict, List
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    PrePaperGovernanceCheckpoint
)
from usa_signal_bot.core.enums import FinalHandoffRiskFlag

def validate_handoff_non_execution(handoff_review: FinalHandoffReview) -> Dict[str, Any]:
    flags = collect_non_execution_risk_flags(handoff_review.__dict__)
    return {"valid": len(flags) == 0, "risk_flags": [f.value for f in flags]}

def validate_archive_non_execution(manifest: SealedReadinessArchiveManifest) -> Dict[str, Any]:
    flags = collect_non_execution_risk_flags(manifest.__dict__)
    return {"valid": len(flags) == 0, "risk_flags": [f.value for f in flags]}

def validate_checkpoint_non_execution(checkpoint: PrePaperGovernanceCheckpoint) -> Dict[str, Any]:
    flags = collect_non_execution_risk_flags(checkpoint.__dict__)
    return {"valid": len(flags) == 0, "risk_flags": [f.value for f in flags]}

def collect_non_execution_risk_flags(payload: Dict[str, Any]) -> List[FinalHandoffRiskFlag]:
    flags = []
    if payload.get("allows_active_paper", False):
        flags.append(FinalHandoffRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("allows_broker_execution", False):
        flags.append(FinalHandoffRiskFlag.BROKER_ORDER_RISK)
    if payload.get("allows_paper_state_mutation", False):
        flags.append(FinalHandoffRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_config_patch", False):
        flags.append(FinalHandoffRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    return flags

def non_execution_compliance_to_text(payload: Dict[str, Any]) -> str:
    return f"NonExecutionCompliance: valid={payload.get('valid')}, flags={payload.get('risk_flags')}"
