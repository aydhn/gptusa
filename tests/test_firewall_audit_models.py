import pytest
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import FirewallReplayPlan, validate_firewall_replay_plan
from usa_signal_bot.core.enums import FirewallReplayStatus, FirewallReplayDecision

def test_firewall_replay_plan_validation():
    plan = FirewallReplayPlan(
        replay_plan_id="test", created_at_utc="test", candidate_id=None, source_pre_rehearsal_review_id=None,
        source_pre_paper_run_id=None, status=FirewallReplayStatus.READY, decision=FirewallReplayDecision.REPLAY_FIREWALL_EVENTS,
        required_attempt_types=[], replay_event_count=0, require_all_dangerous_attempts_blocked=True,
        execution_enabled=False, active_paper_enabled=False, broker_execution_enabled=False,
        paper_state_mutation_enabled=False, config_patch_enabled=False, telegram_real_send_enabled=False,
        warnings=[], errors=[]
    )
    validate_firewall_replay_plan(plan)

    plan.execution_enabled = True
    with pytest.raises(ValueError):
        validate_firewall_replay_plan(plan)
