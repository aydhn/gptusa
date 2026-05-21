import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    StageRehearsalStatus, ReadinessRehearsalStatus, ReadinessRehearsalDecision, ReadinessRehearsalRiskFlag
)
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    StageRehearsalPlan, StageRehearsalResult, ReadinessRehearsalRun,
    create_stage_rehearsal_result_id, create_readiness_rehearsal_run_id,
    validate_readiness_rehearsal_run
)
from usa_signal_bot.paper_readiness_rehearsal.stage_safety_validator import (
    validate_stage_plan_safety, validate_stage_result_safety,
    collect_stage_plan_safety_flags, collect_stage_result_safety_flags
)

class StagedReadinessRehearsalRunner:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def run_rehearsal(self, plans: List[StageRehearsalPlan], source_package_id: Optional[str] = None, candidate_id: Optional[str] = None) -> ReadinessRehearsalRun:
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        results = []
        all_flags = []

        for plan in plans:
            plan_flags = collect_stage_plan_safety_flags(plan)
            all_flags.extend(plan_flags)
            if plan_flags:
                plan.status = StageRehearsalStatus.BLOCKED
                plan.errors.append("Blocked due to safety flags")
                results.append(self._create_failed_result(plan, "Blocked prior to run"))
                continue

            res = self.run_stage(plan)
            res_flags = collect_stage_result_safety_flags(res)
            all_flags.extend(res_flags)
            results.append(res)

        decision = self.determine_run_decision(results)
        status = ReadinessRehearsalStatus.COMPLETED if decision == ReadinessRehearsalDecision.RUN_STAGED_REHEARSAL else ReadinessRehearsalStatus.FAILED
        if any(r.status == StageRehearsalStatus.BLOCKED for r in results) or all_flags:
            status = ReadinessRehearsalStatus.BLOCKED
            decision = ReadinessRehearsalDecision.BLOCK

        run = ReadinessRehearsalRun(
            run_id=create_readiness_rehearsal_run_id(),
            created_at_utc=now_utc,
            status=status,
            source_package_id=source_package_id,
            candidate_id=candidate_id,
            stage_plans=plans,
            stage_results=results,
            decision=decision,
            safety_flags=list(set(all_flags)),
            started_at_utc=now_utc,
            completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            output_paths={},
            warnings=[],
            errors=[]
        )
        validate_readiness_rehearsal_run(run)
        return run

    def run_stage(self, plan: StageRehearsalPlan) -> StageRehearsalResult:
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return StageRehearsalResult(
            result_id=create_stage_rehearsal_result_id(),
            created_at_utc=now_utc,
            source_stage=plan.source_stage,
            status=StageRehearsalStatus.COMPLETED,
            input_refs=plan.required_inputs,
            output_refs=plan.expected_outputs,
            safety_flags=[],
            passed_safety_checks=True,
            execution_attempted=False,
            active_paper_attempted=False,
            broker_execution_attempted=False,
            paper_state_mutation_attempted=False,
            config_patch_attempted=False,
            warnings=[],
            errors=[]
        )

    def _create_failed_result(self, plan: StageRehearsalPlan, error_msg: str) -> StageRehearsalResult:
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return StageRehearsalResult(
            result_id=create_stage_rehearsal_result_id(),
            created_at_utc=now_utc,
            source_stage=plan.source_stage,
            status=StageRehearsalStatus.FAILED,
            input_refs=plan.required_inputs,
            output_refs=plan.expected_outputs,
            safety_flags=[ReadinessRehearsalRiskFlag.STAGE_REHEARSAL_FAILED],
            passed_safety_checks=False,
            execution_attempted=False,
            active_paper_attempted=False,
            broker_execution_attempted=False,
            paper_state_mutation_attempted=False,
            config_patch_attempted=False,
            warnings=[],
            errors=[error_msg]
        )

    def validate_run_safety(self, run: ReadinessRehearsalRun) -> List[str]:
        errors = []
        for r in run.stage_results:
            errors.extend(validate_stage_result_safety(r))
        return errors

    def determine_run_decision(self, results: List[StageRehearsalResult]) -> ReadinessRehearsalDecision:
        if not results:
            return ReadinessRehearsalDecision.INCONCLUSIVE
        if any(r.status in [StageRehearsalStatus.FAILED, StageRehearsalStatus.BLOCKED] for r in results):
            return ReadinessRehearsalDecision.BLOCK
        return ReadinessRehearsalDecision.RUN_STAGED_REHEARSAL

    def rehearsal_run_summary(self, run: ReadinessRehearsalRun) -> Dict[str, Any]:
        return {
            "run_id": run.run_id,
            "status": run.status.value,
            "decision": run.decision.value,
            "stage_count": len(run.stage_plans),
            "safety_flags": len(run.safety_flags)
        }
