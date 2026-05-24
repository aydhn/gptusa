from dataclasses import dataclass
from typing import Any

@dataclass
class NotificationMessage:
    content: str
    channel: str = "dry_run"

def format_board_dossier_report_message(review: Any) -> NotificationMessage:
    content = f"Board Dossier Report: {review.review_id}\n"
    content += "Status: " + ("VALIDATED_NON_EXECUTION" if not review.errors else "BLOCKED")
    content += "\nNote: Board dossier review required. No actual paper launch or broker execution occurs."
    return NotificationMessage(content=content)

def format_acceptance_board_seal_warning_message(seals: list[Any]) -> NotificationMessage:
    content = f"Acceptance Board Seal Warning: {len(seals)} seals require review."
    return NotificationMessage(content=content)

def format_shadow_launch_blocker_warning_message(events: list[Any]) -> NotificationMessage:
    unblocked = sum(1 for e in events if not e.blocked)
    content = f"Shadow Launch Blocker Warning: {unblocked} attempts were not blocked."
    return NotificationMessage(content=content)

def notifications_from_board_dossier_review(review: Any) -> list[NotificationMessage]:
    msgs = [format_board_dossier_report_message(review)]
    if review.warnings:
        msgs.append(NotificationMessage(content="Warnings detected in board dossier."))
    return msgs

def format_dry_admission_gate_report_message(review: dict) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType
    passed = review.get("gate_passed", False)
    status = "PASSED" if passed else "FAILED"
    subject = f"Dry Admission Gate Review - {status}"
    body = f"Dry admission gate evaluation completed.\nStatus: {status}\nLimitations: No active paper/broker/live/demo allowed.\nNot investment advice."
    return NotificationMessage(
        message_id="preview",
        message_type=NotificationType.DRY_ADMISSION_GATE_REPORT.value if hasattr(NotificationType, 'DRY_ADMISSION_GATE_REPORT') else "DRY_ADMISSION_GATE_REPORT",
        subject=subject,
        body=body,
        priority="HIGH",
        channels=["dry_run"],
        metadata=review
    )

def format_shadow_launch_replay_warning_message(results: list) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType
    subject = "Shadow Launch Replay Warning"
    body = f"Issues detected in {len(results)} shadow replay attempts."
    return NotificationMessage(
        message_id="preview",
        message_type=NotificationType.SHADOW_LAUNCH_REPLAY_WARNING.value if hasattr(NotificationType, 'SHADOW_LAUNCH_REPLAY_WARNING') else "SHADOW_LAUNCH_REPLAY_WARNING",
        subject=subject,
        body=body,
        priority="HIGH",
        channels=["dry_run"],
        metadata={"count": len(results)}
    )

def format_board_evidence_freeze_warning_message(freezes: list) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType
    subject = "Board Evidence Freeze Warning"
    body = f"Issues detected in {len(freezes)} evidence freezes (missing or stale)."
    return NotificationMessage(
        message_id="preview",
        message_type=NotificationType.BOARD_EVIDENCE_FREEZE_WARNING.value if hasattr(NotificationType, 'BOARD_EVIDENCE_FREEZE_WARNING') else "BOARD_EVIDENCE_FREEZE_WARNING",
        subject=subject,
        body=body,
        priority="HIGH",
        channels=["dry_run"],
        metadata={"count": len(freezes)}
    )

def notifications_from_dry_admission_gate_review(review: dict) -> list['NotificationMessage']:
    messages = []
    messages.append(format_dry_admission_gate_report_message(review))
    return messages

def format_dry_admission_dossier_report_message(review: Any) -> Any:
    msg = NotificationMessage()
    msg.text = f"Dry-Admission Dossier Review Required. Review ID: {review.review_id}"
    return msg

def format_dry_admission_acceptance_seal_warning_message(seals: list) -> Any:
    msg = NotificationMessage()
    msg.text = f"Dry-Admission Acceptance Seal Warning: {len(seals)} seals evaluated."
    return msg

def format_rehearsal_blocker_warning_message(events: list) -> Any:
    msg = NotificationMessage()
    msg.text = f"Rehearsal Blocker Warning: {len(events)} attempts evaluated."
    return msg

def notifications_from_dry_admission_dossier_review(review: Any) -> list:
    return [format_dry_admission_dossier_report_message(review)]

