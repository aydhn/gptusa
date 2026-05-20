from typing import Any
from usa_signal_bot.paper_quarantine.quarantine_models import ReadOnlyPromotionTicket

def register_promotion_ticket(ticket: ReadOnlyPromotionTicket, registry: list[ReadOnlyPromotionTicket] | None = None) -> list[ReadOnlyPromotionTicket]:
    reg = registry if registry is not None else []

    # remove existing
    reg = [t for t in reg if t.ticket_id != ticket.ticket_id]
    reg.append(ticket)

    # sort by created descending
    return sorted(reg, key=lambda x: x.created_at_utc, reverse=True)

def find_ticket_by_id(registry: list[ReadOnlyPromotionTicket], ticket_id: str) -> ReadOnlyPromotionTicket | None:
    for t in registry:
        if t.ticket_id == ticket_id:
            return t
    return None

def find_tickets_by_candidate_id(registry: list[ReadOnlyPromotionTicket], candidate_id: str) -> list[ReadOnlyPromotionTicket]:
    return [t for t in registry if t.candidate_id == candidate_id]

def latest_ticket_for_candidate(registry: list[ReadOnlyPromotionTicket], candidate_id: str) -> ReadOnlyPromotionTicket | None:
    tickets = find_tickets_by_candidate_id(registry, candidate_id)
    if not tickets:
        return None
    return sorted(tickets, key=lambda x: x.created_at_utc, reverse=True)[0]

def ticket_registry_summary(registry: list[ReadOnlyPromotionTicket]) -> dict[str, Any]:
    return {
        "total_tickets": len(registry),
        "waiting_review": len([t for t in registry if t.status.value == "waiting_review"]),
        "blocked": len([t for t in registry if t.status.value == "blocked"]),
    }

def ticket_registry_to_text(registry: list[ReadOnlyPromotionTicket], limit: int = 100) -> str:
    summary = ticket_registry_summary(registry)
    lines = [
        "Promotion Ticket Registry Summary",
        f"Total: {summary['total_tickets']}",
        f"Waiting Review: {summary['waiting_review']}",
        f"Blocked: {summary['blocked']}",
        "-" * 20
    ]
    for t in registry[:limit]:
        lines.append(f"{t.ticket_id} | {t.status.value} | {t.candidate_id}")
    return "\n".join(lines)
