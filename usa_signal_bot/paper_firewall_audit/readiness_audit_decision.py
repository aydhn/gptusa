from typing import List
from datetime import datetime, timezone
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import (
    FirewallReplayResult, ZeroMutationAuditReport, PrePaperReadinessEvidenceRefresh,
    ReadinessAuditCheckpoint, create_readiness_audit_checkpoint_id
)
from usa_signal_bot.core.enums import (
    ReadinessAuditCheckpointStatus, ReadinessAuditDecision, FirewallAuditRiskFlag, FirewallReplayStatus
)

class PrePaperReadinessAuditDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, replay_result: FirewallReplayResult, zero_mutation_audit: ZeroMutationAuditReport, evidence_refresh: PrePaperReadinessEvidenceRefresh) -> ReadinessAuditCheckpoint:
        flags = self.collect_readiness_audit_risk_flags(replay_result, zero_mutation_audit, evidence_refresh)

        decision = ReadinessAuditDecision.CONTINUE_WITH_ACTIVATION_DENIED_AUDIT
        if FirewallAuditRiskFlag.FIREWALL_REPLAY_FAILED in flags: decision = ReadinessAuditDecision.REQUEST_FIREWALL_REPLAY
        elif FirewallAuditRiskFlag.ZERO_MUTATION_FAILED in flags: decision = ReadinessAuditDecision.REQUEST_ZERO_MUTATION_AUDIT_REFRESH
        elif FirewallAuditRiskFlag.EVIDENCE_MISSING in flags or FirewallAuditRiskFlag.EVIDENCE_STALE in flags: decision = ReadinessAuditDecision.REQUEST_EVIDENCE_REFRESH
        elif len(flags) > 0: decision = ReadinessAuditDecision.BLOCK

        status = ReadinessAuditCheckpointStatus.AUDIT_PASSED_ACTIVATION_DENIED if decision == ReadinessAuditDecision.CONTINUE_WITH_ACTIVATION_DENIED_AUDIT else ReadinessAuditCheckpointStatus.BLOCKED

        return ReadinessAuditCheckpoint(
            checkpoint_id=create_readiness_audit_checkpoint_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            candidate_id=zero_mutation_audit.candidate_id,
            status=status,
            decision=decision,
            firewall_replay_result_id=replay_result.replay_result_id,
            zero_mutation_audit_id=zero_mutation_audit.audit_id,
            evidence_refresh_id=evidence_refresh.refresh_id,
            activation_denied=True,
            activation_allowed=False,
            required_followups=self.followups_for_readiness_audit_decision(decision, flags),
            risk_flags=flags,
            allows_active_paper=False,
            allows_broker_execution=False,
            allows_paper_state_mutation=False,
            allows_config_patch=False,
            allows_telegram_real_send=False,
            warnings=[],
            errors=[]
        )

    def collect_readiness_audit_risk_flags(self, replay_result: FirewallReplayResult, zero_mutation_audit: ZeroMutationAuditReport, evidence_refresh: PrePaperReadinessEvidenceRefresh) -> List[FirewallAuditRiskFlag]:
        flags = []
        flags.extend(replay_result.risk_flags)
        flags.extend(zero_mutation_audit.risk_flags)

        if not replay_result.passed or replay_result.status == FirewallReplayStatus.FAILED:
            flags.append(FirewallAuditRiskFlag.FIREWALL_REPLAY_FAILED)
        if not zero_mutation_audit.passed:
            flags.append(FirewallAuditRiskFlag.ZERO_MUTATION_FAILED)
        if evidence_refresh.missing_count > 0:
            flags.append(FirewallAuditRiskFlag.EVIDENCE_MISSING)
        if evidence_refresh.stale_count > 0:
            flags.append(FirewallAuditRiskFlag.EVIDENCE_STALE)

        return list(set(flags))

    def rationale_for_readiness_audit_decision(self, decision: ReadinessAuditDecision, flags: List[FirewallAuditRiskFlag]) -> str:
        if decision == ReadinessAuditDecision.CONTINUE_WITH_ACTIVATION_DENIED_AUDIT:
            return "Replay and zero mutation passed. Evidence is fresh. Proceeding with safety."
        return f"Blocked due to flags: {[f.value for f in flags]}"

    def followups_for_readiness_audit_decision(self, decision: ReadinessAuditDecision, flags: List[FirewallAuditRiskFlag]) -> List[str]:
        f = []
        if decision != ReadinessAuditDecision.CONTINUE_WITH_ACTIVATION_DENIED_AUDIT:
            f.append("Resolve risk flags before proceeding")
        return f