def format_handoff_freeze_report_message(review: Any) -> NotificationMessage:
    lines = [
        "🧊 PRE-PAPER HANDOFF FREEZE REVIEW REQUIRED",
        f"Review ID: {review.review_id}",
        f"Gates evaluated: {len(review.gates)}",
        f"Passed: {all(g.pre_paper_handoff_complete for g in review.gates)}"
    ]
    if review.warnings:
        lines.append(f"Warnings: {len(review.warnings)}")

    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.PRE_PAPER_HANDOFF_FREEZE_REPORT,
        priority=NotificationPriority.NORMAL,
        subject="Handoff Freeze Gate Summary",
        body="\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"review_id": review.review_id}
    )

def format_sandbox_runtime_admission_replay_warning_message(results: List[Any]) -> NotificationMessage:
    lines = ["⚠️ SANDBOX RUNTIME ADMISSION REPLAY WARNING", f"Replay results with unblocked attempts: {len(results)}"]

    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.SANDBOX_RUNTIME_ADMISSION_REPLAY_WARNING,
        priority=NotificationPriority.HIGH,
        subject="Sandbox Runtime Admission Replay: Unblocked Attempts",
        body="\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"warning_count": len(results)}
    )

def format_simulator_evidence_freeze_warning_message(freezes: List[Any]) -> NotificationMessage:
    lines = ["🚨 SIMULATOR EVIDENCE FREEZE WARNING", f"Freezes missing evidence or stale: {len(freezes)}"]

    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.SIMULATOR_EVIDENCE_FREEZE_WARNING,
        priority=NotificationPriority.CRITICAL,
        subject="Simulator Evidence Freeze: Incomplete",
        body="\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"warning_count": len(freezes)}
    )

def notifications_from_handoff_freeze_review(review: Any) -> List[NotificationMessage]:
    msgs = [format_handoff_freeze_report_message(review)]

    replay_warnings = [r for r in review.sandbox_replay_results if not r.passed]
    if replay_warnings:
        msgs.append(format_sandbox_runtime_admission_replay_warning_message(replay_warnings))

    freeze_warnings = [f for f in review.evidence_freezes if f.missing_evidence_count > 0 or f.stale_evidence_count > 0]
    if freeze_warnings:
        msgs.append(format_simulator_evidence_freeze_warning_message(freeze_warnings))

    return msgs


def format_runtime_registry_report_message(review: Any) -> NotificationMessage:
    content = f"Runtime Registry Normalized: {review.review_id}\n"
    content += "Status: " + ("VALIDATED_NON_EXECUTION" if not review.errors else "BLOCKED")
    content += "\nNote: Phase 102 runtime registry. Not an activation. No live execution."
    return NotificationMessage(content=content)

def notifications_from_runtime_registry_review(review: Any) -> list[NotificationMessage]:
    msgs = [format_runtime_registry_report_message(review)]
    if review.warnings:
        msgs.append(NotificationMessage(content="Warnings detected in runtime registry."))
    return msgs

from usa_signal_bot.runtime_service_graph.phase103_models import RuntimeServiceGraphFullReview, OrchestrationDryRunResult

def format_runtime_service_graph_report_message(review: RuntimeServiceGraphFullReview) -> NotificationMessage:
    return NotificationMessage()

def format_orchestration_dry_run_warning_message(result: OrchestrationDryRunResult) -> NotificationMessage:
    return NotificationMessage()

def notifications_from_runtime_service_graph_review(review: RuntimeServiceGraphFullReview) -> list:
    return []


def format_runtime_lifecycle_report_message(review) -> NotificationMessage:
    return NotificationMessage(
        subject="Phase 104 Lifecycle Review",
        body=f"Review completed. Gate Decision: {review.readiness_gate.decision.value}",
        metadata={"review_id": review.review_id},
        message_type=NotificationType.RUNTIME_LIFECYCLE_REPORT,
        priority=NotificationPriority.INFO
    )

def format_startup_check_warning_message(report) -> NotificationMessage:
    return NotificationMessage(
        subject="Startup Check Warning",
        body=f"Startup checks resulted in status {report.status.value}",
        metadata={"report_id": report.report_id},
        message_type=NotificationType.STARTUP_CHECK_WARNING,
        priority=NotificationPriority.WARNING
    )

def format_readiness_gate_warning_message(gate) -> NotificationMessage:
    return NotificationMessage(
        subject="Readiness Gate Warning",
        body=f"Readiness gate decision: {gate.decision.value}",
        metadata={"gate_id": gate.gate_id},
        message_type=NotificationType.READINESS_GATE_WARNING,
        priority=NotificationPriority.WARNING
    )

def notifications_from_runtime_lifecycle_review(review) -> list[NotificationMessage]:
    return [format_runtime_lifecycle_report_message(review)]
