import datetime
import re
from typing import Dict, Any, List, Optional

from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority
from usa_signal_bot.notifications.notification_models import NotificationMessage, NotificationConfig, create_notification_message_id
from usa_signal_bot.runtime.runtime_models import MarketScanResult
from usa_signal_bot.portfolio.portfolio_models import PortfolioCandidate, AllocationResult
from usa_signal_bot.risk.risk_models import RiskDecision

from usa_signal_bot.quality.quality_models import ResearchQualityScorecard, ProductionReadinessGateResult, SystemAcceptanceResult
from usa_signal_bot.quality.quality_reporting import (
    research_quality_scorecard_to_text,
    production_readiness_gate_result_to_text,
    system_acceptance_result_to_text
)


def append_disclaimer(text: str, config: Optional[NotificationConfig] = None) -> str:
    if not config or not config.include_disclaimer:
        return text

    disclaimer = f"\n\n---\n_Disclaimer: {config.disclaimer_text}_"
    return f"{text}{disclaimer}"

def chunk_message_text(text: str, max_length: int = 3500) -> List[str]:
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""
    lines = text.split('\n')

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
            # If a single line is longer than max_length, force split it
            if len(line) > max_length:
                for i in range(0, len(line), max_length):
                    chunks.append(line[i:i+max_length])
                current_chunk = ""
            else:
                current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def sanitize_message_text(text: str) -> str:
    # Basic sanitization, especially for Telegram Markdown if needed
    # Escape markdown characters to avoid parse errors if using MARKDOWN format
    text = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
    return text

