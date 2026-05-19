import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxRuntimeMode, SandboxStatus, SandboxOperation
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewRun, SandboxRuntimeContext, SandboxPreviewOutput, create_sandbox_preview_run_id
from usa_signal_bot.release_sandbox.signal_preview import build_signal_preview
from usa_signal_bot.release_sandbox.portfolio_preview import build_portfolio_preview
from usa_signal_bot.release_sandbox.risk_preview import build_risk_preview
from usa_signal_bot.release_sandbox.notification_preview import build_sandbox_notification_preview
from usa_signal_bot.release_sandbox.blocked_operation_guard import assert_operation_allowed

class SafePreviewRunner:
    def __init__(self, runtime_mode: SandboxRuntimeMode = SandboxRuntimeMode.FULL_SAFE_PREVIEW):
        self.runtime_mode = runtime_mode

    def run_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewRun:
        started = datetime.datetime.utcnow().isoformat()

        # Enforce Guards
        assert_operation_allowed(SandboxOperation.SEND_ORDER)
        assert_operation_allowed(SandboxOperation.MUTATE_PAPER_STATE)
        assert_operation_allowed(SandboxOperation.SEND_TELEGRAM_REAL)

        outputs = []
        outputs.append(self.run_signal_preview(context))
        outputs.append(self.run_portfolio_preview(context))
        outputs.append(self.run_risk_preview(context))
        outputs.append(self.run_notification_preview(context, outputs))

        return SandboxPreviewRun(
            run_id=create_sandbox_preview_run_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            sandbox_id=context.sandbox_id,
            bundle_id=context.bundle_id,
            bundle_version=context.bundle_version,
            runtime_mode=self.runtime_mode,
            status=SandboxStatus.COMPLETED,
            context=context,
            outputs=outputs,
            operation_decisions=[],
            safety_flags=[],
            started_at_utc=started,
            completed_at_utc=datetime.datetime.utcnow().isoformat(),
            warnings=[],
            errors=[]
        )

    def run_signal_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewOutput:
        return build_signal_preview(context)

    def run_portfolio_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewOutput:
        return build_portfolio_preview(context)

    def run_risk_preview(self, context: SandboxRuntimeContext) -> SandboxPreviewOutput:
        return build_risk_preview(context)

    def run_notification_preview(self, context: SandboxRuntimeContext, outputs: List[SandboxPreviewOutput]) -> SandboxPreviewOutput:
        return build_sandbox_notification_preview(context, outputs)

    def validate_outputs(self, outputs: List[SandboxPreviewOutput]) -> List[str]:
        return []

def preview_run_summary(run: SandboxPreviewRun) -> Dict[str, Any]:
    return {"status": run.status, "outputs": len(run.outputs)}
