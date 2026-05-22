from typing import Any, Dict, List, Optional
import datetime
import uuid
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalRun,
    PrePaperDryRehearsalPlan,
    MutationFirewallEvent,
    create_pre_paper_run_id,
    validate_pre_paper_dry_rehearsal_run
)
from usa_signal_bot.paper_pre_rehearsal.mutation_firewall import PaperStateMutationFirewall
from usa_signal_bot.paper_pre_rehearsal.forbidden_operation_simulator import simulate_forbidden_operations
from usa_signal_bot.paper_pre_rehearsal.paper_baseline_loader import paper_baseline_hash
from usa_signal_bot.core.enums import PrePaperDryRehearsalStatus, PrePaperDryRehearsalDecision, PrePaperRiskFlag

class GuardedPrePaperDryRehearsalRunner:
    def __init__(self, firewall: Optional[PaperStateMutationFirewall] = None, simulate_forbidden_attempts: bool = True):
        self.firewall = firewall or PaperStateMutationFirewall()
        self.simulate_forbidden_attempts = simulate_forbidden_attempts

    def run_read_only_stage(self, plan: PrePaperDryRehearsalPlan, paper_baseline: Dict[str, Any]) -> Dict[str, Any]:
        # Do not mutate the original baseline
        return {
            "stage": "read_only",
            "baseline_hash": paper_baseline_hash(paper_baseline),
            "simulated_signals": [],
            "simulated_fills": []
        }

    def run_firewall_stage(self, plan: PrePaperDryRehearsalPlan, session_id: str) -> List[MutationFirewallEvent]:
        events = []
        if self.simulate_forbidden_attempts:
            events.extend(simulate_forbidden_operations(self.firewall, session_id))
        return events

    def determine_run_decision(self, events: List[MutationFirewallEvent]) -> PrePaperDryRehearsalDecision:
        if not all(e.blocked for e in events):
            return PrePaperDryRehearsalDecision.BLOCK
        return PrePaperDryRehearsalDecision.REQUEST_MANUAL_REVIEW # Safest default

    def validate_run_safety(self, run: PrePaperDryRehearsalRun) -> List[str]:
        violations = []
        if run.plan and run.plan.execution_enabled:
            violations.append("execution_enabled is true")
        if not all(e.blocked for e in run.firewall_events):
            violations.append("Not all firewall events were blocked")
        return violations

    def run_rehearsal(self, plan: PrePaperDryRehearsalPlan, paper_baseline: Optional[Dict[str, Any]] = None) -> PrePaperDryRehearsalRun:
        run_id = create_pre_paper_run_id()
        started_at = datetime.datetime.utcnow().isoformat()

        baseline = paper_baseline or {}
        read_only_output = self.run_read_only_stage(plan, baseline)
        firewall_events = self.run_firewall_stage(plan, session_id=run_id)

        decision = self.determine_run_decision(firewall_events)
        status = PrePaperDryRehearsalStatus.COMPLETED if decision != PrePaperDryRehearsalDecision.BLOCK else PrePaperDryRehearsalStatus.FAILED

        output_summary = {
            "read_only_output": read_only_output,
            "simulated_events": len(firewall_events)
        }

        run = PrePaperDryRehearsalRun(
            run_id=run_id,
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            status=status,
            candidate_id=plan.candidate_id,
            plan=plan,
            firewall_rules=self.firewall.rules,
            firewall_events=firewall_events,
            read_only_paper_baseline=baseline,
            output_summary=output_summary,
            decision=decision,
            safety_flags=[PrePaperRiskFlag.ACTIVATION_ALLOWED_RISK], # Always flag until checkpoint
            started_at_utc=started_at,
            completed_at_utc=datetime.datetime.utcnow().isoformat(),
            output_paths={},
            warnings=[],
            errors=[]
        )
        validate_pre_paper_dry_rehearsal_run(run)
        return run

def dry_rehearsal_run_summary(run: PrePaperDryRehearsalRun) -> Dict[str, Any]:
    return {
        "run_id": run.run_id,
        "status": run.status.value,
        "decision": run.decision.value,
        "firewall_events": len(run.firewall_events)
    }
