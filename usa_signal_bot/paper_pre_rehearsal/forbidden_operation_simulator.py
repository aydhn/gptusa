from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_pre_rehearsal.mutation_firewall import PaperStateMutationFirewall
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import MutationFirewallEvent
from usa_signal_bot.core.enums import MutationAttemptType

def simulate_paper_state_write_attempt(firewall: PaperStateMutationFirewall, session_id: Optional[str] = None) -> MutationFirewallEvent:
    return firewall.evaluate_attempt(MutationAttemptType.PAPER_STATE_WRITE, session_id, "simulator")

def simulate_paper_order_create_attempt(firewall: PaperStateMutationFirewall, session_id: Optional[str] = None) -> MutationFirewallEvent:
    return firewall.evaluate_attempt(MutationAttemptType.PAPER_ORDER_CREATE, session_id, "simulator")

def simulate_broker_order_send_attempt(firewall: PaperStateMutationFirewall, session_id: Optional[str] = None) -> MutationFirewallEvent:
    return firewall.evaluate_attempt(MutationAttemptType.BROKER_ORDER_SEND, session_id, "simulator")

def simulate_active_paper_enable_attempt(firewall: PaperStateMutationFirewall, session_id: Optional[str] = None) -> MutationFirewallEvent:
    return firewall.evaluate_attempt(MutationAttemptType.ACTIVE_PAPER_ENABLE, session_id, "simulator")

def simulate_forbidden_operations(firewall: PaperStateMutationFirewall, session_id: Optional[str] = None) -> List[MutationFirewallEvent]:
    events = []
    events.append(simulate_paper_state_write_attempt(firewall, session_id))
    events.append(simulate_paper_order_create_attempt(firewall, session_id))
    events.append(simulate_broker_order_send_attempt(firewall, session_id))
    events.append(simulate_active_paper_enable_attempt(firewall, session_id))
    return events

def forbidden_operation_simulator_summary(events: List[MutationFirewallEvent]) -> Dict[str, Any]:
    return {
        "simulated_events": len(events),
        "all_blocked": all(e.blocked for e in events)
    }

def forbidden_operation_simulator_to_text(events: List[MutationFirewallEvent]) -> str:
    s = forbidden_operation_simulator_summary(events)
    return f"Forbidden Simulator: {s['simulated_events']} simulated, All Blocked: {s['all_blocked']}"