def compact_number(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return str(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"

    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)

def safe_symbol_list(symbols: List[str], limit: int = 20) -> str:
    if not symbols:
        return "None"

    displayed = ", ".join(symbols[:limit])
    if len(symbols) > limit:
        displayed += f" (+{len(symbols) - limit} more)"
    return displayed

def _create_base_message(
    n_type: NotificationType,
    title: str,
    body: str,
    channel: NotificationChannel = NotificationChannel.DRY_RUN,
    priority: NotificationPriority = NotificationPriority.NORMAL
) -> NotificationMessage:
    return NotificationMessage(
        message_id=create_notification_message_id(),
        notification_type=n_type,
        channel=channel,
        priority=priority,
        title=title,
        body=body,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

def format_scan_summary_message(scan_result: MarketScanResult) -> NotificationMessage:
    title = f"📊 Scan Summary: {scan_result.run_id}"

    status_emoji = "✅" if str(scan_result.status) in ["completed", "RuntimeRunStatus.COMPLETED"] else ("⚠️" if "partial" in str(scan_result.status).lower() else "❌")

    body = (
        f"**Status:** {status_emoji} {scan_result.status}\n"
        f"**Scope:** {scan_result.request.scope}\n"
        f"**Symbols Resolved:** {len(scan_result.resolved_symbols)}\n"
        f"**Signals Generated:** {scan_result.signal_count}\n"
        f"**Candidates Found:** {scan_result.candidate_count}\n"
        f"**Risk Approved:** {scan_result.risk_approved_count}\n"
        f"**Allocations Made:** {scan_result.portfolio_allocation_count}\n"
    )

    if scan_result.errors:
        body += f"\n**Errors ({len(scan_result.errors)}):**\n"
        for err in scan_result.errors[:3]:
            body += f"- {err}\n"

    return _create_base_message(NotificationType.SCAN_SUMMARY, title, body)

def format_selected_candidates_message(candidates: List[Any], limit: int = 10) -> NotificationMessage:
    # Using Any here since SelectedCandidate isn't explicitly imported yet but assumed structurally
    title = f"🎯 Selected Candidates ({len(candidates)})"

    if not candidates:
        return _create_base_message(NotificationType.SELECTED_CANDIDATES, title, "No candidates selected.")

    body = "Review candidates found:\n\n"

    for c in candidates[:limit]:
        # Graceful handling if object or dict
        sym = getattr(c, 'symbol', c.get('symbol', 'UNKNOWN') if isinstance(c, dict) else 'UNKNOWN')
        tf = getattr(c, 'timeframe', c.get('timeframe', 'UNKNOWN') if isinstance(c, dict) else 'UNKNOWN')
        score = getattr(c, 'rank_score', c.get('rank_score', 0) if isinstance(c, dict) else 0)
        action = getattr(c, 'action', c.get('action', 'UNKNOWN') if isinstance(c, dict) else 'UNKNOWN')

        body += f"- **{sym}** ({tf}) - {action} [Score: {score:.2f}]\n"

    if len(candidates) > limit:
        body += f"\n_...and {len(candidates) - limit} more._\n"

    return _create_base_message(NotificationType.SELECTED_CANDIDATES, title, body)

def format_risk_decisions_message(decisions: List[RiskDecision], limit: int = 10) -> NotificationMessage:
    title = f"🛡️ Risk Decisions ({len(decisions)})"

    if not decisions:
        return _create_base_message(NotificationType.RISK_DECISIONS, title, "No risk decisions made.")

    approved = sum(1 for d in decisions if str(d.status) in ["approved", "RiskDecisionStatus.APPROVED"])
    rejected = len(decisions) - approved

    body = f"**Approved:** {approved} | **Rejected/Reduced:** {rejected}\n\n"

    for d in decisions[:limit]:
        status_emoji = "✅" if str(d.status) in ["approved", "RiskDecisionStatus.APPROVED"] else "❌"
        body += f"- {status_emoji} **{d.symbol}** - {d.status}"
        if d.reasons:
            body += f" ({', '.join(d.reasons[:2])})"
        body += "\n"

    if len(decisions) > limit:
        body += f"\n_...and {len(decisions) - limit} more._\n"

    return _create_base_message(NotificationType.RISK_DECISIONS, title, body)

# Assuming PortfolioBasket or list of Allocations
def format_portfolio_basket_message(basket: Any, limit: int = 10) -> NotificationMessage:
    allocations = getattr(basket, 'allocations', basket if isinstance(basket, list) else [])

    title = f"💼 Portfolio Basket ({len(allocations)})"

    if not allocations:
        return _create_base_message(NotificationType.PORTFOLIO_BASKET, title, "No allocations made.")

    body = "Simulated allocation basket:\n\n"

    for a in allocations[:limit]:
        sym = getattr(a, 'symbol', a.get('symbol', 'UNKNOWN') if isinstance(a, dict) else 'UNKNOWN')
        status = getattr(a, 'status', a.get('status', 'UNKNOWN') if isinstance(a, dict) else 'UNKNOWN')
        pct = getattr(a, 'allocation_pct', a.get('allocation_pct', 0) if isinstance(a, dict) else 0)

        body += f"- **{sym}** - {status} ({pct*100:.2f}%)\n"

    if len(allocations) > limit:
        body += f"\n_...and {len(allocations) - limit} more._\n"

    return _create_base_message(NotificationType.PORTFOLIO_BASKET, title, body)

def format_runtime_warning_message(title: str, warnings: List[str], metadata: Optional[Dict[str, Any]] = None) -> NotificationMessage:
    body = "⚠️ **Warnings:**\n\n"
    for w in warnings[:15]:
        body += f"- {w}\n"

    if len(warnings) > 15:
        body += f"\n_...and {len(warnings) - 15} more._\n"

    msg = _create_base_message(NotificationType.RUNTIME_WARNING, f"⚠️ {title}", body, priority=NotificationPriority.HIGH)
    if metadata:
        msg.metadata = metadata
    return msg

def format_runtime_error_message(title: str, errors: List[str], metadata: Optional[Dict[str, Any]] = None) -> NotificationMessage:
    body = "❌ **Errors:**\n\n"
    for e in errors[:15]:
        body += f"- {e}\n"

    if len(errors) > 15:
        body += f"\n_...and {len(errors) - 15} more._\n"

    msg = _create_base_message(NotificationType.RUNTIME_ERROR, f"🚨 {title}", body, priority=NotificationPriority.CRITICAL)
    if metadata:
        msg.metadata = metadata
    return msg

def format_health_summary_message(summary: Dict[str, Any]) -> NotificationMessage:
    title = "🩺 System Health Summary"

    is_healthy = summary.get("overall_status") == "healthy"
    status_emoji = "✅" if is_healthy else "⚠️"

    body = f"**Status:** {status_emoji} {summary.get('overall_status', 'UNKNOWN').upper()}\n\n"

    checks = summary.get("checks", [])
    failed = [c for c in checks if c.get("status") != "pass"]

    if failed:
        body += "**Failed/Warning Checks:**\n"
        for c in failed:
            body += f"- {c.get('component')}: {c.get('message')}\n"
    else:
        body += "All checks passed successfully.\n"

    return _create_base_message(NotificationType.HEALTH_SUMMARY, title, body)

def format_comparison_report_message(result: 'ComparisonRunResult') -> 'NotificationMessage':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationPriority, NotificationChannel
    from usa_signal_bot.comparison.comparison_reporting import comparison_run_result_to_text

    text = comparison_run_result_to_text(result, limit=10)

    priority = NotificationPriority.NORMAL
    if result.overall_gap_severity.value in ["HIGH", "CRITICAL"]:
        priority = NotificationPriority.HIGH

    return NotificationMessage(
        message_id='test1', notification_type=NotificationType.COMPARISON_REPORT, channel=NotificationChannel.DRY_RUN,
        priority=priority,
        title=f"Comparison Report: {result.overall_gap_severity.value} Gap",
        body=text,
        created_at_utc=result.created_at_utc
    )

def format_execution_gap_warning_message(result: 'ComparisonRunResult') -> 'NotificationMessage':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationPriority, NotificationChannel
    from usa_signal_bot.comparison.comparison_reporting import execution_gap_report_to_text, comparison_limitations_text

    text = f"Execution Realism Bucket: {result.execution_gap.execution_realism_bucket.value}\n\n"
    text += execution_gap_report_to_text(result.execution_gap)
    text += "\n\n" + comparison_limitations_text()

    return NotificationMessage(
        message_id='test2', notification_type=NotificationType.EXECUTION_GAP_WARNING, channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.HIGH,
        title="Execution Gap Warning",
        body=text,
        created_at_utc=result.created_at_utc
    )

def format_signal_drift_warning_message(metrics: 'SignalDriftMetrics') -> 'NotificationMessage':
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationPriority, NotificationChannel
    from usa_signal_bot.comparison.comparison_reporting import signal_drift_report_to_text, comparison_limitations_text
    from datetime import datetime, timezone

    text = signal_drift_report_to_text(metrics)
    text += "\n\n" + comparison_limitations_text()

    return NotificationMessage(
        message_id='test3', notification_type=NotificationType.SIGNAL_DRIFT_WARNING, channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.HIGH,
        title=f"Signal Drift Warning: {metrics.drift_status.value}",
        body=text,
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )


def format_quality_scorecard_message(scorecard: ResearchQualityScorecard) -> NotificationMessage:
    text = research_quality_scorecard_to_text(scorecard)
    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.QUALITY_SCORECARD,
        priority=NotificationPriority.NORMAL,
        title="Research Quality Scorecard",
        text=text,
        metadata={"scorecard_id": scorecard.scorecard_id}
    )

def format_readiness_gate_message(gate_result: ProductionReadinessGateResult) -> NotificationMessage:
    text = production_readiness_gate_result_to_text(gate_result)
    priority = NotificationPriority.HIGH if gate_result.status.name in ["FAILED", "BLOCKED"] else NotificationPriority.NORMAL
    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.READINESS_GATE_REPORT,
        priority=priority,
        title="Production Readiness Gate Report",
        text=text,
        metadata={"gate_id": gate_result.gate_id}
    )

