import pytest
from usa_signal_bot.retention.retention_models import RetentionPolicy, RetentionArtifactType, RetentionPolicyAction
from usa_signal_bot.retention.retention_validation import validate_retention_policies_report

def test_validate_policies_valid():
    p = RetentionPolicy(
        policy_id="p1", artifact_type=RetentionArtifactType.TEMP_FILE,
        name="test", enabled=True, keep_latest=5, action=RetentionPolicyAction.REVIEW
    )
    rep = validate_retention_policies_report([p])
    assert rep.valid is True
    assert rep.blocked_count == 0

def test_validate_policies_invalid():
    p = RetentionPolicy(
        policy_id="p1", artifact_type=RetentionArtifactType.RELEASE_BUILD,
        name="test", enabled=True, keep_latest=5, action=RetentionPolicyAction.DELETE, protected=True
    )
    rep = validate_retention_policies_report([p])
    assert rep.valid is False
    assert rep.blocked_count == 1
