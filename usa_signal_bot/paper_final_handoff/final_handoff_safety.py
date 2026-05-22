from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    PrePaperGovernanceCheckpoint
)
from usa_signal_bot.core.enums import FinalHandoffRiskFlag

def collect_final_handoff_safety_flags(handoff_review: Optional[FinalHandoffReview] = None, manifest: Optional[SealedReadinessArchiveManifest] = None, checkpoint: Optional[PrePaperGovernanceCheckpoint] = None) -> List[FinalHandoffRiskFlag]:
    flags = set()
    if handoff_review:
        flags.update(handoff_review.safety_flags)
        if handoff_review.allows_active_paper: flags.add(FinalHandoffRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if manifest:
        if manifest.allows_active_paper: flags.add(FinalHandoffRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if not manifest.sealed or not manifest.immutable: flags.add(FinalHandoffRiskFlag.ARCHIVE_INTEGRITY_FAILED)
    if checkpoint:
        flags.update(checkpoint.safety_flags)
        if checkpoint.allows_active_paper: flags.add(FinalHandoffRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    return list(flags)

def final_handoff_has_blocking_flags(flags: List[FinalHandoffRiskFlag]) -> bool:
    blocking = {
        FinalHandoffRiskFlag.REAL_ORDER_RISK,
        FinalHandoffRiskFlag.PAPER_ORDER_RISK,
        FinalHandoffRiskFlag.BROKER_ORDER_RISK,
        FinalHandoffRiskFlag.PAPER_STATE_MUTATION_RISK,
        FinalHandoffRiskFlag.TELEGRAM_REAL_SEND_RISK,
        FinalHandoffRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        FinalHandoffRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        FinalHandoffRiskFlag.ARCHIVE_AUTO_ENABLE_RISK,
        FinalHandoffRiskFlag.CHECKPOINT_AUTO_ENABLE_RISK,
        FinalHandoffRiskFlag.SECRET_RISK
    }
    return any(f in blocking for f in flags)

def validate_final_handoff_safety(handoff_review: Optional[FinalHandoffReview] = None, manifest: Optional[SealedReadinessArchiveManifest] = None, checkpoint: Optional[PrePaperGovernanceCheckpoint] = None) -> List[str]:
    flags = collect_final_handoff_safety_flags(handoff_review, manifest, checkpoint)
    errors = []
    if final_handoff_has_blocking_flags(flags):
        errors.append(f"Blocking safety flags found: {[f.value for f in flags]}")
    return errors

def final_handoff_safety_summary(flags: List[FinalHandoffRiskFlag]) -> Dict[str, Any]:
    return {"flags": [f.value for f in flags], "blocked": final_handoff_has_blocking_flags(flags)}

def final_handoff_safety_to_text(payload: Dict[str, Any]) -> str:
    return f"FinalHandoffSafety: blocked={payload.get('blocked')}, flags={payload.get('flags')}"
