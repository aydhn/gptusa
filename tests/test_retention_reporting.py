import pytest

def test_limitations_text():
    from usa_signal_bot.retention.retention_reporting import retention_limitations_text
    txt = retention_limitations_text()
    assert "Disclaimer: Local cleanup only." in txt
    assert "Not investment advice." in txt

def test_policy_to_text():
    from usa_signal_bot.retention.retention_models import RetentionPolicy, RetentionArtifactType, RetentionPolicyAction
    from usa_signal_bot.retention.retention_reporting import retention_policy_to_text

    p = RetentionPolicy(
        policy_id="p1", artifact_type=RetentionArtifactType.TEMP_FILE,
        name="test", enabled=True, keep_latest=5, action=RetentionPolicyAction.DELETE
    )
    txt = retention_policy_to_text(p)
    assert "[TEMP_FILE]" in txt
    assert "Action=DELETE" in txt
