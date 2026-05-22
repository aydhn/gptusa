from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionPlan,
    PaperModeDryAdmissionRun,
    DryAdmissionStep,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    create_dry_admission_run_id,
    create_dry_admission_step_id
)
from usa_signal_bot.core.enums import (
    PaperModeDryAdmissionStatus,
    PaperModeDryAdmissionDecision,
    DryAdmissionStepStatus,
    DryAdmissionRiskFlag
)
from usa_signal_bot.paper_dry_admission.no_write_ingestion import extract_no_write_candidate_id
from usa_signal_bot.paper_dry_admission.write_lock_proof_refresh import refresh_runtime_write_lock_proof
from usa_signal_bot.paper_dry_admission.human_approval_ledger import build_default_human_approval_ledger

class PaperModeDryAdmissionRunner:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def run_dry_admission(
        self,
        plan: PaperModeDryAdmissionPlan,
        no_write_payload: dict[str, Any] | None = None,
        paper_snapshot: dict[str, Any] | None = None
    ) -> PaperModeDryAdmissionRun:

        run = PaperModeDryAdmissionRun(
            run_id=create_dry_admission_run_id(),
            status=PaperModeDryAdmissionStatus.RUNNING,
            plan=plan,
            candidate_id=plan.candidate_id,
            started_at_utc=datetime.now(timezone.utc).isoformat()
        )

        refresh = None
        ledger = None

        if plan.require_write_lock_refresh:
            refresh = self.build_write_lock_refresh_for_run(no_write_payload, paper_snapshot)
            run.write_lock_refresh = refresh

        if plan.require_human_ledger:
            ledger = self.build_human_ledger_for_run(plan.candidate_id)
            run.human_ledger = ledger

        for step_name in plan.planned_steps:
            step = self.run_step(step_name, plan, paper_snapshot or {})
            run.steps.append(step)

        run.decision = self.determine_run_decision(run.steps, refresh, ledger)
        if run.decision in [PaperModeDryAdmissionDecision.REJECT, PaperModeDryAdmissionDecision.BLOCK]:
            run.status = PaperModeDryAdmissionStatus.BLOCKED
        elif run.decision == PaperModeDryAdmissionDecision.REQUEST_MANUAL_REVIEW:
            run.status = PaperModeDryAdmissionStatus.WARNING
        else:
            run.status = PaperModeDryAdmissionStatus.COMPLETED_NO_WRITE

        if refresh:
            run.all_writes_blocked = refresh.all_writes_blocked
            run.mutation_detected = refresh.mutation_detected

        safety_issues = self.validate_run_safety(run)
        if safety_issues:
            run.warnings.extend(safety_issues)
            run.status = PaperModeDryAdmissionStatus.BLOCKED

        run.completed_at_utc = datetime.now(timezone.utc).isoformat()
        return run

    def run_step(self, step_name: str, plan: PaperModeDryAdmissionPlan, paper_snapshot: dict[str, Any]) -> DryAdmissionStep:
        return DryAdmissionStep(
            step_id=create_dry_admission_step_id(),
            step_name=step_name,
            status=DryAdmissionStepStatus.COMPLETED_NO_WRITE,
            write_attempted=False,
            order_attempted=False,
            broker_send_attempted=False,
            config_patch_attempted=False,
            telegram_real_send_attempted=False,
            active_paper_enable_attempted=False,
            mutation_detected=False
        )

    def build_write_lock_refresh_for_run(
        self,
        no_write_payload: dict[str, Any] | None = None,
        paper_snapshot: dict[str, Any] | None = None
    ) -> RuntimeWriteLockProofRefresh:
        return refresh_runtime_write_lock_proof(no_write_payload, paper_snapshot, paper_snapshot)

    def build_human_ledger_for_run(self, candidate_id: str | None = None) -> HumanApprovalLedger:
        return build_default_human_approval_ledger(candidate_id)

    def validate_run_safety(self, run: PaperModeDryAdmissionRun) -> List[str]:
        issues = []
        if run.activation_allowed:
            issues.append("activation_allowed is True")
        if not run.activation_denied:
            issues.append("activation_denied is False")
        if not run.all_writes_blocked:
            issues.append("all_writes_blocked is False")
        if run.mutation_detected:
            issues.append("mutation_detected is True")

        for step in run.steps:
            if step.write_attempted or step.order_attempted or step.broker_send_attempted or step.config_patch_attempted or step.telegram_real_send_attempted or step.active_paper_enable_attempted or step.mutation_detected:
                issues.append(f"Step {step.step_name} has invalid attempt flags")

        return issues

    def determine_run_decision(
        self,
        steps: List[DryAdmissionStep],
        refresh: RuntimeWriteLockProofRefresh | None,
        ledger: HumanApprovalLedger | None
    ) -> PaperModeDryAdmissionDecision:

        if any(s.status == DryAdmissionStepStatus.FAILED for s in steps):
            return PaperModeDryAdmissionDecision.BLOCK

        if refresh and not refresh.all_writes_blocked:
            return PaperModeDryAdmissionDecision.REQUEST_WRITE_LOCK_PROOF_REFRESH

        if ledger and ledger.missing_scopes:
            return PaperModeDryAdmissionDecision.REQUEST_HUMAN_LEDGER_REVIEW

        return PaperModeDryAdmissionDecision.REQUEST_MANUAL_REVIEW

    def dry_admission_run_summary(self, run: PaperModeDryAdmissionRun) -> dict[str, Any]:
        return {
            "run_id": run.run_id,
            "status": run.status.value,
            "decision": run.decision.value,
            "steps_completed": len([s for s in run.steps if s.status == DryAdmissionStepStatus.COMPLETED_NO_WRITE]),
            "safety_issues": len(self.validate_run_safety(run))
        }