def format_acceptance_report_message(result: SystemAcceptanceResult) -> NotificationMessage:
    text = system_acceptance_result_to_text(result)
    priority = NotificationPriority.HIGH if result.decision.name in ["NOT_ACCEPTED", "BLOCKED"] else NotificationPriority.NORMAL
    return NotificationMessage(
        message_id=create_notification_message_id(),
        type=NotificationType.ACCEPTANCE_REPORT,
        priority=priority,
        title="System Acceptance Evaluator Report",
        text=text,
        metadata={"acceptance_id": result.acceptance_id}
    )

def notifications_from_system_acceptance_result(result: SystemAcceptanceResult) -> List[NotificationMessage]:
    return [
        format_quality_scorecard_message(result.scorecard),
        format_readiness_gate_message(result.gate_result),
        format_acceptance_report_message(result)
    ]

def format_operational_health_report_message(report: 'OperationalHealthReport') -> NotificationMessage:
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    title = f"[🏥 HEALTH] Operational Status: {report.status.value}"
    body = [
        f"Safety: {report.safety_status.value} | Disk: {report.disk_status.value}",
        f"Errors: {report.error_count} | Critical: {report.critical_count}"
    ]
    if report.required_actions:
        body.append("\nRequired Actions:")
        for a in report.required_actions: body.append(f"- {a}")

    body.append("\nNote: Local observability only. Not live execution approval.")
    return NotificationMessage("msg_" + title[:5], NotificationType.OPERATIONAL_HEALTH_REPORT, NotificationChannel.DRY_RUN, NotificationPriority.HIGH if report.status.value in ["WARNING", "CRITICAL", "FAILED"] else NotificationPriority.NORMAL, title, "\n".join(body), "now")

