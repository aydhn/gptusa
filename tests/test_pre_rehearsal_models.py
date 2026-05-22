import pytest
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalPlan,
    MutationFirewallRule,
    MutationFirewallEvent,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    validate_pre_paper_dry_rehearsal_plan,
    validate_mutation_firewall_rule,
    validate_activation_denied_checkpoint
)
from usa_signal_bot.core.enums import (
    PrePaperDryRehearsalStatus,
    PrePaperDryRehearsalDecision,
    MutationAttemptType,
    FirewallAction,
    ActivationDeniedCheckpointStatus,
    ActivationDeniedDecision
)

def test_validate_plan():
    plan = PrePaperDryRehearsalPlan(
        plan_id="p1", created_at_utc="t", candidate_id="c1", source_checkpoint_id=None, source_archive_id=None,
        status=PrePaperDryRehearsalStatus.DRAFT, decision=PrePaperDryRehearsalDecision.INCONCLUSIVE,
        required_inputs=[], expected_outputs=[], firewall_required=True, activation_denied_required=True,
        execution_enabled=False, active_paper_enabled=False, broker_execution_enabled=False,
        paper_state_mutation_enabled=False, config_patch_enabled=False, telegram_real_send_enabled=False,
        warnings=[], errors=[]
    )
    validate_pre_paper_dry_rehearsal_plan(plan)  # should not raise

    plan.execution_enabled = True
    with pytest.raises(ValueError):
        validate_pre_paper_dry_rehearsal_plan(plan)

def test_validate_firewall_rule():
    rule = MutationFirewallRule(
        rule_id="r1", created_at_utc="t", attempt_type=MutationAttemptType.PAPER_STATE_WRITE,
        action=FirewallAction.DENY_AND_RECORD, enabled=True, blocking=True, description="d",
        risk_flags=[], warnings=[], errors=[]
    )
    validate_mutation_firewall_rule(rule)

    rule.action = FirewallAction.ALLOW_READ_ONLY
    with pytest.raises(ValueError):
        validate_mutation_firewall_rule(rule)

def test_validate_activation_checkpoint():
    cp = ActivationDeniedCheckpoint(
        checkpoint_id="cp1", created_at_utc="t", status=ActivationDeniedCheckpointStatus.CREATED,
        decision=ActivationDeniedDecision.DENY_ACTIVATION_AND_CONTINUE_AUDIT, candidate_id=None,
        source_run_id=None, source_plan_id=None, activation_denied=True, denial_reason="",
        required_followups=[], safety_flags=[], allows_active_paper=False, allows_broker_execution=False,
        allows_paper_state_mutation=False, allows_config_patch=False, allows_telegram_real_send=False,
        warnings=[], errors=[]
    )
    validate_activation_denied_checkpoint(cp)

    cp.activation_denied = False
    with pytest.raises(ValueError):
        validate_activation_denied_checkpoint(cp)
