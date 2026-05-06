import datetime
import re
from typing import Dict, Any, List, Optional

from usa_signal_bot.core.enums import NotificationChannel, NotificationType, NotificationPriority
from usa_signal_bot.notifications.notification_models import NotificationMessage, NotificationConfig, create_notification_message_id
from usa_signal_bot.runtime.runtime_models import MarketScanResult
from usa_signal_bot.portfolio.portfolio_models import PortfolioCandidate, AllocationResult
from usa_signal_bot.risk.risk_models import RiskDecision

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
