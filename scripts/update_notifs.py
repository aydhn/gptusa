def update_notifs():
    with open('usa_signal_bot/notifications/notification_templates.py', 'r') as f:
        content = f.read()

    new_funcs = """
def format_regime_cost_report_message(review: Any) -> NotificationMessage:
    lines = [
        "📊 REGIME COST REVIEW",
        f"Review ID: {review.review_id}",
        f"Symbols Processed: {len(review.symbols)}",
        f"High Risk/Blocked: {sum(1 for s in review.snapshots if s.combined_regime.value in ['HIGH_RISK', 'BLOCKED'])}"
    ]
    if review.warnings:
        lines.append(f"Warnings: {len(review.warnings)}")

    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.REGIME_COST_REPORT,
        priority=NotificationPriority.NORMAL,
        subject="Regime Cost Review Summary",
        body="\\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"review_id": review.review_id}
    )

def format_adaptive_execution_warning_message(decisions: List[Any]) -> NotificationMessage:
    blocked = [d.symbol for d in decisions if d.decision.value == "BLOCK_FILL_SIMULATION"]
    lines = ["⚠️ ADAPTIVE EXECUTION BLOCKED WARNING", f"Symbols Blocked: {len(blocked)}"]
    if blocked:
        lines.append(f"Examples: {', '.join(blocked[:5])}")

    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.ADAPTIVE_EXECUTION_WARNING,
        priority=NotificationPriority.HIGH,
        subject="Adaptive Execution: Fills Blocked",
        body="\\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"blocked_count": len(blocked)}
    )

def format_regime_cost_block_warning_message(review: Any) -> NotificationMessage:
    lines = ["🚨 REGIME COST BLOCK WARNING", f"Review {review.review_id} contained blocked symbols."]
    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.REGIME_COST_BLOCK_WARNING,
        priority=NotificationPriority.CRITICAL,
        subject="Regime Cost: Operations Blocked",
        body="\\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"review_id": review.review_id}
    )
"""
    if "format_regime_cost_report_message" not in content:
        content += new_funcs
        with open('usa_signal_bot/notifications/notification_templates.py', 'w') as f:
            f.write(content)

update_notifs()
