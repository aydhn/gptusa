from typing import Any, List, Dict
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import ZeroMutationBaseline
from usa_signal_bot.core.enums import FirewallAuditRiskFlag

def required_zero_mutation_invariants() -> List[str]:
    return [
        "NO_STATE_COMMITTED",
        "NO_ORDER_EXECUTED",
        "NO_PORTFOLIO_MUTATED",
        "NO_POSITION_MUTATED",
        "NO_CASH_MUTATED",
        "NO_EQUITY_MUTATED",
        "NO_CONFIG_PATCHED",
        "NO_BROKER_ORDER",
        "NO_TELEGRAM_SEND"
    ]

def check_zero_mutation_invariants(before: ZeroMutationBaseline, after: ZeroMutationBaseline) -> dict[str, bool]:
    return {
        "NO_STATE_COMMITTED": not after.paper_state_committed,
        "NO_ORDER_EXECUTED": not after.paper_order_executed,
        "NO_PORTFOLIO_MUTATED": not after.portfolio_state_mutated,
        "NO_POSITION_MUTATED": not after.position_mutated,
        "NO_CASH_MUTATED": not after.cash_mutated,
        "NO_EQUITY_MUTATED": not after.equity_mutated,
        "NO_CONFIG_PATCHED": not after.config_patched,
        "NO_BROKER_ORDER": not after.broker_order_sent,
        "NO_TELEGRAM_SEND": not after.telegram_real_sent
    }

def failed_zero_mutation_invariants(results: dict[str, bool]) -> List[str]:
    return [k for k, v in results.items() if not v]

def invariant_results_to_risk_flags(results: dict[str, bool]) -> List[FirewallAuditRiskFlag]:
    flags = []
    if not results.get("NO_BROKER_ORDER", True): flags.append(FirewallAuditRiskFlag.BROKER_ORDER_RISK)
    if not results.get("NO_STATE_COMMITTED", True): flags.append(FirewallAuditRiskFlag.PAPER_STATE_MUTATION_RISK)
    if not results.get("NO_TELEGRAM_SEND", True): flags.append(FirewallAuditRiskFlag.TELEGRAM_REAL_SEND_RISK)
    return flags

def mutation_invariant_checker_summary(results: dict[str, bool]) -> dict[str, Any]:
    return {"failed": failed_zero_mutation_invariants(results)}

def mutation_invariant_checker_to_text(results: dict[str, bool]) -> str:
    failed = failed_zero_mutation_invariants(results)
    return f"Invariants failed: {len(failed)}"
