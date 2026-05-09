def test_retention_policy():
    from usa_signal_bot.retention.retention_models import RetentionPolicy, RetentionArtifactType, RetentionPolicyAction
    p = RetentionPolicy(
        policy_id="test",
        artifact_type=RetentionArtifactType.TEMP_FILE,
        name="test",
        enabled=True,
        keep_latest=0,
        action=RetentionPolicyAction.DELETE
    )
    assert p.artifact_type == RetentionArtifactType.TEMP_FILE

def test_retention_policy_validation():
    from usa_signal_bot.retention.retention_models import RetentionPolicy, RetentionArtifactType, RetentionPolicyAction, validate_retention_policy
    import pytest
    p = RetentionPolicy(
        policy_id="test",
        artifact_type=RetentionArtifactType.TEMP_FILE,
        name="test",
        enabled=True,
        keep_latest=-1,
        action=RetentionPolicyAction.DELETE
    )
    with pytest.raises(ValueError):
        validate_retention_policy(p)

def test_id_factory():
    from usa_signal_bot.retention.retention_models import create_retention_policy_id
    assert create_retention_policy_id("test").startswith("policy_")