def format_observability_warning_message(title: str, warnings: list[str], metadata: dict = None) -> NotificationMessage:
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    body = ["Observability Warning:", ""]
    for w in warnings: body.append(f"- {w}")
    return NotificationMessage("msg_" + title[:5], NotificationType.OBSERVABILITY_WARNING, NotificationChannel.DRY_RUN, NotificationPriority.HIGH, title, "\n".join(body), "now")

def format_log_rotation_report_message(result: 'LogRotationResult') -> NotificationMessage:
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    title = f"[🔄 LOG ROTATION] Status: {result.status.value}"
    body = [
        f"Original Path: {result.original_path}",
        f"Rotated Path: {result.rotated_path or 'N/A'}",
        f"Original Size: {result.original_size_bytes or 0} bytes"
    ]
    return NotificationMessage("msg_" + title[:5], NotificationType.LOG_ROTATION_REPORT, NotificationChannel.DRY_RUN, NotificationPriority.LOW, title, "\n".join(body), "now")

def notifications_from_operational_health_report(report: 'OperationalHealthReport') -> list[NotificationMessage]:
    return [format_operational_health_report_message(report)]

def format_incident_report_message(report):
    return f"Incident Report: {report.status.name}"

def format_recovery_plan_report_message(plan):
    return f"Recovery Plan: {plan.status.name}"

def format_rollback_dry_run_report_message(result):
    return f"Rollback Result: {result.status.name}"

