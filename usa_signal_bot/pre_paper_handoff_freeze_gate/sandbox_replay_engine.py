from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    SandboxRuntimeAdmissionReplayStatus,
    SandboxRuntimeAdmissionReplayOutcome,
    SandboxRuntimeAdmissionReplayDecision,
    PrePaperHandoffFreezeRiskFlag
)
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    SandboxRuntimeAdmissionReplayPlan,
    SandboxRuntimeAdmissionReplayResult,
    SandboxRuntimeAdmissionReplayItem,
    create_sandbox_replay_item_id,
    create_sandbox_replay_result_id
)

class SandboxRuntimeAdmissionBlockerReplayEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def replay(self, plan: SandboxRuntimeAdmissionReplayPlan, events: Optional[List[dict[str, Any]]] = None) -> SandboxRuntimeAdmissionReplayResult:
        result = SandboxRuntimeAdmissionReplayResult(
            replay_result_id=create_sandbox_replay_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            replay_plan_id=plan.replay_plan_id,
            status=SandboxRuntimeAdmissionReplayStatus.RUNNING,
            outcome=SandboxRuntimeAdmissionReplayOutcome.UNKNOWN,
            replayed_attempt_count=0,
            blocked_attempt_count=0,
            allowed_attempt_count=0,
            missing_event_count=0,
            passed=False,
            risk_flags=[],
            warnings=[],
            errors=[]
        )

        events = events or []
        items = []

        for event in events:
            item = self.replay_single_event(event)
            items.append(item)
            result.replayed_attempt_count += 1
            if item.blocked:
                result.blocked_attempt_count += 1
            else:
                result.allowed_attempt_count += 1

        result.errors.extend(self.validate_replay_coverage(plan, events))
        result.missing_event_count = len([e for e in plan.required_attempt_types if e not in [x.get("attempt_type") for x in events]])

        result.outcome = self.determine_replay_outcome(plan, items)
        result.passed = result.outcome == SandboxRuntimeAdmissionReplayOutcome.ALL_SANDBOX_RUNTIME_ADMISSION_ATTEMPTS_BLOCKED
        if result.passed:
            result.status = SandboxRuntimeAdmissionReplayStatus.COMPLETED_ALL_BLOCKED
        else:
            result.status = SandboxRuntimeAdmissionReplayStatus.FAILED

        result.risk_flags = self.collect_replay_risk_flags(plan, items)
        if not result.passed:
            result.risk_flags.append(PrePaperHandoffFreezeRiskFlag.SANDBOX_REPLAY_FAILED)

        return result

    def replay_single_event(self, event: dict[str, Any]) -> SandboxRuntimeAdmissionReplayItem:
        blocked = event.get("blocked", True)
        sra_allowed = event.get("sandbox_runtime_admission_allowed", False)
        psr_allowed = event.get("paper_sandbox_runtime_allowed", False)
        sa_allowed = event.get("simulator_admission_allowed", False)
        lps_allowed = event.get("local_paper_simulator_allowed", False)
        ad_allowed = event.get("admission_allowed", False)
        ap_enabled = event.get("active_paper_enabled", False)
        oc = event.get("order_created", False)
        psm = event.get("paper_state_mutated", False)
        bos = event.get("broker_order_sent", False)
        trs = event.get("telegram_real_sent", False)
        cp = event.get("config_patched", False)

        if sra_allowed or psr_allowed or sa_allowed or lps_allowed or ad_allowed or ap_enabled or oc or psm or bos or trs or cp:
            blocked = False

        decision = SandboxRuntimeAdmissionReplayDecision.BLOCK if blocked else SandboxRuntimeAdmissionReplayDecision.UNKNOWN

        return SandboxRuntimeAdmissionReplayItem(
            replay_item_id=create_sandbox_replay_item_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            attempt_type=event.get("attempt_type", "UNKNOWN"),
            source_event_id=event.get("event_id"),
            decision=decision,
            blocked=blocked,
            sandbox_runtime_admission_allowed=sra_allowed,
            paper_sandbox_runtime_allowed=psr_allowed,
            simulator_admission_allowed=sa_allowed,
            local_paper_simulator_allowed=lps_allowed,
            admission_allowed=ad_allowed,
            active_paper_enabled=ap_enabled,
            order_created=oc,
            paper_state_mutated=psm,
            broker_order_sent=bos,
            telegram_real_sent=trs,
            config_patched=cp,
            risk_flags=[],
            warnings=[],
            errors=[]
        )

    def validate_replay_coverage(self, plan: SandboxRuntimeAdmissionReplayPlan, events: List[dict[str, Any]]) -> List[str]:
        errors = []
        attempt_types = [e.get("attempt_type") for e in events]
        for req in plan.required_attempt_types:
            if req not in attempt_types:
                errors.append(f"Missing required attempt type: {req}")
        return errors

    def determine_replay_outcome(self, plan: SandboxRuntimeAdmissionReplayPlan, replay_items: List[SandboxRuntimeAdmissionReplayItem]) -> SandboxRuntimeAdmissionReplayOutcome:
        for item in replay_items:
            if not item.blocked:
                return SandboxRuntimeAdmissionReplayOutcome.SANDBOX_RUNTIME_ADMISSION_ATTEMPT_ALLOWED

        attempt_types = [item.attempt_type for item in replay_items]
        for req in plan.required_attempt_types:
            if req not in attempt_types:
                return SandboxRuntimeAdmissionReplayOutcome.BLOCKER_EVENTS_MISSING

        return SandboxRuntimeAdmissionReplayOutcome.ALL_SANDBOX_RUNTIME_ADMISSION_ATTEMPTS_BLOCKED

    def collect_replay_risk_flags(self, plan: SandboxRuntimeAdmissionReplayPlan, replay_items: List[SandboxRuntimeAdmissionReplayItem]) -> List[PrePaperHandoffFreezeRiskFlag]:
        flags = []
        for item in replay_items:
            if not item.blocked:
                flags.append(PrePaperHandoffFreezeRiskFlag.SANDBOX_RUNTIME_ADMISSION_ATTEMPT_NOT_BLOCKED)
            if item.sandbox_runtime_admission_allowed:
                flags.append(PrePaperHandoffFreezeRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK)
            if item.paper_sandbox_runtime_allowed:
                flags.append(PrePaperHandoffFreezeRiskFlag.PAPER_SANDBOX_RUNTIME_RISK)
            if item.simulator_admission_allowed:
                flags.append(PrePaperHandoffFreezeRiskFlag.SIMULATED_ADMISSION_RISK)
            if item.local_paper_simulator_allowed:
                flags.append(PrePaperHandoffFreezeRiskFlag.LOCAL_PAPER_SIMULATOR_RISK)
            if item.admission_allowed:
                flags.append(PrePaperHandoffFreezeRiskFlag.ADMISSION_ALLOWED_RISK)
            if item.active_paper_enabled:
                flags.append(PrePaperHandoffFreezeRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
            if item.order_created:
                flags.append(PrePaperHandoffFreezeRiskFlag.ORDER_CREATED_RISK)
            if item.paper_state_mutated:
                flags.append(PrePaperHandoffFreezeRiskFlag.PAPER_STATE_MUTATION_RISK)
            if item.broker_order_sent:
                flags.append(PrePaperHandoffFreezeRiskFlag.BROKER_ORDER_RISK)
            if item.telegram_real_sent:
                flags.append(PrePaperHandoffFreezeRiskFlag.TELEGRAM_REAL_SEND_RISK)
            if item.config_patched:
                flags.append(PrePaperHandoffFreezeRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        return list(set(flags))

    def replay_summary(self, result: SandboxRuntimeAdmissionReplayResult) -> dict[str, Any]:
        return {
            "passed": result.passed,
            "outcome": result.outcome.value,
            "blocked": result.blocked_attempt_count,
            "allowed": result.allowed_attempt_count
        }
