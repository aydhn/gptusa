import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxRuntimeMode, SandboxStatus
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxPreviewRun, SandboxRuntimeContext, SandboxPreviewOutput, create_sandbox_preview_run_id
)
from usa_signal_bot.release_sandbox.signal_preview import build_signal_preview, validate_signal_preview_safe
from usa_signal_bot.release_sandbox.portfolio_preview import build_portfolio_preview, validate_portfolio_preview_safe
from usa_signal_bot.release_sandbox.risk_preview import build_risk_preview, validate_risk_preview_safe
from usa_signal_bot.release_sandbox.notification_preview import build_sandbox_notification_preview, validate_notification_preview_safe
from usa_signal_bot.release_sandbox.blocked_operation_guard import sandbox_operation_decision

class SafePreviewRunner:
    def __init__(self, runtime_mode: SandboxRuntimeMode = SandboxRuntimeMode.FULL_SAFE_PREVIEW):
        self.runtime_mode = runtime_mode

    def run_signal_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewOutput:
        return build_signal_preview(context)

    def run_portfolio_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewOutput:
        return build_portfolio_preview(context)

    def run_risk_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewOutput:
        return build_risk_preview(context)

    def run_notification_preview(self, context: SandboxRuntimeContext, outputs: List[SandboxPreviewOutput]) -> SandboxPreviewOutput:
        return build_sandbox_notification_preview(context, outputs)

    def validate_outputs(self, outputs: List[SandboxPreviewOutput]) -> List[str]:
        warnings = []
        for o in outputs:
            if o.output_type == "SIGNAL_PREVIEW":
                warnings.extend(validate_signal_preview_safe(o))
            elif o.output_type == "PORTFOLIO_PREVIEW":
                warnings.extend(validate_portfolio_preview_safe(o))
            elif o.output_type == "RISK_PREVIEW":
                warnings.extend(validate_risk_preview_safe(o))
            elif o.output_type == "NOTIFICATION_PREVIEW":
                warnings.extend(validate_notification_preview_safe(o))
        return warnings

    def run_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewRun:
        started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        outputs = []
        outputs.append(self.run_signal_preview(context))
        outputs.append(self.run_portfolio_preview(context))
        outputs.append(self.run_risk_preview(context))
        outputs.append(self.run_notification_preview(context, outputs))

        warnings = self.validate_outputs(outputs)
        status = SandboxStatus.COMPLETED if not warnings else SandboxStatus.WARNING

        completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        return SandboxPreviewRun(
            run_id=create_sandbox_preview_run_id(),
            created_at_utc=started_at,
            sandbox_id=context.sandbox_id,
            bundle_id=context.bundle_id,
            bundle_version=context.bundle_version,
            runtime_mode=self.runtime_mode,
            status=status,
            context=context,
            outputs=outputs,
            operation_decisions=[], # Could track guards run here
            safety_flags=[],
            started_at_utc=started_at,
            completed_at_utc=completed_at,
            warnings=warnings,
            errors=[]
        )

def preview_run_summary(run: SandboxPreviewRun) -> Dict[str, Any]:
    return {
        "run_id": run.run_id,
        "status": run.status.value,
        "runtime_mode": run.runtime_mode.value,
        "outputs_count": len(run.outputs),
        "warnings_count": len(run.warnings)
    }
