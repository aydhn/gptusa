from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunProposal,
    DryRunBridgeSession,
    DryRunBridgeSessionStatus,
    DryRunBridgeMode,
    create_dry_run_bridge_session_id,
    BridgeTelemetryEvent,
    HumanReviewCheckpoint,
    validate_dry_run_bridge_context,
    validate_dry_run_proposal,
    validate_human_review_checkpoint
)
from usa_signal_bot.paper_dry_run_bridge.proposal_generator import generate_dry_run_proposals, validate_dry_run_proposals_safe
from usa_signal_bot.paper_dry_run_bridge.risk_evaluator import evaluate_dry_run_proposals_risk
from usa_signal_bot.paper_dry_run_bridge.notification_preview import build_dry_run_notification_preview, validate_dry_run_notification_preview_safe
from usa_signal_bot.paper_dry_run_bridge.human_review_checkpoint import build_human_review_checkpoint
from usa_signal_bot.paper_dry_run_bridge.operation_monitor import monitor_allowed_operation
from usa_signal_bot.paper_dry_run_bridge.blocked_operation_telemetry import create_blocked_operation_event

class SupervisedDryRunBridgeRunner:
    def __init__(self, mode: DryRunBridgeMode = DryRunBridgeMode.FULL_SUPERVISED_DRY_RUN):
        self.mode = mode

    def run_session(self, context: DryRunBridgeContext) -> DryRunBridgeSession:
        session_id = create_dry_run_bridge_session_id()
        started_at = datetime.now(timezone.utc).isoformat()

        telemetry = [monitor_allowed_operation("session_start", session_id)]

        try:
            validate_dry_run_bridge_context(context)
        except ValueError as e:
            telemetry.append(create_blocked_operation_event("context_validation", str(e), session_id))
            return DryRunBridgeSession(
                session_id=session_id,
                created_at_utc=started_at,
                status=DryRunBridgeSessionStatus.FAILED,
                context=context,
                proposals=[],
                telemetry_events=telemetry,
                human_checkpoints=[],
                safety_flags=[],
                started_at_utc=started_at,
                completed_at_utc=datetime.now(timezone.utc).isoformat(),
                output_paths={},
                warnings=["Context validation failed"],
                errors=[str(e)]
            )

        proposals = self.run_proposal_stage(context)
        telemetry.append(monitor_allowed_operation("generate_proposals", session_id))

        if self.mode != DryRunBridgeMode.CANDIDATE_PROPOSAL_ONLY:
            proposals = self.run_risk_stage(context, proposals)
            telemetry.append(monitor_allowed_operation("evaluate_risk", session_id))

        if self.mode in [DryRunBridgeMode.FULL_SUPERVISED_DRY_RUN, DryRunBridgeMode.NOTIFICATION_PREVIEW_ONLY]:
            notification_payload = self.run_notification_stage(context, proposals)
            telemetry.append(monitor_allowed_operation("generate_notification", session_id))

        checkpoint = self.build_checkpoint_stage(context, session_id)
        telemetry.append(monitor_allowed_operation("build_checkpoint", session_id))

        telemetry.extend(self.build_session_telemetry(context, proposals, checkpoint))

        session = DryRunBridgeSession(
            session_id=session_id,
            created_at_utc=started_at,
            status=DryRunBridgeSessionStatus.COMPLETED,
            context=context,
            proposals=proposals,
            telemetry_events=telemetry,
            human_checkpoints=[checkpoint],
            safety_flags=[],
            started_at_utc=started_at,
            completed_at_utc=datetime.now(timezone.utc).isoformat(),
            output_paths={},
            warnings=[],
            errors=[]
        )

        errors = self.validate_session_safety(session)
        if errors:
            session.status = DryRunBridgeSessionStatus.BLOCKED
            session.errors.extend(errors)

        return session

    def run_proposal_stage(self, context: DryRunBridgeContext) -> List[DryRunProposal]:
        proposals = generate_dry_run_proposals(context)
        errors = validate_dry_run_proposals_safe(proposals)
        if errors:
            raise ValueError(f"Unsafe proposals generated: {errors}")
        return proposals

    def run_risk_stage(self, context: DryRunBridgeContext, proposals: List[DryRunProposal]) -> List[DryRunProposal]:
        return evaluate_dry_run_proposals_risk(proposals, context)

    def run_notification_stage(self, context: DryRunBridgeContext, proposals: List[DryRunProposal]) -> dict[str, Any]:
        payload = build_dry_run_notification_preview(context, proposals)
        errors = validate_dry_run_notification_preview_safe(payload)
        if errors:
            raise ValueError(f"Unsafe notification preview generated: {errors}")
        return payload

    def build_checkpoint_stage(self, context: DryRunBridgeContext, session_id: Optional[str] = None) -> HumanReviewCheckpoint:
        checkpoint = build_human_review_checkpoint(context, session_id)
        validate_human_review_checkpoint(checkpoint)
        return checkpoint

    def build_session_telemetry(self, context: DryRunBridgeContext, proposals: List[DryRunProposal], checkpoint: HumanReviewCheckpoint) -> List[BridgeTelemetryEvent]:
        # Implementation details inside session runner for basic events
        return []

    def validate_session_safety(self, session: DryRunBridgeSession) -> List[str]:
        errors = []
        try:
            validate_dry_run_bridge_context(session.context)
        except Exception as e:
            errors.append(str(e))

        for p in session.proposals:
            try:
                validate_dry_run_proposal(p)
            except Exception as e:
                errors.append(str(e))

        for c in session.human_checkpoints:
            try:
                validate_human_review_checkpoint(c)
            except Exception as e:
                errors.append(str(e))

        return errors
