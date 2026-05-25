from usa_signal_bot.data_provider_runtime.provider_runtime_policy import build_phase107_provider_runtime_policy, validate_provider_runtime_policy

def test_provider_runtime_policy():
    policy = build_phase107_provider_runtime_policy()
    errors = validate_provider_runtime_policy(policy)
    assert len(errors) == 0