def format_scheduler_report_message(result: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.scheduler.scheduler_reporting import scheduler_run_result_to_text

    return NotificationMessage(
        message_id=f"sched_report_{result.run_id}",
        notification_type=NotificationType.SCHEDULER_REPORT,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title=f"Scheduler Run {result.status.value}",
        body=scheduler_run_result_to_text(result),
        created_at_utc=result.created_at_utc
    )

def format_lock_warning_message(report: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.scheduler.stale_lock_detector import stale_lock_report_to_text

    return NotificationMessage(
        message_id=report.report_id,
        notification_type=NotificationType.LOCK_WARNING,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.HIGH,
        title=f"Stale Lock Warning ({report.stale_count} locks)",
        body=stale_lock_report_to_text(report),
        created_at_utc=report.created_at_utc
    )

def format_concurrency_blocked_message(result: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.scheduler.scheduler_reporting import concurrency_decision_to_text

    return NotificationMessage(
        message_id=result.decision_id,
        notification_type=NotificationType.CONCURRENCY_BLOCKED,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title="Concurrency Blocked",
        body=concurrency_decision_to_text(result),
        created_at_utc=result.created_at_utc
    )

def notifications_from_scheduler_run_result(result: Any) -> list:
    return [format_scheduler_report_message(result)]

def notifications_from_stale_lock_report(report: Any) -> list:
    if report.stale_count > 0:
        return [format_lock_warning_message(report)]
    return []

def notifications_from_concurrency_decision(result: Any) -> list:
    from usa_signal_bot.core.enums import ConcurrencyDecision
    if result.decision == ConcurrencyDecision.BLOCK:
        return [format_concurrency_blocked_message(result)]
    return []

def format_performance_baseline_report_message(baseline: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.performance.baseline_reporting import performance_baseline_to_text, performance_baseline_limitations_text
    import uuid
    from datetime import datetime, timezone

    text = performance_baseline_to_text(baseline)
    text += performance_baseline_limitations_text()

    return NotificationMessage(
        message_id=f"msg_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        title=f"📈 Performance Baseline Generated: {baseline.scope.value}",
        body=text,
        notification_type=NotificationType.PERFORMANCE_BASELINE_REPORT,
        priority=NotificationPriority.NORMAL,
        channel=NotificationChannel.DRY_RUN,
        metadata={"baseline_id": baseline.baseline_id, "version": baseline.version}
    )

def format_sla_threshold_warning_message(report: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority, BaselineComparisonStatus
    from usa_signal_bot.performance.baseline_reporting import sla_evaluation_report_to_text, performance_baseline_limitations_text
    import uuid
    from datetime import datetime, timezone

    text = sla_evaluation_report_to_text(report)
    text += performance_baseline_limitations_text()

    priority = NotificationPriority.HIGH
    if report.status == BaselineComparisonStatus.BLOCKED:
        priority = NotificationPriority.CRITICAL

    return NotificationMessage(
        message_id=f"msg_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        title=f"⚠️ SLA Threshold Warning: {report.status.value}",
        body=text,
        notification_type=NotificationType.SLA_THRESHOLD_WARNING,
        priority=priority,
        channel=NotificationChannel.DRY_RUN,
        metadata={"report_id": report.report_id}
    )

def format_runtime_regression_alert_message(alerts: List[Any]) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.performance.baseline_reporting import performance_alerts_to_text, performance_baseline_limitations_text
    import uuid
    from datetime import datetime, timezone

    text = performance_alerts_to_text(alerts)
    text += performance_baseline_limitations_text()

    # Check max severity from alerts to drive priority
    priority = NotificationPriority.HIGH
    for a in alerts:
        from usa_signal_bot.core.enums import SLASeverity
        if a.severity == SLASeverity.BLOCKER:
            priority = NotificationPriority.CRITICAL

    return NotificationMessage(
        message_id=f"msg_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        title=f"🚨 Runtime Regression Alerts ({len(alerts)})",
        body=text,
        notification_type=NotificationType.RUNTIME_REGRESSION_ALERT,
        priority=priority,
        channel=NotificationChannel.DRY_RUN,
        metadata={"alert_count": len(alerts)}
    )

def notifications_from_performance_review(result: Any) -> List[Any]:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.performance.baseline_reporting import performance_review_result_to_text
    import uuid
    from datetime import datetime, timezone

    text = performance_review_result_to_text(result)
    priority = NotificationPriority.NORMAL
    from usa_signal_bot.core.enums import BaselineComparisonStatus
    if result.acceptance_status in [BaselineComparisonStatus.FAIL, BaselineComparisonStatus.BLOCKED]:
        priority = NotificationPriority.HIGH

    msg = NotificationMessage(
        message_id=f"msg_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        title=f"📊 Performance Review: {result.acceptance_status.value}",
        body=text,
        notification_type=NotificationType.PERFORMANCE_BASELINE_REPORT,
        priority=priority,
        channel=NotificationChannel.DRY_RUN,
        metadata={"review_id": result.review_id}
    )
    return [msg]

def notifications_from_performance_alerts(alerts: List[Any]) -> List[Any]:
    if not alerts:
        return []
    return [format_runtime_regression_alert_message(alerts)]

def format_liquidity_warning_message(profiles: list) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType, NotificationPriority, NotificationChannel
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    import uuid
    import datetime

    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    title = f"Liquidity Warning ({len(profiles)} symbols)"

    lines = ["The following symbols have liquidity warnings:"]
    for p in profiles:
        lines.append(f"- {p.symbol}: {p.status.value}")

    body = "\n".join(lines)
    return NotificationMessage(
        message_id=msg_id,
        notification_type=NotificationType.LIQUIDITY_WARNING,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.HIGH,
        title=title,
        body=body,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

def format_tradability_guard_report_message(review) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType, NotificationPriority, NotificationChannel
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    import uuid
    import datetime

    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    title = "Tradability Guard Report"

    blocked = sum(1 for t in review.tradability_results if t.status.value == "BLOCK_SIGNAL")
    body = f"Analyzed {len(review.symbols)} symbols. Blocked {blocked} signals due to tradability constraints.\nNo live orders are generated."

    return NotificationMessage(
        message_id=msg_id,
        notification_type=NotificationType.TRADABILITY_GUARD_REPORT,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.NORMAL,
        title=title,
        body=body,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

def format_execution_realism_warning_message(review) -> 'NotificationMessage':
    from usa_signal_bot.core.enums import NotificationType, NotificationPriority, NotificationChannel
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    import uuid
    import datetime

    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    title = "Execution Realism Warning"

    body = "Execution realism review indicates optimistic or unrealistic assumptions.\n"
    if review.warnings:
        body += "Warnings:\n"
        for w in review.warnings[:5]:
            body += f"- {w}\n"

    return NotificationMessage(
        message_id=msg_id,
        notification_type=NotificationType.EXECUTION_REALISM_WARNING,
        channel=NotificationChannel.DRY_RUN,
        priority=NotificationPriority.HIGH,
        title=title,
        body=body,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

def notifications_from_execution_realism_review(review) -> list:
    msgs = []

    illiquid_profiles = [p for p in review.liquidity_profiles if p.status.value in ["THIN", "ILLIQUID"]]
    if illiquid_profiles:
        msgs.append(format_liquidity_warning_message(illiquid_profiles))

    msgs.append(format_tradability_guard_report_message(review))

    if review.report_type.value in ["UNREALISTIC", "OPTIMISTIC"] or len(review.warnings) > 0:
        msgs.append(format_execution_realism_warning_message(review))

    return msgs


from typing import Any, Dict, List
from usa_signal_bot.cost_robustness.robustness_models import CostRobustnessReview, CostFragilityAssessment, ExecutionSensitivityMatrix

def format_cost_robustness_report_message(review: CostRobustnessReview) -> Dict[str, Any]:
    return {"message": "Cost Robustness Report", "review_id": review.review_id}

def format_cost_fragility_warning_message(assessment: CostFragilityAssessment) -> Dict[str, Any]:
    return {"message": "Cost Fragility Warning", "score": assessment.fragility_score}

def format_execution_sensitivity_warning_message(matrix: ExecutionSensitivityMatrix) -> Dict[str, Any]:
    return {"message": "Execution Sensitivity Warning", "status": matrix.robustness_status}

def notifications_from_cost_robustness_review(review: CostRobustnessReview) -> List[Dict[str, Any]]:
    return [format_cost_robustness_report_message(review)]

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
        body="\n".join(lines),
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
        body="\n".join(lines),
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
        body="\n".join(lines),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        metadata={"review_id": review.review_id}
    )


from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview, RegimeTransitionSignal, SymbolRegimeAlignment
from usa_signal_bot.regime_map.regime_map_reporting import regime_map_review_to_text, regime_transition_signal_to_text, symbol_regime_alignment_to_text

def format_regime_map_report_message(review: RegimeMapReview) -> NotificationMessage:
    body = regime_map_review_to_text(review, limit=20)
    return NotificationMessage(
        title=f"Regime Map Review: {review.universe_name}",
        body=body,
        type="REGIME_MAP_REPORT"
    )

def format_regime_transition_warning_message(signals: list[RegimeTransitionSignal]) -> NotificationMessage:
    lines = [regime_transition_signal_to_text(s) for s in signals]
    return NotificationMessage(
        title="Regime Transition Warning",
        body="\n".join(lines),
        type="REGIME_TRANSITION_WARNING"
    )

def format_regime_alignment_warning_message(alignments: list[SymbolRegimeAlignment]) -> NotificationMessage:
    lines = [symbol_regime_alignment_to_text(a) for a in alignments]
    return NotificationMessage(
        title="Regime Alignment Warning",
        body="\n".join(lines),
        type="REGIME_ALIGNMENT_WARNING"
    )

def notifications_from_regime_map_review(review: RegimeMapReview) -> list[NotificationMessage]:
    messages = [format_regime_map_report_message(review)]

    if review.transition_signals:
         high_risks = [s for s in review.transition_signals if s.risk.value in ["HIGH", "CRITICAL"]]
         if high_risks:
             messages.append(format_regime_transition_warning_message(high_risks))

    if review.alignments:
         conflicts = [a for a in review.alignments if a.status.value == "CONFLICTED"]
         if conflicts:
             messages.append(format_regime_alignment_warning_message(conflicts))

    return messages


def format_allocation_report_message(review) -> NotificationMessage:
    body = (
        f"Allocation Review ID: {review.review_id}\n"
        f"Total Allocated: ${review.total_allocated_notional_usd}\n"
        f"Blocked: {review.blocked_count}\n"
        f"Note: Dry-run sizing metadata. Not an investment advice. No broker execution."
    )
    return NotificationMessage("Allocation Review Report", body)

def format_position_size_warning_message(results) -> NotificationMessage:
    blocked = [r.symbol for r in results if r.status.value in ["BLOCKED", "SUPPRESSED"]]
    body = f"The following symbols had sizing blocked/suppressed: {', '.join(blocked)}"
    return NotificationMessage("Position Size Warning", body)

def format_risk_budget_warning_message(budget) -> NotificationMessage:
    body = f"Risk Budget Status: {budget.status.value}\nWarnings: {', '.join(budget.warnings)}"
    return NotificationMessage("Risk Budget Warning", body)

def format_portfolio_construction_report_message(review) -> dict:
    from usa_signal_bot.portfolio_construction.construction_reporting import portfolio_construction_review_to_text
    return {
        "title": "Portfolio Construction Review",
        "body": portfolio_construction_review_to_text(review, 10)
    }

def notifications_from_portfolio_construction_review(review) -> list:
    return [format_portfolio_construction_report_message(review)]

def format_rebalance_report_message(review: Any) -> Any:
    # Basic stub
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    return NotificationMessage(channel="dry_run", message="Rebalance report review required.")

def format_turnover_warning_message(assessment: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    return NotificationMessage(channel="dry_run", message="High turnover warning.")

def format_drift_warning_message(measurements: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    return NotificationMessage(channel="dry_run", message="Drift warning.")

def notifications_from_rebalance_review(review: Any) -> Any:
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    return [NotificationMessage(channel="dry_run", message="Rebalance review required.")]
