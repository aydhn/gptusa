import re

def update_notifs():
    with open('usa_signal_bot/notifications/notification_templates.py', 'r') as f:
        content = f.read()

    new_funcs = """
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
        body="\\n".join(lines),
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
        body="\\n".join(lines),
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
        body="\\n".join(lines),
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
"""
    if "format_handoff_freeze_report_message" not in content:
        content += new_funcs
        with open('usa_signal_bot/notifications/notification_templates.py', 'w') as f:
            f.write(content)

update_notifs()
