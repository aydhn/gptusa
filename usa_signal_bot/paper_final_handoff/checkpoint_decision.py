from typing import List
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    ArchiveIntegrityReport,
    PrePaperCheckpointGate,
    PrePaperGovernanceCheckpoint,
    create_pre_paper_checkpoint_id,
    _ts
)
from usa_signal_bot.core.enums import (
    PrePaperCheckpointDecision,
    PrePaperCheckpointStatus,
    PrePaperCheckpointGateStatus,
    FinalHandoffRiskFlag
)

class PrePaperCheckpointDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, handoff_review: FinalHandoffReview, manifest: SealedReadinessArchiveManifest, integrity_report: ArchiveIntegrityReport, gates: List[PrePaperCheckpointGate]) -> PrePaperGovernanceCheckpoint:
        flags = self.collect_checkpoint_risk_flags(handoff_review, manifest, integrity_report, gates)

        decision = PrePaperCheckpointDecision.PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL
        status = PrePaperCheckpointStatus.PASSED_FOR_GUARDED_PRE_PAPER_DRY_REHEARSAL

        if FinalHandoffRiskFlag.ARCHIVE_INTEGRITY_FAILED in flags:
            decision = PrePaperCheckpointDecision.REQUEST_ARCHIVE_REFRESH
            status = PrePaperCheckpointStatus.REQUEST_CHANGES
        elif FinalHandoffRiskFlag.MANUAL_REVIEW_MISSING in flags:
            decision = PrePaperCheckpointDecision.REQUEST_MANUAL_REVIEW
            status = PrePaperCheckpointStatus.REQUEST_CHANGES
        elif any(f in flags for f in [
            FinalHandoffRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
            FinalHandoffRiskFlag.BROKER_ORDER_RISK,
            FinalHandoffRiskFlag.PAPER_STATE_MUTATION_RISK,
            FinalHandoffRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            FinalHandoffRiskFlag.REAL_ORDER_RISK,
            FinalHandoffRiskFlag.TELEGRAM_REAL_SEND_RISK
        ]):
            decision = PrePaperCheckpointDecision.BLOCK
            status = PrePaperCheckpointStatus.BLOCKED

        return PrePaperGovernanceCheckpoint(
            checkpoint_id=create_pre_paper_checkpoint_id(),
            created_at_utc=_ts(),
            status=status,
            candidate_id=handoff_review.candidate_id,
            archive_id=manifest.archive_id,
            handoff_review_id=handoff_review.handoff_review_id,
            integrity_report_id=integrity_report.integrity_report_id,
            gates=gates,
            decision=decision,
            rationale=self.rationale_for_checkpoint_decision(decision, flags),
            required_followups=self.followups_for_checkpoint_decision(decision, flags),
            safety_flags=flags,
            manual_review_required=True,
            allows_active_paper=False,
            allows_broker_execution=False,
            allows_paper_state_mutation=False,
            allows_config_patch=False,
            warnings=[],
            errors=[]
        )

    def collect_checkpoint_risk_flags(self, handoff_review: FinalHandoffReview, manifest: SealedReadinessArchiveManifest, integrity_report: ArchiveIntegrityReport, gates: List[PrePaperCheckpointGate]) -> List[FinalHandoffRiskFlag]:
        flags = set(handoff_review.safety_flags + integrity_report.risk_flags)
        for g in gates:
            if g.status != PrePaperCheckpointGateStatus.PASS:
                for f in g.risk_flags:
                    flags.add(f)
        return list(flags)

    def rationale_for_checkpoint_decision(self, decision: PrePaperCheckpointDecision, flags: List[FinalHandoffRiskFlag]) -> str:
        if decision == PrePaperCheckpointDecision.PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL:
            return "All gates passed. Handed off to guarded dry rehearsal. Note: Not active paper enable."
        return f"Blocked or requested changes due to risk flags: {[f.value for f in flags]}"

    def followups_for_checkpoint_decision(self, decision: PrePaperCheckpointDecision, flags: List[FinalHandoffRiskFlag]) -> List[str]:
        if decision == PrePaperCheckpointDecision.PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL:
            return ["Proceed to guarded pre-paper dry rehearsal (Phase 81)."]
        return ["Address failed safety gates or integrity issues."]
