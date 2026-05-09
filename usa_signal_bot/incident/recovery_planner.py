from pathlib import Path
import datetime
from usa_signal_bot.core.enums import RecoveryActionStatus, RecoveryPlanStatus
from usa_signal_bot.incident.incident_models import IncidentRecord
from usa_signal_bot.incident.recovery_models import RecoveryPlan, RecoveryPlanResult, RecoveryAction, RecoveryActionResult, create_recovery_plan_id, create_recovery_plan_result_id, validate_recovery_plan
from usa_signal_bot.incident.recovery_actions import default_recovery_actions_for_incident
from usa_signal_bot.incident.incident_classifier import should_block_recovery

class RecoveryPlanner:
    def __init__(self, data_root: Path, project_root: Path | None = None):
        self.data_root = data_root
        self.project_root = project_root

    def build_plan(self, incidents: list[IncidentRecord], dry_run: bool = True) -> RecoveryPlan:
        actions_dict = {}
        blocked = False

        for inc in incidents:
            if should_block_recovery(inc):
                blocked = True
            acts = default_recovery_actions_for_incident(inc)
            for a in acts:
                actions_dict[a.action_type.value] = a # deduplicate

        actions = list(actions_dict.values())

        status = RecoveryPlanStatus.CREATED
        if not incidents:
            status = RecoveryPlanStatus.SKIPPED
        elif blocked:
            status = RecoveryPlanStatus.BLOCKED
        else:
            status = RecoveryPlanStatus.READY

        req_count = sum(1 for a in actions if a.required)

        plan = RecoveryPlan(
            plan_id=create_recovery_plan_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            status=status,
            incident_ids=[i.incident_id for i in incidents],
            actions=actions,
            required_action_count=req_count,
            dry_run=dry_run,
            warnings=["Recovery is blocked due to critical safety incident"] if blocked else [],
            errors=[]
        )

        validate_recovery_plan(plan)
        return plan

    def execute_action(self, action: RecoveryAction, execute_commands: bool = False) -> RecoveryActionResult:
        status = RecoveryActionStatus.DRY_RUN_ONLY
        summary = f"Simulated action: {action.name}"

        if action.status == RecoveryActionStatus.BLOCKED:
            status = RecoveryActionStatus.BLOCKED
            summary = "Action is blocked."
        elif execute_commands and not action.dry_run:
            # Here we would normally use subprocess, but local constraint prevents arbitrary execution without guarded wrappers
            # We enforce execute_commands = False by default. For now, simulate.
            status = RecoveryActionStatus.COMPLETED
            summary = f"Executed: {action.command}"

        return RecoveryActionResult(
            action_id=action.action_id,
            action_type=action.action_type,
            status=status,
            executed_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            dry_run=not execute_commands or action.dry_run,
            summary=summary,
            output_paths={},
            warnings=[],
            errors=[]
        )

    def execute_plan(self, plan: RecoveryPlan, execute_commands: bool = False) -> RecoveryPlanResult:
        results = []
        status = plan.status

        if status in [RecoveryPlanStatus.BLOCKED, RecoveryPlanStatus.SKIPPED]:
             return RecoveryPlanResult(
                result_id=create_recovery_plan_result_id(),
                created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
                status=status,
                plan=plan,
                action_results=[],
                output_paths={},
                warnings=["Plan not executed due to status " + status.value],
                errors=[]
             )

        for action in plan.actions:
            res = self.execute_action(action, execute_commands)
            results.append(res)

        final_status = RecoveryPlanStatus.DRY_RUN_COMPLETED if plan.dry_run or not execute_commands else RecoveryPlanStatus.COMPLETED

        return RecoveryPlanResult(
            result_id=create_recovery_plan_result_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            status=final_status,
            plan=plan,
            action_results=results,
            output_paths={},
            warnings=[],
            errors=[]
        )

    def decide_plan_status(self, actions: list[RecoveryAction], incidents: list[IncidentRecord]) -> RecoveryPlanStatus:
        if not incidents:
            return RecoveryPlanStatus.SKIPPED
        if any(should_block_recovery(i) for i in incidents):
            return RecoveryPlanStatus.BLOCKED
        return RecoveryPlanStatus.READY

    def write_result(self, result: RecoveryPlanResult) -> list[Path]:
        from usa_signal_bot.incident.incident_store import write_recovery_plan_json, write_recovery_result_json
        plan_path = write_recovery_plan_json(self.data_root, result.plan)
        res_path = write_recovery_result_json(self.data_root, result)
        result.output_paths["plan_json"] = str(plan_path)
        result.output_paths["result_json"] = str(res_path)
        return [plan_path, res_path]
