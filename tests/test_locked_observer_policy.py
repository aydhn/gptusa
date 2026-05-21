from usa_signal_bot.paper_observer.locked_observer_policy import default_locked_observer_policy, validate_locked_policy_safety

def test_default_locked_observer_policy():
    policy = default_locked_observer_policy()
    assert policy.locked_runtime is True
    assert policy.allow_active_paper is False
    assert policy.allow_broker_orders is False

    errors = validate_locked_policy_safety(policy)
    assert len(errors) == 0

def test_validate_locked_policy_safety_errors():
    policy = default_locked_observer_policy()
    policy.locked_runtime = False
    policy.allow_active_paper = True

    errors = validate_locked_policy_safety(policy)
    assert len(errors) == 2
    assert any("must have locked_runtime=True" in e for e in errors)
    assert any("cannot allow active paper" in e for e in errors)
