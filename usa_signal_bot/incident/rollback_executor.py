from pathlib import Path
import datetime
import zipfile
import shutil
from usa_signal_bot.core.enums import RollbackPlanStatus, RollbackStepStatus, RollbackSafetyStatus
from usa_signal_bot.incident.rollback_models import (
    RollbackSource, RollbackStep, RollbackPlan, RollbackExecutionResult,
    create_rollback_step_id, create_rollback_plan_id, create_rollback_execution_id, validate_rollback_plan
)

class RollbackExecutor:
    def __init__(self, project_root: Path, data_root: Path):
        self.project_root = project_root
        self.data_root = data_root

    def build_steps_from_source(self, source: RollbackSource, dry_run: bool = True) -> list[RollbackStep]:
        steps = []
        p = Path(source.path)
        if not p.exists():
            return steps

        if p.suffix == ".zip":
            # Simulate extract
            try:
                with zipfile.ZipFile(p, 'r') as zf:
                    for name in zf.namelist():
                        if name.endswith('/'):
                            continue
                        target = str(self.project_root / name)
                        # Identify protected paths heuristically
                        protected = any(term in name for term in ["config/", "secrets", ".yaml", ".env", "usa_signal_bot/", "docs/", "tests/"])
                        steps.append(RollbackStep(
                            step_id=create_rollback_step_id(name),
                            name=f"Extract {name}",
                            source_path=source.path + "::" + name,
                            target_path=target,
                            status=RollbackStepStatus.PENDING,
                            action="EXTRACT",
                            dry_run=dry_run,
                            protected=protected
                        ))
            except Exception as e:
                pass # Precheck handles errors
        else:
            # Single file replace
            target = str(self.data_root / p.name)
            protected = any(term in p.name for term in ["config", "secrets", ".yaml", ".env"])
            steps.append(RollbackStep(
                step_id=create_rollback_step_id(p.name),
                name=f"Copy {p.name}",
                source_path=source.path,
                target_path=target,
                status=RollbackStepStatus.PENDING,
                action="COPY",
                dry_run=dry_run,
                protected=protected
            ))
        return steps

    def verify_step_safe(self, step: RollbackStep) -> tuple[bool, str]:
        if step.protected:
            return False, "Target is protected."

        target = Path(step.target_path).resolve()
        proj = self.project_root.resolve()
        try:
             # must be inside project
             target.relative_to(proj)
        except ValueError:
             return False, "Target is outside project root."

        return True, "Safe."

    def build_plan(self, source: RollbackSource, dry_run: bool = True) -> RollbackPlan:
        steps = self.build_steps_from_source(source, dry_run)

        safety = RollbackSafetyStatus.SAFE
        for s in steps:
            safe, msg = self.verify_step_safe(s)
            if not safe:
                s.warnings.append(msg)
                if s.protected:
                    safety = RollbackSafetyStatus.WARNING
                else:
                    safety = RollbackSafetyStatus.BLOCKED

        plan = RollbackPlan(
            plan_id=create_rollback_plan_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            status=RollbackPlanStatus.CREATED if safety != RollbackSafetyStatus.BLOCKED else RollbackPlanStatus.BLOCKED,
            source=source,
            dry_run=dry_run,
            steps=steps,
            safety_status=safety,
            warnings=["Plan contains protected paths" if safety == RollbackSafetyStatus.WARNING else ""],
            errors=["Plan blocked due to unsafe paths" if safety == RollbackSafetyStatus.BLOCKED else ""]
        )
        # Clear empty lists
        plan.warnings = [w for w in plan.warnings if w]
        plan.errors = [e for e in plan.errors if e]

        validate_rollback_plan(plan)
        return plan

    def execute_step(self, step: RollbackStep, force: bool = False, allow_overwrite: bool = False) -> RollbackStep:
        if step.dry_run:
            step.status = RollbackStepStatus.DRY_RUN_OK
            return step

        safe, msg = self.verify_step_safe(step)
        if not safe and not force:
            step.status = RollbackStepStatus.BLOCKED
            step.errors.append(f"Blocked: {msg}")
            return step

        if step.protected:
            step.status = RollbackStepStatus.BLOCKED
            step.errors.append("Blocked: Cannot overwrite protected path.")
            return step

        target = Path(step.target_path)
        if target.exists() and not allow_overwrite:
            step.status = RollbackStepStatus.BLOCKED
            step.errors.append("Blocked: Target exists and allow_overwrite is False.")
            return step

        # Actual execution (extremely rare in this system, mostly reserved)
        try:
            if step.action == "COPY":
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(step.source_path, target)
                step.status = RollbackStepStatus.EXECUTED
            elif step.action == "EXTRACT":
                source_archive, inner_name = step.source_path.split("::", 1)
                with zipfile.ZipFile(source_archive, 'r') as zf:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(inner_name) as z_in, open(target, 'wb') as f_out:
                        shutil.copyfileobj(z_in, f_out)
                step.status = RollbackStepStatus.EXECUTED
            else:
                step.status = RollbackStepStatus.FAILED
                step.errors.append("Unknown action.")
        except Exception as e:
            step.status = RollbackStepStatus.FAILED
            step.errors.append(str(e))

        return step

    def dry_run(self, plan: RollbackPlan) -> RollbackExecutionResult:
        plan.dry_run = True
        for s in plan.steps:
            s.dry_run = True
        return self.execute(plan, force=False, allow_overwrite=False)

    def execute(self, plan: RollbackPlan, force: bool = False, allow_overwrite: bool = False) -> RollbackExecutionResult:
        executed = []
        skipped = []
        failed = []

        if plan.status == RollbackPlanStatus.BLOCKED:
            return RollbackExecutionResult(
                execution_id=create_rollback_execution_id(),
                created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
                status=RollbackPlanStatus.BLOCKED,
                dry_run=plan.dry_run,
                plan=plan,
                executed_steps=[],
                skipped_steps=plan.steps,
                failed_steps=[],
                warnings=[],
                errors=["Plan is blocked."]
            )

        for step in plan.steps:
            res = self.execute_step(step, force=force, allow_overwrite=allow_overwrite)
            if res.status in [RollbackStepStatus.EXECUTED, RollbackStepStatus.DRY_RUN_OK]:
                executed.append(res)
            elif res.status in [RollbackStepStatus.SKIPPED, RollbackStepStatus.BLOCKED]:
                skipped.append(res)
            else:
                failed.append(res)

        status = RollbackPlanStatus.EXECUTED
        if plan.dry_run:
            status = RollbackPlanStatus.DRY_RUN_COMPLETED
        elif failed:
            status = RollbackPlanStatus.FAILED

        return RollbackExecutionResult(
            execution_id=create_rollback_execution_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            status=status,
            dry_run=plan.dry_run,
            plan=plan,
            executed_steps=executed,
            skipped_steps=skipped,
            failed_steps=failed,
            warnings=[],
            errors=[]
        )
