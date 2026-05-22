from typing import Any, Dict
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalPlan,
    MutationFirewallRule,
    MutationFirewallEvent,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    PrePaperAuditEntry,
    PrePaperDryRehearsalReview
)
from usa_signal_bot.paper_pre_rehearsal.dry_rehearsal_plan import pre_paper_plan_to_text
from usa_signal_bot.paper_pre_rehearsal.firewall_rules import firewall_rules_to_text
from usa_signal_bot.paper_pre_rehearsal.activation_denied_checkpoint import activation_denied_checkpoint_to_text
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_audit import pre_paper_audit_to_text
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_report import pre_paper_dry_rehearsal_review_to_text, pre_paper_rehearsal_limitations_text
from usa_signal_bot.paper_pre_rehearsal.rehearsal_output_analyzer import analyze_pre_paper_rehearsal_run

def mutation_firewall_rule_to_text(item: MutationFirewallRule) -> str:
    return f"Rule {item.rule_id} for {item.attempt_type.value}: Action={item.action.value}, Blocking={item.blocking}"

def mutation_firewall_event_to_text(item: MutationFirewallEvent) -> str:
    return f"Event {item.event_id}: {item.attempt_type.value} -> Action={item.action.value}, Blocked={item.blocked}"

def pre_paper_dry_rehearsal_run_to_text(item: PrePaperDryRehearsalRun, limit: int = 100) -> str:
    analysis = analyze_pre_paper_rehearsal_run(item)
    return f"Run {item.run_id} (Status: {item.status.value}, Decision: {item.decision.value}): {analysis['firewall_event_count']} events, {analysis['blocked_event_count']} blocked. Warnings: {len(analysis['warnings'])}"

def pre_paper_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Pre-Paper Store Summary: {summary['plans']} plans, {summary['runs']} runs, {summary['checkpoints']} checkpoints, {summary['reviews']} reviews."
